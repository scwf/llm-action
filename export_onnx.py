from transformers import AutoModel # 或者从 timm 导入相应的模型类
import torch

# 模型名称或路径 (Hugging Face Hub 上的)
model_name_or_path = "timm/hiera_base_224.mae"

# 1. 加载模型 (确保已安装 transformers 或 timm)
# 对于 timm 模型，可能像这样：
# import timm
# model = timm.create_model(model_name_or_path, pretrained=True)
# model.eval()

# 或者如果它是标准的 Hugging Face Transformers 模型：
try:
    model = AutoModel.from_pretrained(model_name_or_path)
    model.eval() # 设置为评估模式
except Exception as e:
    print(f"Error loading model with AutoModel: {e}")
    print("Attempting with timm...")
    import timm
    try:
        # Hiera 在 TIMM 中的名称可能不完全是 "timm/hiera_base_224.mae"
        # 你可能需要找到它在 TIMM 中的确切名称，例如 'hiera_base_mae.hvga_224_in1k'
        # 或者，如果 `timm/hiera_base_224.mae` 本身就是一个可以直接被 `timm.create_model` 识别的 HF 路径
        model_timm_name = 'hiera_base_224.mae' # 这可能需要确认
        # 尝试从 HF Hub 加载 TIMM 模型，如果 TIMM 支持这种方式
        if model_name_or_path.startswith('timm/'):
             model_timm_name = model_name_or_path.split('/')[-1]

        # 这里的模型名称可能需要根据 TIMM 的实际命名规则调整
        # 例如 hiera_base.mae_in1k_224 (Hiera Base MAE pre-trained on ImageNet-1k at 224x224)
        # 查阅 Hiera 在 TIMM 中的具体模型名非常重要
        # 假设模型在 TIMM 中注册的名字是 'hiera_base_mae_224' (这只是一个猜测)
        # model = timm.create_model('hiera_base_mae_224', pretrained=True, checkpoint_path=model_name_or_path) # 如果直接加载HF路径
        
        # 更通用的方式是，如果 transformers 库能处理 TIMM 模型
        from transformers import AutoImageProcessor
        processor = AutoImageProcessor.from_pretrained(model_name_or_path)
        model = AutoModel.from_pretrained(model_name_or_path)
        model.eval()

    except Exception as e_timm:
        print(f"Error loading model with timm: {e_timm}")
        exit()


# 2. 创建一个虚拟输入 (dummy input)
# Hiera 通常输入是 (batch_size, channels, height, width)
# 这里的 224 来自模型名称 hiera_base_224.mae
batch_size = 1
dummy_input = torch.randn(batch_size, 3, 224, 224)

# 3. 导出到 ONNX
onnx_model_path = "hiera_base_224_mae.onnx"
try:
    torch.onnx.export(
        model,
        dummy_input,
        onnx_model_path,
        input_names=['input'],      # 输入名
        output_names=['output'],    # 输出名
        dynamic_axes={'input': {0: 'batch_size'}, 'output': {0: 'batch_size'}}, # 动态轴
        opset_version=16 # 或更高版本，根据模型需要
    )
    print(f"Model successfully exported to {onnx_model_path}")
except Exception as e:
    print(f"Error during ONNX export: {e}")
    print("Make sure the model is correctly loaded and the dummy input matches the model's expected input.")