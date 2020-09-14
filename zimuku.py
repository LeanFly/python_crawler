#coding=utf-8

import requests
import re
from lxml import etree  #引入lxml的xpath解析器
import os

#定义 headers
htmlHeather = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36'
}

#搜索地址
searchUrl = 'http://www.zimuku.la/search?q='

#获取本地电影名
path = './'
for file in os.listdir(path):
    #print(files)    #当前目录下所有子文件    
    if os.path.splitext(file)[-1] in ['.mp4' , '.avi' , '.wmv' , '.mkv' , '.mov' , '.rmvb']:
        videoName = os.path.splitext(file)[0]
    # else:
    #     videoName = os.getcwd().split('\\')[-1]
print('获取到本地视频--> %s ' % videoName)
#手动搜索关键词
searchKey = str(input('请输入电影名：'))

res = requests.get(searchUrl + searchKey).text

#获取搜索结果的第一个字幕详情页链接
etreeRes = etree.HTML(res)
resTd = etreeRes.xpath('//td/a/@href')[0]
subDownUrl = 'http://zmk.pw/dld' + resTd.split('detail')[-1]
print('成功搜索到字幕 %s ' % videoName)
resDown = requests.get(subDownUrl).text
DownUrl ='http://zmk.pw' + re.findall(r'rel="nofollow" href="(.*?)" class=', resDown)[0]

#获取下载页面的真是下载地址-->location
downHeader = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Cookie': '__cfduid=df89840e9e87ff0f924b6f636062972361599813451; PHPSESSID=dqopetqvrihq731v7e43pfn6e6',
    'Host': 'zmk.pw',
    'Pragma': 'no-cache',
    'Referer': subDownUrl,
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36'
}
session = requests.Session()
downRes = session.get(url=DownUrl, headers=downHeader, allow_redirects=False)
srtLocation = downRes.headers['location']
print('获取到字幕真实下载地址')
srtName = videoName + '.srt'
print('开始生成字幕 %s' % srtName)
#开始下载
with open(srtName, 'wb') as f:
    f.write(requests.get(srtLocation).content)

print('字幕下载完成')
