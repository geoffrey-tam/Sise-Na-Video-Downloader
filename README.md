# Sise-Na-Video-Downloader

广州大学华软软件学院 NA 视频下载器

# 运行方法

`python3 main.py`

# 配置文件



- code 里提供了一个 "config_example" 文件，可作参考
- 第一次运行程序会创建一个新的 "config" 文件
- 其中 
  1. **downloade_path** 为下载路径
  2. **downloader** 为下载器
     - **1** : http 下载，使用 python 自带的库文件
     - **2** : axel 下载，在终端中调用 axel 下载命令，需安装 axel 工具
     - **3** : aria 下载，投送到 aria2 服务器上下载

# 日志文件

程序第一次运行会产生 "history" 文件，里面记录着下载记录，在程序主界面可快捷查看
