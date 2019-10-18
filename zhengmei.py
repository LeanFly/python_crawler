'''
@Description: In User Settings Edit
@Author: your name
@Date: 2019-10-15 15:53:03
@LastEditTime: 2019-10-18 20:05:29
@LastEditors: Please set LastEditors
'''

import urllib.request
import os
import re

page_url = 'http://www.zhengmei.co/'

#创建url打开函数
def url_open(url):
    headers = {'User-Agent':'Mozilla/5.0 3578.98 Safari/537.36'}
    req = urllib.request.Request(url=url, headers=headers)
    response = urllib.request.urlopen(req, timeout=100.0)
    html = response.read()
    return html

#查找页面上的栏目，生成栏目地址列表
def find_cate(page_url):
    print('开始获取栏目……')
    html = url_open(page_url).decode('UTF-8')
    #print(html)
    Cates = []
    #a = html.find('?</span><a href="')
    a = html.find('<ul class="nav-list fl">')
    #print(a)
    a1 = html.find('</ul>')
    b = html[a:a1]
    #print(b)
    b1 = b.find('<a href="')
    while b1 != -1:
        b2 = b.find('/">', b1)
        if b2 != -1:
            print('获取到栏目地址--> %s' % b[b1+9:b2+1])
            Cates.append(b[b1+9:b2+1])
        else:
            b2 = b1 + 50
        b1 = b.find('<a href="', b2)
    #print(Cates)
    #正妹秀是视频,移除该栏目
    Cates.remove('http://www.zhengmei.co/show/')
    print('发现 %d 个栏目' % len(Cates))
    #返回栏目地址列表
    return Cates

#获取所有的详情页,生成列表
def find_details(cate):
    print('开始获取详情页地址……')
    html = url_open(cate).decode('utf-8')
    a = html.find('<div class="page-show"><a href="')
    a1 = html.find('">首页', a)
    page1 = html[a+32:a1]
    b = html.find('下一页</a><a href="')
    b1 = html.find('.html', b)
    c = html[b:b1]
    page_all = c.split('_')[1]
    #获取当前栏目的所有页面
    Cate_pages = []
    for num in range(1, int(page_all)+1):
        if num < 2:
            Cate_pages.append(page1)
        else:
            Cate_pages.append(page1[:-5] + '_' + str(num) + '.html')
    #print(Cate_pages)
    #获取所有的详情页
    detail_pages = []
    for cate_page in Cate_pages:
        html = url_open(cate_page).decode('utf-8')
        a = html.find('张</span><a href="')
        while a != -1:
            a1 = html.find('"  targe', a)
            if a1 != -1:
                print('获取到详情页地址--> %s' % html[a+17:a1])
                detail_pages.append(html[a+17:a1])
            else:
                a1 = a + 100
            a = html.find('张</span><a href="', a1)
    #print(detail_pages)
    print('获取到 %d 个地址' % len(detail_pages))
    #转化为H5链接
    print('开始转换链接地址……')
    detail_h5 = []
    for i in detail_pages:
        page_id = i.split('/')[-1].split('.')[0]
        page_h5 = 'http://m.zhengmei.co/n.php?id=' + page_id
        detail_h5.append(page_h5)
    print('地址转换完成！')
    return detail_h5
    
#获取详情页图片地址
def find_img(page_h5):
    print('开始获取图片地址……')
    html = url_open(page_h5).decode('utf-8')
    #图片地址列表
    images = []
    a = html.find('<!-- .p-content 为内容区域 -->')
    a1 = html.find('<div class="prompt">', a)
    b = html[a:a1]
    b1 = b.find('src="')
    while b1 != -1:
        b2 = b.find('" border=', b1)
        if b2 != -1:
            images.append(b[b1+5:b2])
            print('采集到图片地址--> %s' % b[b1+5:b2] )
        else:
            b2 = b1 + 144
        b1 = b.find('src="', b2)
    #print(images)      
    return images

def save_img(folder, img_src):
    print('开始生成图片……')
    for img in img_src:
        img_name = img.split('/')[-1]
        print('正在生成图片--> %s' % img_name)
        with open(img_name, 'wb') as f:
            #读取超时则跳过
            try:
                img_content = url_open(img)
            except Exception as e:
                continue
            f.write(img_content)

#获取文件夹命名
def folder_name(url):
    #读取超时则跳过
    while True:
        try:
            html = url_open(url).decode('utf-8')
        except Exception as e:
            continue
    a = html.find('<title>')
    a1 = html.find('_', a)
    name = html[a+7:a1]
    #去除文件夹名字中的非法字符
    folder_dis = ['\\', '/', '|', ':', '?', '"', '“', '”', '*', '<', '>']
    for dis in folder_dis:
            while dis in name:
                name = name.replace(dis, '')
    return name

#开始下载
def Downloader(folder='正妹公社'):
    print('下载开始……')
    os.mkdir(folder)
    os.chdir(folder)

    #开始获取栏目地址，返回栏目列表
    Cates = find_cate(page_url)

    #创建栏目文件夹
    for cate in Cates:
        #获取当前栏目的移动端详情页，返回列表
        Details_H5 = find_details(cate)       
        #获取栏目名字，创建文件夹
        Channel_folder = folder_name(cate)
        os.mkdir(Channel_folder)
        os.chdir(Channel_folder)

        

        #创建详情页文件夹
        for detail in Details_H5:
            Detail_folder = folder_name(detail)
            os.mkdir(Detail_folder)
            os.chdir(Detail_folder)
            #获取图片地址
            Images = find_img(detail)
            #写入图片
            save_img(folder, Images)
            #返回上层目录
            os.chdir(os.pardir)
        #返回主目录
        os.chdir(os.pardir)
    print('下载完成，开始欣赏吧！')

if __name__ == '__main__':
    Downloader()
