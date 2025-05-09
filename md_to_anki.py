import genanki
import markdown
import re
import random
import os

# Function to convert Markdown LaTeX to Anki's MathJax format
def convert_latex_for_anki(text):
    text = re.sub(r'\$\$(.*?)\$\$', r'\[\1\]', text, flags=re.DOTALL)
    text = re.sub(r'\$(.*?)\$', r'\\(\1\\)', text)
    return text

def get_heading_level(line):
    """Determines the heading level (1-6) or 0 if not a heading."""
    stripped_line = line.strip()
    if stripped_line.startswith("###### "): return 6
    if stripped_line.startswith("##### "): return 5
    if stripped_line.startswith("#### "): return 4
    if stripped_line.startswith("### "): return 3
    if stripped_line.startswith("## "): return 2
    if stripped_line.startswith("# "): return 1
    return 0

def extract_heading_text(line, level):
    """Extracts text from a heading line."""
    return line.strip()[level+1:].strip()


def markdown_to_anki_deepest_level(md_filepath, output_apkg_filepath):
    model_id = random.randrange(1 << 30, 1 << 31)
    anki_model = genanki.Model(
        model_id,
        'DNN Mindmap Deepest Level Model (MD)',
        fields=[
            {'name': 'Question'}, # The deepest heading text
            {'name': 'Answer'},   # Content under the deepest heading
            {'name': 'Path'},     # Hierarchical path to the question
            {'name': 'SourceMD_Card'}, # Original Markdown for this card's content
        ],
        templates=[
            {
                'name': 'Card 1',
                'qfmt': '{{Question}}<div style="font-size:0.8em; color:grey; margin-top:10px;">Path: {{Path}}</div>',
                'afmt': '{{FrontSide}}\n\n<hr id="answer">\n\n{{Answer}}',
            },
        ],
        css="""
        .card {
            font-family: arial;
            font-size: 20px;
            text-align: left;
            color: black;
            background-color: white;
        }
        .card pre {
            white-space: pre-wrap; /* Ensures code blocks wrap */
            background-color: #f0f0f0;
            padding: 10px;
            border-radius: 5px;
            font-family: monospace;
        }
        .card code {
            font-family: monospace;
            background-color: #e0e0e0;
            padding: 2px 4px;
            border-radius: 3px;
        }
        ul, ol {
            margin-left: 20px;
            padding-left: 20px;
        }
        li {
            margin-bottom: 0.5em;
        }
        h1, h2, h3, h4, h5, h6 { /* Styles for headings if they appear in answer */
            margin-top: 1em;
            margin-bottom: 0.5em;
            font-weight: bold;
        }
        h4 { font-size: 1.1em; }
        h5 { font-size: 1.0em; }
        h6 { font-size: 0.9em; }
        """
    )

    deck_id = random.randrange(1 << 30, 1 << 31)
    deck_name = "Deep Neural Network Mindmap (Deepest)" # Default deck name
    all_anki_notes = []

    current_path_headings = ["", "", "", "", "", ""] # H1 to H6
    current_card_question = None
    current_card_answer_md_lines = []
    current_card_level = 0 # Level of the current_card_question

    try:
        with open(md_filepath, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except FileNotFoundError:
        print(f"Error: Markdown file not found at {md_filepath}")
        return
    except Exception as e:
        print(f"Error reading Markdown file: {e}")
        return

    first_h1_found_for_deck_name = False

    for line_num, line_content_raw in enumerate(lines):
        line_level = get_heading_level(line_content_raw)

        # Set Deck Name from the very first H1
        if not first_h1_found_for_deck_name and line_level == 1:
            deck_name = extract_heading_text(line_content_raw, 1)
            first_h1_found_for_deck_name = True
            # H1 itself won't form a card if it's just the deck title,
            # but its text is stored for path context if needed.
            current_path_headings[0] = deck_name # Store H1 for path
            continue # Don't process H1 as a card question immediately

        # If a new heading is encountered OR it's the end of file,
        # process the accumulated content for the *previous* card.
        is_new_heading = (line_level > 0)
        is_eof = (line_num == len(lines) - 1)

        if current_card_question is not None and \
           (is_new_heading and line_level <= current_card_level or is_eof) :
            # Add the last line to answer if it's EOF and not a new heading
            if is_eof and not is_new_heading:
                if line_content_raw.strip(): # Only add if non-empty
                    current_card_answer_md_lines.append(line_content_raw.rstrip('\n'))

            if current_card_answer_md_lines: # Only create card if there's an answer
                answer_md_text = "\n".join(current_card_answer_md_lines).strip()
                if answer_md_text: # Double check answer is not just whitespace
                    answer_html = markdown.markdown(
                        answer_md_text,
                        extensions=['fenced_code', 'tables', 'nl2br']
                    )

                    # Construct path from H1 up to one level above current_card_level
                    path_parts = [h for h in current_path_headings[:current_card_level-1] if h]
                    
                    note_question = convert_latex_for_anki(current_card_question)
                    note_answer = convert_latex_for_anki(answer_html)
                    note_path = convert_latex_for_anki(" > ".join(path_parts))
                    source_md_card = f"Q ({current_card_level}): {current_card_question}\n\nA (raw MD):\n{answer_md_text}"

                    anki_note = genanki.Note(
                        model=anki_model,
                        fields=[note_question, note_answer, note_path, source_md_card]
                    )
                    all_anki_notes.append(anki_note)

            # Reset for the next card, regardless of whether a card was made
            current_card_question = None
            current_card_answer_md_lines = []
            current_card_level = 0


        # Update current path and identify new potential card question
        if line_level > 0:
            heading_text = extract_heading_text(line_content_raw, line_level)
            current_path_headings[line_level-1] = heading_text # Update path context for this level

            # Clear path context for deeper levels
            for i in range(line_level, 6):
                current_path_headings[i] = ""

            # This new heading becomes the question for the next card
            current_card_question = heading_text
            current_card_level = line_level
            current_card_answer_md_lines = [] # Start accumulating answer for this new question

        # If it's a content line for an active card question
        elif current_card_question is not None:
            if line_content_raw.strip() or current_card_answer_md_lines: # Add non-empty or if already started
                current_card_answer_md_lines.append(line_content_raw.rstrip('\n'))
        
        # If it's the very last line and it was content, it should be processed above.
        # If it was a heading, it also got processed.

    # --- Final check for any pending card at EOF (already handled in loop for EOF) ---

    if not all_anki_notes:
        print("No notes were generated. Check your Markdown heading structure.")
        return

    anki_deck = genanki.Deck(deck_id, deck_name)
    for note in all_anki_notes:
        anki_deck.add_note(note)

    genanki.Package(anki_deck).write_to_file(output_apkg_filepath)
    print(f"Successfully created Anki package: {output_apkg_filepath} with {len(all_anki_notes)} notes.")


# --- Main execution ---
if __name__ == "__main__":

    input_md = "./mynotes/deep-neural-network_copy.md" # Replace with your actual MD file name

    output_apkg = "dnn_anki_deck-3.apkg"
    
    markdown_to_anki_deepest_level(input_md, output_apkg)
