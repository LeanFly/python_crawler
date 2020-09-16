#coding=utf-8

import os
import requests
import re
from lxml import etree
from PIL import Image
import time

#定义141jav的搜索API
searchApi = 'https://www.141jav.com/search/?q='
searchKey = str(input('请输入视频编号：'))

searchUrl = searchApi + searchKey

print('正在搜索视频……\n……\n……')


#解析搜索结果
httpHeaders = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36'
}

searchRes = requests.get(url=searchUrl).text

#生成封面
coverName = searchKey + '.jpg'
coverURL = re.findall(r'<img class="image" src="(.*?)" onerror', searchRes)[0]
with open(coverName, 'wb') as f:
    f.write(requests.get(coverURL).content)
#裁剪图片
imgTemp = Image.open(coverName)
imgSize = imgTemp.size
'''
裁剪：传入一个元组作为参数
元组里的元素分别是：（距离图片左边界距离x， 距离图片上边界距离y，距离图片左边界距离+裁剪框宽度x+w，距离图片上边界距离+裁剪框高度y+h）
'''
# 截取图片中一块宽400高540的
x = 400
y = 0
w = 400
h = 540
region = imgTemp.crop((x, y, x+w, y+h))
region.save(coverName)
print('已下载视频 %s 的封面' % searchKey)

#获取磁力链接
magnetUrl = re.findall(r'title="Magnet torrent" href="(.*?)" rel=', searchRes)[0]
with open((searchKey+'.txt'), 'w') as f:
    f.write(magnetUrl)
print('查找到当前视频的磁力下载链接-->\n %s' % magnetUrl)
print('10秒后关闭')

time.sleep(10)