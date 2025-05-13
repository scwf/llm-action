# 修复 Hugging Face 401 / Gated Repo 访问报错

> `401 Client Error: Unauthorized` / `You are trying to access a gated repo` 表示当前进程没有携带**有效访问令牌**，或你的账号尚未获批访问受限模型。按照下述步骤操作，即可恢复下载。

---

## 1 常见报错信息
```text
You are trying to access a gated repo.
Make sure to have access to it at https://huggingface.co/<repo>.
401 Client Error … Cannot access gated repo for url …/config.json.
```

---

## 2 根本原因
1. **模型被标记为 Gated（受限）**：发布者要求用户先在对应模型网页上点击 “Request access / Agree & Access”。
2. **本地进程无有效 Token**：缺少 `hf_*****` 访问令牌或令牌过期。

---

## 3 快速解决步骤
### 3.1 在网页申请/确认访问
1. 登录浏览器进入模型主页，如：<https://huggingface.co/canopylabs/orpheus-tts-0.1-finetune-prod>
2. 若页面顶部出现 **Request access** 或 **Agree & Access**，点击并确认。

### 3.2 生成读取令牌并登录
```bash
# 终端内执行
huggingface-cli login          # 按提示粘贴 "read" 令牌，默认token是存在~/.cache/huggingface/token`
```
> 令牌获取：Profile → Settings → **Access Tokens** → New token → 选 **Read** scope。

### 3.3 在脚本或服务中携带令牌
| 场景 | 推荐方式 |
|------|----------|
| 交互 Shell / Notebook | 直接运行 `huggingface-cli login` 一次即可缓存到 `~/.cache/huggingface/token` |
| Docker / systemd | `export HF_TOKEN=<token>` 写入环境变量；或在 `Environment=` 指令中注入 |
| 纯 Python 脚本 | 
```python
from huggingface_hub import login
login(token="<token>")
```

---

## 4 验证下载是否恢复
```bash
python - <<'PY'
from huggingface_hub import hf_hub_download
f = hf_hub_download("canopylabs/orpheus-tts-0.1-finetune-prod", "config.json")
print("文件路径:", f)
PY
```
应当输出本地文件路径而非报错。

---

## 5 安全建议
* 令牌不要硬编码进源码；使用 `.env` / Secrets 管理。
* 可以为长期服务账户单独生成 **过期时间** 的 Token，方便轮换。
* 若 Token 泄露，可随时在 **Access Tokens** 页面点击 **Revoke** 即刻失效。

---

完成以上步骤后，再运行 `python test.py` 等脚本即可顺利拉取受限模型、避免 401 错误。

