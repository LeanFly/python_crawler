# coding：utf8

import os
import urllib.request
import json
import re

#定义一个UrlOpen函数
def UrlOpen(url, headers):
    headers = {'User-Agent':'Mozilla/5.0 3578.98 Safari/537.36'}
    req = urllib.request.Request(url=url, headers=headers)
    res = urllib.request.urlopen(req, timeout=2000)
    rContent = res.read()
    return rContent


#定义下载函数
def ImgDownloader():
    #定义图片链接前缀
    imgFull = 'https://h5.crazyccy.com/appgame/v615/resource/'

    #定义图片的url列表
    imgList = [{
        "url": "hotAssets/onlytestforload.png",
			"type": "image",
			"name": "onlytestforload_png"
		}, {
			"url": "hotAssets/dpk_recrewardbg.png",
			"type": "image",
			"name": "dpk_recrewardbg_png"
		}, {
			"url": "hotAssets/dpk_greenbtnbg.png",
			"type": "image",
			"name": "dpk_greenbtnbg_png"
		}, {
			"url": "hotAssets/dpk_checkbox.png",
			"type": "image",
			"name": "dpk_checkbox_png"
		}, {
			"url": "hotAssets/dpk_checkboxbg.png",
			"type": "image",
			"name": "dpk_checkboxbg_png"
		}]


    #生成图片地址列表
    imgUrl = []
    for i in imgList:
        if i['type'] == 'image':
            imgUrl.append(imgFull + i['url'])

    print(imgUrl)

    #开始下载图片
    for i in imgUrl:
        imgName = i.split('/')[-1]
        print('downloading img --》 %s' % imgName)
        with open(imgName, 'wb') as f:
            #f.write(urllib.request.urlopen(urllib.request.Request(i)).read())
            try:
                imgContent = UrlOpen(i)
            except Exception as error:
                continue
            f.write(imgContent)

if __name__ == '__main__':
    ImgDownloader()