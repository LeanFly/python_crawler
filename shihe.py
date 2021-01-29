#coding=utf-8

import os
import re
import requests
import time
import random


if  os.path.exists('六年级'):
    os.chdir('六年级')
else:
    os.mkdir('六年级')
    os.chdir('六年级')

apiUrl = "http://shihe.huijiaoyun.com/notice/sh/sky.html"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.96 Safari/537.36 Edg/88.0.705.53"
}
#当前六年级，十三周课程

res = requests.get(url=apiUrl, headers=headers)
res.encoding='utf-8'
res = res.text
res = res.replace('\r\n', '')
classSix = re.findall(r"<!--六年级 begin-->(.*?)<!--六年级 end-->", res)
print("获取到总课程共 %d 周" % len(classSix))
ep = 1
# 开始获取课程并下载
for i in classSix:
    classname1 = re.findall(r'class="col3"><strong>(.*?)</strong>', i)
    classname2 = re.findall(r'class="col4"><strong title="(.*?)"', i)
    classapi = re.findall(r'<a href="(.*?)"', i)

    for j in classapi:
        classname = str(ep) + classname1[classapi.index(j)] + classname2[classapi.index(j)].replace('？', '').replace('?', '').replace('*', '-') + '.mp4'
        if os.path.isfile(classname):
            continue
        else:
            print('开始下载课程 %s ' % classname)
            with open(classname, 'wb') as f :
                f.write(requests.get(j).content)
            time.sleep(random.randint(5,15))

    ep = ep + 1
print('下载完毕')