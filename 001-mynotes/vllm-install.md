# vLLM 0.8.5 安装注意事项速览

> 本文档汇总了在 **Linux/WSL GPU 环境** 中安装 vLLM 0.8.5 的版本兼容、依赖管理与常见坑，供快速参考。

---

## 1  先决条件
1. **Python ≥ 3.9**（官方 wheel 提供 cp39–cp312）。
2. **显卡驱动**：
   - NVIDIA 535+（CUDA 11.8/12.x）
   - AMD ROCm 6.1+ 或 Intel oneAPI 2024.2（若走 ROCm/oneAPI）。
3. **Linux 发行版**；Windows 需 WSL 2/Docker，多 GPU 及 TPU 仍仅 Linux 支持。

---

## 3 推荐安装流程
vLLM 0.8.5 自带 PyTorch 依赖，**缺省情况下只要一条命令**：

```bash
# CPU 或 CUDA 12.4（默认）
pip install vllm==0.8.5            # 自动获取 torch‑2.7.0 + 对应 CUDA
```

如果你需要 **CUDA 11.8 / 12.1**，选择带后缀的官方 wheel：

```bash
# CUDA 11.8
pip install https://github.com/vllm-project/vllm/releases/download/v0.8.5/\
            vllm-0.8.5+cu118-cp312-abi3-manylinux1_x86_64.whl

# CUDA 12.1
pip install https://github.com/vllm-project/vllm/releases/download/v0.8.5/\
            vllm-0.8.5+cu121-cp312-abi3-manylinux1_x86_64.whl
```

pip 会自动解析依赖，拉取 **`torch==2.7.0+cu118`** 或 **`+cu121`** 等**一致**的 CUDA 轮子，无需人工干预。

### 若已预装其他 CUDA Torch（可选）
- 想保留现有 `torch` 版本：
  ```bash
  pip install vllm==0.8.5 --no-deps   # 跳过依赖解析
  ```
- 或者在同一行里显式声明：
  ```bash
  pip install torch==2.7.0+cu118 vllm==0.8.5+cu118 \
       --extra-index-url https://download.pytorch.org/whl/cu118
  ```

> **简而言之：** 普通用户直接 `pip install vllm==0.8.5`，高阶用户才需要 `--no-deps` / 自定义 Torch。

---

## 4 常见坑与解决
| 症状 | 原因 | 解决方案 |
|------|------|-----------|
| **GPU 不可见 / `CUDA not available`** | vLLM 自动安装了 CPU 版 Torch | 先卸载 `torch*`, 重装 CUDA 轮子 → `pip install vllm --no-deps` |
| **`RuntimeError: version mismatch with torch`** | 预装 Torch 版本 < 2.7 | 升级到 2.7.0，与 vLLM 0.8.5 对齐 |
| **pip 重新下载 Torch 覆盖原版本** | 没有 `--no-deps` 或同一行显式指明 Torch | 按 3 节命令执行 |
| **WSL 无显卡** | 驱动或 GPU‑P 版本过旧 | `wsl --update` + 安装 545+ Windows 显卡驱动 |
| **编译 flash‑attn 失败** | 源码安装未装 GCC 11+/ninja | 直接用预编译 wheel 或安装 build deps |

---

## 5 安装后验证
```bash
python - <<'PY'
import torch, vllm
print('torch :', torch.__version__)
print('cuda  :', torch.version.cuda, torch.cuda.is_available())
print('vllm  :', vllm.__version__)
PY
```
输出显示 `cuda  : 11.8 True`（或 12.x）且版本对应即成功。

---

## 6 附加提示
- **多 CUDA 并存**：用 `-p ~/.local/vllm-cu118` 等独立前缀隔离不同 CUDA 版本。
- **镜像源**：国内网络建议先 `pip download --resume-retries`，或使用 TUNA/SJTU PyTorch 镜像。
- **源码编译**：仅当需自定义优化或 Torch ≤ 2.6 时才必须；步骤见官方 *Build from source*。

