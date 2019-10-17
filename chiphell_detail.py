'''
@Description: In User Settings Edit
@Author: your name
@Date: 2019-10-16 16:02:53
@LastEditTime: 2019-10-17 17:41:53
@LastEditors: Please set LastEditors
'''
import urllib.request
import os
import ssl


detail_url = input('请输入想要保存图片的详情页地址：')

#定义链接的打开函数，防止https证书问题、header问题
def url_open(url):
    headers = {'User-Agent':'Mozilla/5.0 3578.98 Safari/537.36'}
    #添加忽略https证书验证
    context = ssl._create_unverified_context()
    req = urllib.request.Request(url=url, headers=headers)
    response = urllib.request.urlopen(req)
    html = response.read()
    #print(url)
    return html

#通过循环方式将页面图片地址生成一个列表
def img_src(detail_url):
    html = url_open(detail_url).decode('utf-8')
    imgs = []
    #a = html.find('zoomfile="')
    #img_types = ['.jpg', '.jpeg', '.png', '.gif', '.webp', '.bmp', '.raw']
    #开始循环查找，如果能找到则 a!=-1
    #for img_type in img_types:
    a = html.find('zoomfile="')
    while a != -1:        
        b = html.find('g"', a)
        if b != -1:
            imgs.append(html[(a+10):b+1])
            print(imgs)
        else:
            b = a + 60  #下一次的b从上一次的url结束位置开始
        #a的下一次查找从b开始
        a = html.find('zoomfile="', b)
    return imgs
        #print(imgs)

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
def folder():
    html = url_open(detail_url).decode('utf-8')
    a = html.find('<title>')
    b = html.find(' - 摄影作品', a)
    folder = html[a+7:b]
    #folder = list(folder)
    #windows文件夹名字不得包含'\','/','|',':','?','"','“','”','*','<','>'
    folder_dis = ['\\', '/', '|', ':', '?', '"', '“', '”', '*', '<', '>']
    #folder = list(folder)
    for dis in folder_dis:
        while dis in folder:
            folder = folder.replace(dis, '')
    #移除特殊字符后重新生成文件夹名字
    #folder = ''.join(folder)
    print(folder)
    return folder

#图片下载
def Downloader(folder=folder()):
    #创建文件夹
    os.mkdir(folder)
    #打开文件夹
    os.chdir(folder)
    #执行图片地址获取函数生成图片列表
    images = img_src(detail_url)
    #执行图片下载函数
    #for i in images:
    img_download(folder, images)

if __name__ == '__main__':
    Downloader()
    print('下载完成……')

