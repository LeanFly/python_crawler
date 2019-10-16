'''
@Description: In User Settings Edit
@Author: your name
@Date: 2019-10-15 15:53:03
@LastEditTime: 2019-10-16 15:18:12
@LastEditors: Please set LastEditors
'''
#!/usr/bin/python
#-*-coding:utf-8 -*-
import urllib.request
import urllib.parse
import os
import re

cate_link = input('?????????')


def url_open(url):
    headers = {'User-Agent':'Mozilla/5.0 3578.98 Safari/537.36'}
    req = urllib.request.Request(url=cate_link, headers=headers)
    response = urllib.request.urlopen(req)
    html = response.read()
    return html

#???????????
def find_urls(cate_link):
    html = url_open(cate_link).decode('UTF-8')
    #print(html)
    url_details = []
    #a = html.find('?</span><a href="')
    a = html.find('</span><a href="')
    #print(a)
    while a != -1:
        b = html.find('html', a)
        #print(b)
        if b !=-1:
            url_details.append(html[a+16:b+4])
            #print(url_details)
        else:
            b = a + 52
        a = html.find('</span><a href="', b)

        for i in url_details:
            if 'index_' in i:
                url_details.remove(i)
                return url_details
    
    
#if __name__ == '__main__':
x = find_urls(cate_link)
print(x)
