#coding=utf-8
import requests
import json
import random
from multiprocessing import Queue
from handle_mongo import mongo_info
from concurrent.futures import ThreadPoolExecutor

#创建队列
queue_list = Queue()
#创建关键词列表
keywords = ['']
def handle_request(url,data):
    headers = {
        'client':'4',
        'version':'6948.2',
        'device':'SM-G955F',
        #'sdk':'22,5.1.1',
        'imei':'355757010301428',
        #'channel':'qqkp',
        #'mac':'30:0E:D5:18:48:B0',
        'resolution':'1600*900',
        'dpi':'2.0',
        #'android-id':'300ed51848b06261',
        #'pseudo-id':'51848b06261300ed',
        'brand':'samsung',
        'scale':'2.0',
        'timezone':'28800',
        'language':'zh',
        'cns':'3',
        'carrier':'CHINA+MOBILE',
        #'imsi':'460073014213184',
        'User-Agent':'Mozilla/5.0 (Linux; Android5.1.1; SM-G955FBuild/JLS36C; wv) AppleWebKit/537.36 (KHTML, likeGecko) Version/4.0Chrome/74.0.3729.136MobileSafari/537.36',
        'act-code':'e6c2ae98126372a22d7cea8f6bdf28a0',
        #'act-timestamp':'1572318833',
        'uuid':'0f819582-d689-4955-8398-956ce51e4912',
        #'battery-level':'0.70',
        #'battery-state':'2',
        'newbie':'1',
        #'reach':' 10000',
        'Content-Type':'application/x-www-form-urlencoded; charset=utf-8',
        'Accept-Encoding':'gzip, deflate',
        'Connection':'Keep-Alive',
        #'Cookie':'duid=61640082',
        'Host':'api.douguo.net',
        #'Content-Length':'88',
        }
    #使用代理伪装
    ip_list = ['http://39.137.69.7:8080','http://193.112.113.26:1080','http://123.207.66.220:1080']
    proxy = {'http':random.choice(ip_list)}
    response = requests.post(url=url, headers=headers, data=data, proxies=proxy, timeout=60)
    return response

def handle_index():
    keyword = input('请输入菜谱查找关键词：')
    url = 'http://api.douguo.net/recipe/v2/search/0/400'
    #笔记 'http://api.douguo.net/search/universal/0/10'
    data = {
        'client':'4',
        #'_session':'1572320366716355757010301428',
        'keyword':keyword,
        'order':'0',
        #'_vs':'11102',
        #'type':'0'
        }
    
    response = handle_request(url=url, data=data)
    #print(response, end='\r\n')
    index_response_dict = json.loads(response.text)
    
    ids = []
    authors = []
    titles = []
    
    #print(index_response_dict['result']['list'][0]['r']['id'])
    for index_item in index_response_dict['result']['list']:
        #print(index_item['type'], end='\n\n')
        #print(index_item['r']['id'], end='\n\n')
        ids.append(index_item['r']['id'])

        queue_list.put(index_item['r']['id'])
    

        authors.append(index_item['r']['an'])
        titles.append(index_item['r']['n'])
    #print(queue_list.qsize())
    print('发现 %d 个菜谱' % len(ids))
    #return ids
    #print(ids, end='\n\n')
    #print(authors, end='\n\n')
    #print(titles, end='\n\n')
    
def handle_Recipe(ids):    
    #for detail_id in ids:
        
    #菜谱详情页地址
    detail_url = 'http://api.douguo.net/recipe/detail/' + str(ids)
    print('发现菜谱详情地址--> %s' % detail_url)
    detail_data = {
        'client':'4',
        #'_session':'1572320366716355757010301428',
        'author_id':'0',
        '_vs':'11102',
        '_ext':'{"query":{"kw":"+ keyword +","src":"11102","idx":"16","type":"13","id":"+ ditail_id +"}}',
        #'is_new_user':'1',
        }
    content_response = handle_request(url=detail_url, data=detail_data).text
    content = json.loads(content_response)
    #print(content, end= '\n\n')
    Recipe = {}
    #菜谱标题
    Recipe['title'] = content['result']['recipe']['title']
    #print(Recipe['title'])
    #菜谱作者
    Recipe['author'] = content['result']['recipe']['author']
    #print(Recipe['author'])
    #制作步骤
    Recipe['cook_step'] = content['result']['recipe']['cookstep']
    #print(Recipe['cook_step'])
    #食材清单
    Recipe['shicai'] = content['result']['recipe']['major']
    #print(Recipe['shicai'])
    #小贴士
    Recipe['tips'] = content['result']['recipe']['tips']
    #print(Recipe['tips'])
    #菜品建议
    #advice = content['result']['recipe']['advice']
    #缩略图
    Recipe['title_pic'] = content['result']['recipe']['original_photo_path']
    print('当前入库的菜谱是--> %s' % Recipe['title'])
    mongo_info.insert_item(Recipe)
    
    


handle_index()

#定义最大线程
pool = ThreadPoolExecutor(max_workers=20)
while queue_list.qsize() > 0:
    pool.submit(handle_Recipe,queue_list.get())
