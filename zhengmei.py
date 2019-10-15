'''
@Description: In User Settings Edit
@Author: your name
@Date: 2019-10-14 13:31:42
@LastEditTime: 2019-10-15 14:06:43
@LastEditors: Please set LastEditors
'''
#爬取正妹公社www.zhengmei.co网站详情页图片
import urllib.request
import urllib.parse
import ssl
import os

url = input('请输入网址：')

#定义一个地址打开函数，通过添加header来防网址的爬虫屏蔽
def url_open(url):
    headers = {'User-Agent':'Mozilla/5.0 3578.98 Safari/537.36'}
    req = urllib.request.Request(url=url, headers=headers)
    response = urllib.request.urlopen(req)
    html = response.read()
    #print(url)
    return html

#获取页面地址
def get_page(url):
    html = url_open(url).decode('utf-8')
    a = html.find("<span class='current'>") + 22
    b = html.find('</span>', a)
    return html[a:b]
 
#获取img地址，生成一个列表
def find_imgs(url):
    html = url_open(url).decode('utf-8')
    img_src = []
    a = html.find('src="http://www.zhengmei.co') + 27
    a1 = html.find('"', a)
    src ='http://www.zhengmei.co' + html[a:a1]
    img_src.append(src)
    return img_src

def save_imgs(folder, img_src):
    for i in img_src:
        img_name = i.split('/')[-1]
        print(img_name)
        with open(img_name, 'wb') as f:
            img = url_open(i)
            f.write(img)

#定义下载函数
def Img_download(folder=url.split('/')[-1][:4], pages = 20):    #(文件夹名字从url地址中获取)
    #folder = url.split('/')[-1][:4]
    os.mkdir(folder)
    os.chdir(folder)
    page_num = int(get_page(url))
    for i in range(pages):
        if i < 1:
            page_url = url
        else:
            page_nums = page_num + i
            page_url = url[:-5] + '_' + str(page_nums) + '.html'
        img_src = find_imgs(page_url)
        save_imgs(folder, img_src)


if __name__ == '__main__':
    Img_download()
    print('下载完成')