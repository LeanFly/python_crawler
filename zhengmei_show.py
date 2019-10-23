# -*- coding:UTF-8 -*-


import urllib.request
import re
import os


channel_url = 'http://www.zhengmei.co/show/index.html'

#创建url打开函数
def url_open(url):
    headers = {'User-Agent':'Mozilla/5.0 3578.98 Safari/537.36'}
    req = urllib.request.Request(url=url, headers=headers)
    #response = urllib.request.urlopen(req, timeout=100.0)

    try:
        response = urllib.request.urlopen(req, timeout=100.0)
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

#创建栏目页列表
def channel_page(url):
    
    channel_page = []
    html = url_open(url)
    a = html.find('下一页</a>')
    a1 = html.find('尾页</a>', a)
    b = html[a:a1]
    page_num = b.split('/')[-1].split('_')[-1].split('.')[0]

    for num in range(1, int(page_num)+1):
        if num < 2:
            channel_page.append(channel_url)
        else:
            channel_page.append(channel_url[:-5] + '_' + str(num) + '.html')
    return channel_page

#创建详情页列表
def detail_page(url):
    #detail_page = []
    html = url_open(url)
    a = html.find('<ul class="detail-list">')
    a1 = html.find('</ul>', a)
    b = html[a:a1]
    p = r'</span><a href="([^"]+\.html)"'
    detail_page = re.findall(p, b)
    print('发现 %d 个视频页面'  % len(detail_page))
    return detail_page

def find_video(url):
    html = url_open(url)
    a = html.find('<div class="con-5-con mt20">')
    a1 = html.find('<div class="con3-sa-mian">', a)
    a2 = html[a:a1]
    a3 = a2.find('src="')
    a4 = a2.find('" ', a3)
    source = a2[a3+5:a4]
    print('发现视频链接-> %s' % source)
    b = html.find('<div class="con-5-l"><span>')
    b1 = html.find('</span>', b)
    video_name = html[b+27:b1] + '.mp4'
    print(video_name)
    print('开始下载-> %s' % video_name)
    urllib.request.urlretrieve(source, video_name)

 
def Video_downloader(folder='show'):
    if not os.path.exists(folder):
        os.mkdir(folder)
        os.chdir(folder)
    else:
        os.chdir(folder)
        
    Channel_pages = channel_page(channel_url)
    for page in Channel_pages:
        Detail_pages = detail_page(page)
        for detail in Detail_pages:
            try:
                find_video(detail)
            except Exception as e:
                continue

if __name__ == '__main__':
    Video_downloader()