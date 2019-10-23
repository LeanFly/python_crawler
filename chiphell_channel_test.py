# -*- coding:UTF-8 -*-

import urllib.request
import os
import ssl

#https://www.chiphell.com/portal.php?mod=list&catid=102&page=1
channel_url = input('请输入想要下载列表地址：')

#链接打开函数
def url_open(channel_url):
    #定义header
    headers = {'User-Agent':'Mozilla/5.0 3578.98 Safari/537.36'}
    #添加https验证忽略
    context = ssl._create_unverified_context()
    req = urllib.request.Request(url=channel_url, headers=headers)
    response = urllib.request.urlopen(req)
    html = response.read()
    return html

#列表页页码
def Channel_url(channel_url):
    html = url_open(channel_url).decode('utf-8')
    #列表页地址
    channel_pages = []
    
    #获取总页码数
    a = html.find('<span title="共 ')
    b = html.find(' 页', a)
    page_num = html[a+15:b]
    page_num = int(page_num) + 1
    
    for i in range(1, page_num):
        channel_urls = channel_url[:-1] + str(i)
        channel_pages.append(channel_urls)
    return channel_pages

#获取列表页内的详情页地址，生成列表
def Detail(channel_url):
    #channel_pages = Channel_url(channel_url)
    detail_page = []
    #for i in channel_pages:
    html = url_open(channel_url).decode('utf-8')        
    a = html.find('"xs2"><a href="')
    while a != -1:
        b = html.find('" target', a)
        if b != -1:
            detail_href = html[a+15:b]
            detail = 'https://www.chiphell.com/' + detail_href
            #print(detail)
            detail_page.append(detail)
        else:
            b = a + 45
        a = html.find('"xs2"><a href="', b)
    return detail_page
'''
    with open('detail_url.txt', 'w', encoding='utf-8') as f:
        for i in detail_page:
            f.write(i)   

'''
#获取详情页的图片地址
def img_src(detail_url):
    #detail_page = Detail()
    #for detail_url in detail_page:
    html = url_open(detail_url).decode('utf-8')
    imgs = []
    a = html.find('zoomfile="')
    #开始循环查找，如果能找到则 a!=-1
    while a != -1:
        b = html.find('g"', a)
        if b != -1:
            imgs.append(html[a+10:b+1])
        else:
            b = a + 60
        #a的下一次查找从b开始
        a = html.find('zoomfile="', b)
    return imgs

#将获取到的图片地址写入到文件夹
def img_download(folder, imgs):
    for i in imgs:
        #通过分割图片地址获取图片名字
        img_name = i.split('/')[-1]
        print(img_name)
        #打开生成一个图片
        with open(img_name, 'wb') as f:
            #打开图片地址
            img = url_open(i)
            #写入图片
            f.write(img)

#文件夹名字
def Folder(detail_url):
    #detail_page = Detail()
    #for detail_url in detail_page:
    html = url_open(detail_url).decode('utf-8')
    a = html.find('<title>')
    b = html.find(' - ', a)
    folder = html[a+7:b]
    #windows文件夹名字不得包含'\','/','|',':','?','"','“','”','*','<','>'
    folder_dis = ['\\', '/', '|', ':', '?', '"', '“', '”', '*', '**', '<', '>']
    #folder = list(folder)
    #移除特殊字符后生成合规的文件夹名字
    for dis in folder_dis:
        while dis in folder:
            folder = folder.replace(dis, '')
    #folder = ''.join(folder)
    print(folder)
    return folder
        

#图片下载
def Downloader(folders=Folder(channel_url)):
    #创建人物肖像文件夹
    os.mkdir(folders)
    #打开该文件夹
    os.chdir(folders)
    
    #执行Channel_url(channel_url)获取列表页
    channel_pages = Channel_url(channel_url)
    print(len(channel_pages))
    detail_pages = []
    #执行Detail(channel_url)获取详情页链接
    for channel_page in channel_pages:
        detail_page = Detail(channel_page)
        detail_pages += detail_page
    #print(detail_pages)
    #执行Folder(detail_url)获取子文件夹名
    for j in detail_pages:
        folder = Folder(j)
        os.mkdir(folder)
        os.chdir(folder)
        #获取图片地址
        imgs = img_src(j)
        #写入图片
        img_download(folder, imgs)
        #写入完成后返回上一层父目录
        os.chdir(os.pardir)



if __name__ == '__main__':
    Downloader()
    print('下载完成……')



'''
if __name__ == '__main__':
    Detail()
 '''   
