# CUMT_LOAD

## 环境配置

此处仅展示conda管理下的python配置

1. 创建环境，`conda create -n load python=3.13`

2. 激活环境，`conda activate load`

3. 安装所需库，`pip install -r requirements.txt`

## 打包方式

`python -m nuitka --onefile --windows-console-mode=disable --windows-icon-from-ico=planet.ico --include-data-file=02.png=02.png cumt.py`

用 Python 方式调用 Nuitka 编译器。

`--onefile` 打包为单个 exe 文件（所有依赖都封装进一个文件，方便分发）。

`--windows-icon-from-ico=planet.ico` 指定生成的 exe 文件图标为 planet.ico，必须是标准的 ico 格式。

`--include-data-file=02.png=02.png` 把当前目录下的 02.png 文件包含进 exe，运行时也能访问。前面是源文件，后面是打包后存放的路径（这里保持不变）。

`--windows-disable-console`取消运行程序时弹出的黑框

## 修改部分

如果想要把提示部分的图片改成自己想要的图片，就自己找一张图片放在当前目录下，并且将名字改成`02.png`（别问为什么是02，因为02天下第一喵）。

打包的软件的图标是`planet.ico`，这个得是ico文件。你可以用自己的图片然后将名字改成`planet.ico` 。

因为这个是无图形界面的代码，所以不发布已经打包好的exe文件。