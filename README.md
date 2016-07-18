### A web scraper for sites renderd by javascript

 - Basen on selenium and phantomJS
 - sse_scraper是中科大软院信息平台的通知抓取器,详见[my blog](xxuan.me/2016-07-16-webscraper.html)
 - bilibili_scraper是哔哩哔哩网站的视频弹幕抓取器, 详见[my blog](http://xxuan.me/2016-07-17-bilibili-scraper.html)
 - bilibili_scraper的可执行文件包正在制作中

---

###Bilibili 弹幕批量下载器使用指南
####Windows
1. 安装python并设置环境变量:
 - 从[官方网站](https://www.python.org/downloads/release/python-2712/)下载python2.7.12安装包(64位系统下载Windows x86-64 MSI Installer, 32位用户下载Windows x86 MSI installer)
 - 记住安装目录地址.右键windows图标, 启动命令行(cmd), 输入:

     ```
 path=%path%;C:\Python27;C:\Python27\Scripts\
     ```
 其中两个地址是默认安装路径, 如果更改了路径需要自行修改

2. 使用pip并安装依赖组件:
 - 重启下cmd, 输入`pip --version` 检查一下是否安装了pip, 默认应该是python自带的, 会返回版本号
 - 安装selenium和beautifulsoup4. 在cmd中输入:

     ```
 pip install selenium, beautifulsoup4 -i https://pypi.douban.com/simple
     ```
 等待安装完毕即可.
 
3. 下载phantomJS
 - 在[官方网站](http://phantomjs.org)下载对应版本并解压, 记住解压地址. (假设解压至C:/phantomjs-2.1.1-widows/)

4. 编辑下载参数
 - [下载本文件](https://github.com/shawnau/webscraper/archive/master.zip) 并解压. 假设下载至C:/webscraper-master/bilibili_scraper.py
 - 用任一文本编辑器打开bilibili_scraper.py, 把倒数第五行的`parameter.driverPath` 之后双引号中的地址改成之前下载的phantomJS的exe文件的地址. 例如 `"C:/phantomjs-2.1.1-widows/bin/phantomjs.exe"` ,注意最好不要使用含中文的地址
 - 将最后一行中双引号中的地址改成需要下载的视频地址, 并检查需要下载的网页样式, 是新式([样例](http://www.bilibili.com/video/av5280311/)) 还是旧式([样例](http://www.bilibili.com/video/av5313786/)), 若为旧式, 请将`"old"` 参数改为`"new"`, 若为新式或者只有一个视频, 则无需变动

5. 启动

 打开cmd, 执行(同第4步的路径, 假设下载至C:/webscraper-master/bilibili_scraper.py)
 
 ```
     python C:/webscraper-master/bilibili_scraper.py
 ```
 下载弹幕会保存至data文件夹下.
