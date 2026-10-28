# Day 2: 从源码编译带 CUDA 加速的 OpenCV (C++ & Python)

## 1. 准备工作：安装底层依赖与 CUDA 环境
为了让 OpenCV 支持 NVIDIA 显卡加速，并且能够被 C++ 和 Python 调用，我首先补齐了系统级的工具链：
- **C++ 编译工具**：安装了 `build-essential`、`cmake`、`git` 等。
- **CUDA Toolkit**：安装了 CUDA 12.8（通过 `nvcc --version` 验证成功）。
- **cuDNN 库**：安装了 cuDNN 9.27（通过 `find /usr -name "libcudnn.so*"` 确认底层动态库已就位）。
- **图像/视频依赖**：安装了 `libgtk-3-dev`, `libavcodec-dev`, `libv4l-dev` 等一堆依赖包。
*(避坑：Ubuntu 24.04 中 `libtbb2` 被替换为了 `libtbbmalloc2`，`libdc1394-22-dev` 改名为了 `libdc1394-dev`)*

## 2. 为什么必须“从源码编译”？
以前在 Windows 下都是直接下载 `.exe` 安装，这次为什么要下载上百兆的源码自己编译？
- **硬件差异大**：我的显卡是最新的 RTX 5070（Blackwell 架构，计算能力 sm_120）。现成的 OpenCV 安装包大多是用老架构编译的，无法发挥新显卡的全部性能。
- **量身定制**：通过自己编译，我可以在 CMake 中明确指定 `-D CUDA_ARCH_BIN=12.0`，让编译器专门为我的显卡生成底层机器码（0和1），实现真正的硬件级加速。

## 3. 编译过程与疯狂踩坑

### 阶段一：CMake 配置
使用 `cmake` 命令生成 `Makefile`。一开始直接复制了网上的教程，遇到了几个坑：
1. **路径错误**：因为多行命令中的 `\` 后带了一个空格，导致 CMake 找不到 `CMakeLists.txt`。解决：把参数合并成一整行执行。
2. **OpenJPEG 冲突**：由于 Anaconda 环境里有残缺的 OpenJPEG 库，导致 CMake 报错。解决：在命令中加上 `-D WITH_OPENJPEG=OFF`，直接绕过。

### 阶段二：开始 `make` 编译（踩坑重灾区）
执行 `make -j$(nproc)` 满负荷编译，结果遇到了各种 CUDA 源码报错：
1. **cudaarithm 模块报错**：在 `minmax.cu` 报错。推测是旧版源码对新架构支持不好。
   *解决*：加上 `-D BUILD_opencv_cudaarithm=OFF` 禁用它。
2. **cudaimgproc 模块报错**：报 NPP 库函数接口参数不匹配（`int*` 变成了 `size_t*`）。
   *解决*：放弃旧版，重新拉取 **OpenCV 4.12.0** 源码，新版本修复了这个接口。
3. **cudalegacy 模块报错**：报 `cuda::minMaxLoc` 找不到，因为这是官方弃用的遗留模块。
   *解决*：加上 `-D BUILD_opencv_cudalegacy=OFF` 禁用它。
4. **make: getcwd 报错**：非常奇葩的错误，因为之前 `rm -rf` 导致 build 文件夹底层状态损坏。
   *解决*：重新建一个干净的 build 文件夹，重跑 CMake。
5. **中途 OOM 内存爆炸**：满负荷 `-j` 编译极其吃内存。
   *解决*：改用 `make -j4`，牺牲一点速度换取稳定性。

## 4. 最终编译与安装
经历了多次 `make clean` 和重新配置，最终看到了神圣的 `[100%] Built target opencv_python3`。
- 执行 `sudo make install` 安装到系统。
- 执行 `sudo ldconfig` 刷新系统动态链接库。

## 5. 验证成功

### Python 端验证
在虚拟环境中验证：
```python
import cv2
print(cv2.__version__)          # 输出 4.12.0
print(cv2.cuda.getCudaEnabledDeviceCount()) # 输出 1 (代表成功识别显卡)
