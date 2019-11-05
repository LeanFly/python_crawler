#coding=utf-8

import requests
import re
import json
from parsel import Selector
import pymongo
from handle_mango import mongo_info
import time


#print(mongo_info.get_item()['user_uid'])
uid = mongo_info.get_item()['user_uid']
def crawl_contents():
    #调用一个特别函数，本函数通过weibo个人页面的H5页面获取
    # https://m.weibo.cn/api/container/getIndex

    #获取微博的containerid
    container_url = 'https://m.weibo.cn/api/container/getIndex?' + 'type=uid&value=' + uid

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.87 Safari/537.36'
    }

    response = requests.get(url=container_url, headers=headers)
    container_dict = json.loads(response.text)
    containerid = container_dict['data']['tabsInfo']['tabs'][1]['containerid']

    #通过获取containerid获取微博内容的json文件
    content_list = []

    for page in range(1):
        #print('正在获取第 %d 页的微博' % (page+1))
        content_url = 'https://m.weibo.cn/api/container/getIndex?' + 'containerid=' + containerid + '&page=' + str(page)
        print(content_url)
        try:
            content_req = requests.get(url=content_url, headers=headers)
        except:
            continue
        content_dict = json.loads(content_req.text)
        #print(content_dict)
        
        for card in content_dict['data']['cards']:
            content_info = {}
            try:
                content_info['scheme_url'] = card['scheme']
                content_info['dates'] = card['mblog']['created_at']
                content_info['reposts'] = comment = card['mblog']['reposts_count']
                content_info['comment'] = card['mblog']['comments_count']
                content_info['attitudes'] = comment = card['mblog']['attitudes_count']
                '''content_info = {
                    'url':scheme_url,
                    'date':dates,
                    '转发':reposts,
                    '评论':comment,
                    '意见':attitudes,
                    }'''
            except:
                continue
            print(content_info)
            mongo_info.insert_item(content_info)
crawl_contents()


    