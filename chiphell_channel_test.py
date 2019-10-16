'''
@Description: In User Settings Edit
@Author: your name
@Date: 2019-10-16 17:23:03
@LastEditTime: 2019-10-16 20:04:46
@LastEditors: Please set LastEditors
'''


import urllib.request
import os
import ssl

channel_url = 'https://www.chiphell.com/portal.php?mod=list&catid=102&page=1'

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
def Detail():
    channel_pages = Channel_url(channel_url)
    detail_page = []
    for i in channel_pages:
        html = url_open(i).decode('utf-8')        
        a = html.find('"xs2"><a href="')
        while a != -1:
            b = html.find('" target', a)
            if b != -1:
                detail_href = html[a+15:b]
                detail = 'https://www.chiphell.com/' + detail_href
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
def img_src(detail_page):
    detail_page = Detail()
    for detail_url in detail_page:
        html = url_open(detail_url).decode('utf-8')
        imgs = []
        a = html.find('zoomfile="')
        #开始循环查找，如果能找到则 a!=-1
        while a != -1:
            b = html.find('.jpg', a)
            if b != -1:
                imgs.append(html[a+10:b+4])
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
    detail_page = Detail()
    for detail_url in detail_page:
        html = url_open(detail_url).decode('utf-8')
        a = html.find('<title>')
        b = html.find(' - 摄影作品', a)
        folder = html[a+7:b]
        os.mkdir(folder)

#图片下载
def Downloader(folder='人物肖像' ):
    #创建文件夹
    os.mkdir(folder)
    #打开文件夹
    os.chdir(folder)
    
    #Channel_url(channel_url)
    #获取详情页链接
    detail_page = Detail()
    
    #获取图片链接
    images = img_src(detail_page)

    #执行图片下载
    img_download(folder, images)

    

if __name__ == '__main__':
    Downloader()
    print('下载完成……')



'''
if __name__ == '__main__':
    Detail()
 '''   