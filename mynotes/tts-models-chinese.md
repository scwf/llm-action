
| 项目                   | 中文支持                                | 零样本声音克隆                                                  | 本地部署（公开权重/代码）                             | 
| -------------------- | ----------------------------------- | -------------------------------------------------------- | ----------------------------------------- | 
| **SPARK‑TTS**        | ✔ 中英双语 ([GitHub][1])                | ✔ README 明示 *“High‑Quality Voice Cloning”* ([GitHub][1]) | ✔ Apache‑2.0 代码可 pip / 本地部署 ([GitHub][1]) | 
| **Kokoro‑TTS**       | ✔ 含普通话 ([Analytics Vidhya][2])      | ✖ 官方文章指出 *“缺乏 voice cloning 能力”* ([Analytics Vidhya][2]) | ✔ 开源权重 ([Analytics Vidhya][2])            | 
| **Orpheus‑TTS**      | ✔ 已发布 zh‑系列模型 ([Hugging Face][3])   | ✔ README 显式列出 *“Zero‑Shot Voice Cloning”* ([GitHub][4])  | ✔ Apache‑2.0 代码 & 权重 ([GitHub][4])        | 
| **F5‑TTS‑V1**        | ✔ 站点写明多语含中文 ([f5tts.org][5])        | ✔ 站点与论文声明零样本克隆 ([f5tts.org][5])                          | ✔ MIT 代码 + 权重 ([GitHub][6])               | 
| **FishSpeech 1.5**   | ✔ 13 语种含中文 ([Reddit][7])            | ✔ “TTS‑Arena #2” 口号即零样本克隆 ([Reddit][7])                  | ✔ 开源权重 ([Reddit][7])                      |
| **XTTS‑v2 / v3**     | ✔ Coqui 官方列入中文 ([Hugging Face][8])  | ✔ Demo 默认零样本克隆 ([Hugging Face][8])                       | ✔ Apache‑2.0 代码 ([Hugging Face][8])       | 
| **ChatTTS**          | ✔ 中英训练 ([GitHub][9])                | ✖ Roadmap 写明“尚未开源 zero‑shot 推理” ([GitHub][9])            | ✔ AGPL‑3.0 代码可本地跑 ([GitHub][9])           | 
| **GPT‑SoVITS‑V3**    | ✔ 跨语种含中文 ([GitHub][10])             | ✔ 5 秒样本零样本 TTS ([GitHub][10])                            | ✔ MIT 代码+Docker ([GitHub][10])            |
| **Index‑TTS**        | ✔ 专门做中文拼音纠错 ([GitHub][11])          | ✔ 标题即 *“Zero‑Shot TTS System”* ([GitHub][11])            | ✔ Apache‑2.0 权重 ([GitHub][11])            | 
| **CosyVoice 2‑0.5B** | ✔ 中文及方言 ([GitHub][12])              | ✔ Cross‑lingual 零样本克隆 ([GitHub][12])                     | ✔ Apache‑2.0 代码 ([GitHub][12])            | 
| **MegaTTS 3**        | ✔ 中英双语 ([GitHub][13])               | **部分支持**：需上传 20 秒音频获得 .npy latent 后可本地克隆 ([GitHub][13])  | ✔ Apache‑2.0 代码；权重开放 ([GitHub][13])       | 
| **Seed‑TTS**         | ✔ 论文与评测集含中文 ([BytedanceSpeech][14]) | ✔ 论文宣称零样本，但**未开源模型** ([GitHub][15])                      | ✖ 仅公开测试集，无法本地部署 ([GitHub][15])            |

---

[1]: https://github.com/SparkAudio/Spark-TTS "GitHub - SparkAudio/Spark-TTS: Spark-TTS Inference Code"
[2]: https://www.analyticsvidhya.com/blog/2025/01/kokoro-82m/ "Kokoro-82M: Compact, Customizable, & Cutting-Edge TTS Model"
[3]: https://huggingface.co/collections/canopylabs/orpheus-multilingual-research-release-67f5894cd16794db163786ba "Orpheus Multilingual Research Release - a canopylabs Collection"
[4]: https://github.com/canopyai/Orpheus-TTS "GitHub - canopyai/Orpheus-TTS: Towards Human-Sounding Speech"
[5]: https://f5tts.org/ "F5-TTS | Free Online AI Text-to-Speech Synthesis Tool"
[6]: https://github.com/SWivid/F5-TTS?utm_source=chatgpt.com "Official code for \"F5-TTS: A Fairytaler that Fakes Fluent and Faithful ..."
[7]: https://www.reddit.com/r/LocalLLaMA/comments/1h6p335/fishspeech_v15_multilingual_zeroshot_instant/?utm_source=chatgpt.com "FishSpeech v1.5 - #2 ranked on TTS-Arena : r/LocalLLaMA - Reddit"
[8]: https://huggingface.co/spaces/coqui/xtts?utm_source=chatgpt.com "XTTS - a Hugging Face Space by coqui"
[9]: https://github.com/2noise/ChatTTS "GitHub - 2noise/ChatTTS: A generative speech model for daily dialogue."
[10]: https://github.com/RVC-Boss/GPT-SoVITS "GitHub - RVC-Boss/GPT-SoVITS: 1 min voice data can also be used to train a good TTS model! (few shot voice cloning)"
[11]: https://github.com/index-tts/index-tts "GitHub - index-tts/index-tts: An Industrial-Level Controllable and Efficient Zero-Shot Text-To-Speech System"
[12]: https://github.com/FunAudioLLM/CosyVoice "GitHub - FunAudioLLM/CosyVoice: Multi-lingual large voice generation model, providing inference, training and deployment full-stack ability."
[13]: https://github.com/bytedance/MegaTTS3 "GitHub - bytedance/MegaTTS3"
[14]: https://bytedancespeech.github.io/seedtts_tech_report/?utm_source=chatgpt.com "Seed-TTS"
[15]: https://github.com/BytedanceSpeech/seed-tts-eval?utm_source=chatgpt.com "BytedanceSpeech/seed-tts-eval - GitHub"
