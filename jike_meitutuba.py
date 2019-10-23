# -*- coding:UTF-8 -*-

import os
import urllib.request
import re
import random



channel_url = 'https://jike.info/?cid[]=10'

def url_open(url):
    headers = {'cookie': 'express.sid=s%3AC4M0kp7JYiDKTZ8oEnIR2Hc9vBXfG9Kp.anyCM%2Bkn6Uz4djhuRjf69i3UqiLLcsJ4etlF0h4G1cA; io=rxwTbImnK42k_UW8AO3x','User-Agent':'Mozilla/5.0 3578.98 Safari/537.36'}
    req = urllib.request.Request(url=url, headers=headers)
    #创建代理
    proxies = ['183.146.213.157:80', '36.25.243.51:80', '119.41.236.180:8010', '117.28.245.75:80', '47.110.130.152:8080']
    proxy = random.choice(proxies)
    proxy_support = urllib.request.ProxyHandler({'http':proxy})
    opener = urllib.request.build_opener(proxy_support)
    urllib.request.install_opener(opener)
    
    #异常处理
    try:
        response = urllib.request.urlopen(req, timeout=200.0)
    except URLError as e:
        if hasattr(e, 'reason'):
            print('We failed to reach a server.')
            print('Reason:', e.reason)
        elif hasattr(e, 'code'):
            print('The server could\'t fulfill the request.')
            print('Error Code:', e.code)
    else:
        html = response.read().decode('utf-8')

    return html

#采集详情页链接
def url_tid(url):
    print('开始采集详情页地址…')
    html = url_open(url).decode('utf-8')
    a = html.find('"tids":[')
    b = html.find('],"', a)
    tids = html[a+8:b]
    Tids = tids.split(',')
    Detail_url = []
    for tid in Tids:
        detail_url = 'https://jike.info/topic/' + tid
        print(detail_url)
        Detail_url.append(detail_url)
    print('采集到 %d 个详情页' % len(Detail_url))
    return Detail_url

def find_img(url):
    print('开始采集详情页图片…')
    html = url_open(url).decode('utf-8')
    images = []
    a = html.find('<img src="')
    while a != -1:
        b = html.find('" ', a)
        if b != -1:
            images.append(html[a+10:b])
        else:
            b = a + 180
        a = html.find('<img src="', b)
    print('采集到 %d 张图片' % len(images))
    return images

def save_img(folder, images):
    print('开始生成图片…')
    folder_dis = ['\\', '/', '|', ':', '?', '"', '“', '”', '*', '<', '>']
    for img in images:
        img_name = img.split('/')[-1]
        #去除文件夹名字中的非法字符
        for dis in folder_dis:
                while dis in img_name:
                    img_name = img_name.replace(dis, '')
        print(img_name)
        with open(img_name, 'wb') as f:
            try:
                img_content = url_open(img)
            except Exception as e:
                continue
            f.write(img_content)

#获取文件夹命名
def folder_name(url):
    html = url_open(url).decode('utf-8')
    a = html.find('<title>')
    a1 = html.find('</title>', a)
    name = html[a+7:a1]
    #去除文件夹名字中的非法字符
    folder_dis = ['\\', '/', '|', ':', '?', '"', '“', '”', '*', '<', '>']
    for dis in folder_dis:
            while dis in name:
                name = name.replace(dis, '')
    print('开始创建图片文件夹 %s' % name)            
    return name

def Downloader(Folder= 'JIKE_美图'):
    os.mkdir(Folder)
    os.chdir(Folder)

    #采集详情页
    Details = url_tid(channel_url)
    
    #采集图片
    for detail in Details:
        folder = folder_name(detail)
        os.mkdir(folder)
        os.chdir(folder)
        Images = find_img(detail)
        save_img(folder, Images)
        #采集完一个详情页的图片后返回上一层
        os.chdir(os.pardir)
    print('图片下载完成^_^')
    


if __name__ == '__main__':
    Downloader()