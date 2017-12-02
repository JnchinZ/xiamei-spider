宅男女神的爬虫
=======

爬取这个网址的图片：https://www.nvshens.com

以夏美酱为例

爬去图片之前先配好python3环境；
需要的包：

 - requests
 - urllib

直接文件运行xiamei.py即可。
脚本最后的代码A是直接用代码下载图片，所以下载的比较慢；
如果想快点下载可以使用代码B先把图片的url下载到all_urls.txt的文件中，然后把里面的所有url丢到迅雷里去下载，这样可能会快点吧。
