## 摘要
本文档演示在 **WSL 2** 环境中
1. 配置网络代理（启用 *mirrored networking*）并
2. 安装 **Miniforge3**（conda‑forge 发行版）的一步到位脚本。配置思路同样适用于 Ubuntu、Debian 等发行版。

---

## 一、启用 *mirrored networking* 让 WSL 直连 Windows 代理

WSL 2 从 2023 年起支持 **mirrored networking**，启用后 Linux 子系统与 Windows 主机可以互相通过 `localhost`（`127.0.0.1`）进行 TCP/UDP 访问，无需再查找虚拟网关 IP，也不用修改 CLI 配置。操作步骤如下：

1. **编辑 `.wslconfig`**（位于 Windows 用户主目录, %USERPROFILE%\.wslconfig）：  
   ```ini
   [wsl2]
   networkingMode=mirrored
   ```
2. **重启 WSL**：在 PowerShell 运行  
   ```powershell
   wsl --shutdown
   ```  
   然后重新打开任意发行版终端。
3. **验证**：  
   ```bash
   curl -I http://127.0.0.1:33210
   ```  
   如果能访问到 Windows 侧代理端口，则配置成功，后续可直接  
   ```bash
   export http_proxy=http://127.0.0.1:33210
   export https_proxy=$http_proxy
   export all_proxy=socks5://127.0.0.1:33211
   ```  
   并写入 `~/.bashrc` 永久生效。

> **注意**  
> • *mirrored networking* 仍处于预览阶段；如遇 VPN / Endpoint Security 软件冲突，可改回 `networkingMode=nat`。  
> • 代理程序需监听 `127.0.0.1`（默认即可）或 `0.0.0.0`；不影响使用。

## 二、安装 Miniforge3（含 mamba）

### 1. 下载最新安装脚本

```bash
cd ~
curl -fsSLO https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-Linux-x86_64.sh
```
`-f` 失败即退、`-sS` 静默+显示错误、`-L` 自动跟随跳转、`-O` 按远端文件名保存。([conda-forge.org](https://conda-forge.org/download/?utm_source=chatgpt.com))

### 2. 交互安装（推荐）

```bash
bash Miniforge3-Linux-x86_64.sh
# 全程按回车，末尾选择 yes 让安装器写入 ~/.bashrc
```
Miniforge3 官方脚本体积约 80 MB，下载列表可在 condaforge 页面查看。([github.com](https://github.com/conda-forge/miniforge?utm_source=chatgpt.com), [conda-forge.org](https://conda-forge.org/miniforge/?utm_source=chatgpt.com))

### 3. 静默安装示例

```bash
bash Miniforge3-Linux-x86_64.sh -b -p $HOME/miniforge3
source "$HOME/miniforge3/etc/profile.d/conda.sh"
conda init bash   # 写入 PATH
```

### 4. 验证

```bash
conda --version   # conda 24.x
mamba --version   # mamba 1.x
```
若能正确输出版本且 `conda info` 显示 `base *` 环境，则安装成功。([conda-forge.org](https://conda-forge.org/download/?utm_source=chatgpt.com))

---

## 三、常见问题速查

| 现象 | 诊断与解决 |
| --- | --- |
| `curl: Network is unreachable` | WSL 内使用了 `0.0.0.0` 或 `127.0.0.1` 但未启用 mirrored；改用宿主网关 IP。([learn.microsoft.com](https://learn.microsoft.com/en-us/windows/wsl/networking?utm_source=chatgpt.com)) |
| `conda` 命令不生效 | 忘记 `source ~/.bashrc` 或未执行 `conda init bash`。([conda-forge.org](https://conda-forge.org/download/?utm_source=chatgpt.com)) |

---

**至此，WSL 里的代理与 Miniforge3 已配置完毕，祝使用顺利！**

