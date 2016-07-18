### Bilibili 弹幕批量下载器

 - Based on selenium and phantomJS
 - 批量下载b站弹幕, 只需提供其中1p的av号, 支持批量下载多部番组

---

###使用指南
####Windows
1. 安装python并设置环境变量:
 - 从[官方网站](https://www.python.org/downloads/release/python-2712/)下载python2.7.12安装包(64位系统下载Windows x86-64 MSI Installer, 32位用户下载Windows x86 MSI installer)
 - 记住安装目录地址.右键windows图标, 启动命令行(cmd), 输入:

     ```
 path=%path%;C:\Python27;
 path=%path%;C:\Python27\Scripts\;
     ```
 其中两个地址是默认安装路径, 如果更改了路径需要自行修改

2. 使用pip并安装依赖组件:
 - 重启下cmd, 输入`pip --version` 检查一下是否安装了pip, 默认应该是python自带的, 会返回版本号
 - 安装selenium和beautifulsoup4. 在cmd中输入:

     ```
 pip install selenium -i https://pypi.douban.com/simple
 pip install beautifulsoup4 -i https://pypi.douban.com/simple
     ```
 等待安装完毕即可.
 
3. 下载phantomJS
 - 在[官方网站](http://phantomjs.org)下载对应版本并解压, 记住解压地址. (假设解压至C:/phantomjs-2.1.1-widows/)

4. 编辑config.json
 - [下载本文件](https://github.com/shawnau/bilibili_scraper/archive/master.zip) 并解压
 - 用任一文本编辑器打开config.json, 参数如下:
     - `system` 键可填"windows", "osx", "linux", 对应操作系统
     - `phantomJS_path` 键填写下载的phantomJS可执行文件位置. 样例:
         
         ```python
         # osx下: 
         "phantomJS_path": "/Users/Shawn/Downloads/phantomjs-2.1.1-macosx/bin/phantomjs",
         # windows下, 注意添加exe后缀
         "phantomJS_path": "C:/phantomjs-2.1.1-windows/bin/phantomjs.exe",
         ```
     - `video_list` 键即为需要下载的番组的av号. 填入av号后检查需要下载的网页样式, 是新式([样例](http://www.bilibili.com/video/av5280311/)) 还是旧式([样例](http://www.bilibili.com/video/av5313786/)), 若为旧式, 请将`"old"` 参数改为`"new"`, 若为新式或者只有一个视频, 则无需变动.本栏可以自行增删行数实现批量下载不同番组, 除最后一行外不要忘记添加逗号.

5. 启动

 打开cmd, 执行(假设下载至D:/bilibili_scraper-master/bilibili_scraper.py)
 
 ```python
     # 先切换到d盘 
     d:
     # 再进入下载器文件夹
     cd webscraper-master
     # 最后运行脚本
     python bilibili_scraper.py
 ```
 下载弹幕会保存至data文件夹下.

6. 注意
 - 不要使用包含中文的文件路径
