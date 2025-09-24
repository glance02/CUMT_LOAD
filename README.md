# CUMT_LOAD

## 打包方式
`python -m nuitka --onefile --windows-disable-console --windows-icon-from-ico=planet.ico --include-data-file=02.png=02.png cumt.py`

用 Python 方式调用 Nuitka 编译器。

`--onefile`
打包为单个 exe 文件（所有依赖都封装进一个文件，方便分发）。

`--windows-icon-from-ico=planet.ico`
指定生成的 exe 文件图标为 planet.ico，必须是标准的 ico 格式。

`--include-data-file=02.png=02.png`
把当前目录下的 02.png 文件包含进 exe，运行时也能访问。前面是源文件，后面是打包后存放的路径（这里保持不变）。

`--windows-disable-console`取消运行程序时弹出的黑框