#coding=utf-8

import requests
import time
import re
from lxml import etree
from selenium import webdriver
import json


keyword = '健身'


#构造url解析函数
def crawl_keyword(url, data):
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.87 Safari/537.36',
        'cookie': 'WEATHER_CITY=%E5%8C%97%E4%BA%AC; UM_distinctid=16ab8fd9b2f191-00301054f500a9-7a1b34-1fa400-16ab8fd9b3055e; csrftoken=c53caca54971f3efecd72376c6f8ed58; _ga=GA1.2.1363732801.1558058274; __utmz=24953151.1564566417.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); uuid="w:ba1ee3e32cf440d5a72b0ed6d746730b"; __utma=24953151.1363732801.1558058274.1564566417.1566363714.2; CNZZDATA1259612802=2095179794-1557878329-%7C1570668200; tt_webid=6750068326112806407; tt_webid=6750068326112806407; WIN_WH=1920_452; s_v_web_id=8ba941688edb4e62b5f44751364d5ca1; __tasessionId=68uj0igdn1572932521933'    
        }
    response = requests.get(url=url, headers=headers, data=data)
    
    #print(response.text)
    return response

#构造json用户解析函数
def crawl_users():
    keyword = input('请输入搜索的内容关键词：')
    offset = 0
    data = {
    'aid': '24',
    'app_name': 'web_search',
    'offset': '0',
    'format': 'json',
    #keyword: 模特
    #'autoload': 'true'
    #'count': '20'
    #'en_qc': '1'
    #'cur_tab': '1'
    #'from': 'search_tab'
    #'pd': 'synthesis'
    #'timestamp': '1572920679137'
    }
    user_id = []
    user_name = []
    user_info = {}
    offsets = []
    offset = 0

    for i in range(20):
        offset += 20   
        offsets.append(offset)    
    
    for offset in offsets:
        api_url = 'https://www.toutiao.com/api/search/content/?aid=24&app_name=web_search&offset='+ str(offset) +'&format=json&keyword=' + keyword
        #print(api_url)
        crawl_keyword(url=api_url, data=data)        
        response = crawl_keyword(url=api_url, data=data)
        #创建内容字典
        content_dict = json.loads(response.text)
        #print(content_dict)
        try:
            for content_item in content_dict['data']:
                try:
                    user_id.append(content_item['media_creator_id'])    
                    user_name.append(content_item['media_name'])    
                except Exception as error:
                    continue
        except:
            continue
    print(user_id)        
    print(user_name)      

        
    

crawl_users()