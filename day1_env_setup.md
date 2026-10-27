# 环境配置 (Day 1)

## 1. 显卡与驱动
- 电脑：Lenovo Legion Y9000P (RTX 5070)
- 安装过程：因N卡冲突，在GRUB添加 `nomodeset` 安装系统，后通过 `sudo ubuntu-drivers autoinstall` 成功安装驱动。
- 验证：`nvidia-smi` 显示 CUDA Version 13.2。

## 2. Anaconda 安装
- 使用清华源下载 Anaconda3-2026.07-1。
- 换源：配置了 conda 的清华镜像源。
- 环境隔离：创建了 `pytorch_env` (Python 3.10) 虚拟环境。

## 3. PyTorch GPU 环境
- 安装命令：`pip install torch==2.7.1 ...`
- 验证结果：
  - torch版本：2.7.1+cu128
  - `torch.cuda.is_available()` 输出：True
- 心得：意识到环境隔离的重要性，明白了 `pip` 和 `wget` 的区别。
