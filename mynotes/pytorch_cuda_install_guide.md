
# ✅ 安装支持 CUDA 的 PyTorch（含本地 CUDA 检查）

适用于需要使用 GPU 的 PyTorch 开发环境（Windows / Linux / macOS）。

---

## 🔹 第 1 步：查询本地 CUDA 版本

### 方法 1：查看驱动支持的 CUDA 版本

在终端执行：

```bash
nvidia-smi
```

输出示例：

```
+-----------------------------------------------------------------------------+
| NVIDIA-SMI 537.13       Driver Version: 537.13       CUDA Version: 12.2     |
+-----------------------------------------------------------------------------+
```

此处的 `CUDA Version` 是你的驱动支持的最高版本。

---

### 方法 2：查看是否安装 CUDA Toolkit

```bash
nvcc --version
```

输出示例：

```
Cuda compilation tools, release 11.8, V11.8.89
```

说明本地安装了 CUDA Toolkit 11.8。

---

## 🔹 第 2 步：打开 Anaconda PowerShell Prompt

使用 Anaconda 自带终端（推荐）以确保环境配置正确。

---

## 🔹 第 3 步：创建 Conda 虚拟环境

```bash
conda create -n your-env-name -y python=3.12
```

- `your-env-name` 可替换为任意你喜欢的环境名。
- `-y` 表示自动确认安装。

---

## 🔹 第 4 步：激活 Conda 环境

```bash
conda activate your-env-name
```

---

## 🔹 第 5 步：访问 PyTorch 官网获取安装命令

前往官网安装引导页面：

👉 https://pytorch.org/get-started/locally/

按以下选项选择并复制生成的安装命令：

- **PyTorch Build**：Stable
- **Your OS**：Windows / Linux / macOS
- **Package**：pip
- **Language**：Python
- **Compute Platform**：根据你的显卡驱动选择（如 CUDA 11.8）

网站将为你生成类似这样的命令：

```bash
pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```

将生成的命令粘贴到终端中运行。

---

## 🔹 第 6 步：验证 PyTorch 是否正确安装并识别 GPU

```bash
python
```

进入 Python 解释器后输入：

```python
import torch
print("PyTorch version:", torch.__version__)
print("CUDA available:", torch.cuda.is_available())
print("GPU name:", torch.cuda.get_device_name(0) if torch.cuda.is_available() else "No GPU detected")
```

---

## 🔹 附加操作：管理 Conda 环境

- 查看所有 Conda 环境：
  ```bash
  conda env list
  ```

- 删除某个环境：
  ```bash
  conda remove --name your-env-name --all
  ```

---

## ✅ 小结

| 步骤 | 内容 |
|------|------|
| ①    | 查看 CUDA 驱动支持版本 |
| ②    | 创建并激活 Conda 虚拟环境 |
| ③    | 前往 PyTorch 官网获取对应命令 |
| ④    | 安装 PyTorch + GPU 支持 |
| ⑤    | 验证 PyTorch GPU 可用性 |

---
