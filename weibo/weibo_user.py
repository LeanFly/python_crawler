#coding=utf-8

import requests
from lxml import etree
from parsel import Selector
import re
from handle_mango import mongo_info

url = 'https://s.weibo.com/user?q=' + input('请输入要搜索的用户关键词：')

def weibo_spider():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.87 Safari/537.36'

    }

    response = requests.get(url=url, headers=headers)
    #构造html
    html = etree.HTML(response.text)
    #构造css文本
    css_text = Selector(text=response.text)
    wrap_list = css_text.css('.card')
    #print(wrap_list)
    
    #未登录状态获取搜索到的全部用户
    for cards in wrap_list:
        #创建用户字典
        user_info = {}
        #print(cards)
        #微博认证信息
        user_info['认证信息'] = cards.css('.info div a::attr(title)').extract_first()
        #user_info['name'] = html.xpath('//div[@id="pl_user_feedList"]/div[@class="card card-user-b s-pg16 s-brt1"][1]/div[@class="info"]/div/a[1]/em/text()')
        #个人主页
        personal_url = cards.css('.info div a::attr(href)').extract_first()    #:nth-child[1]::text
        if personal_url != None:
            user_info['personal_url'] = 'https:' + cards.css('.info div a::attr(href)').extract_first()
        #用户名
        user_name = cards.css('.info div a[class=name]').extract_first()
        if user_name != None:
            user_info['user_name'] = re.sub(r'(<(.*?)>)', '', user_name)
        #uid
        user_info['user_uid'] = cards.css('.info div a[class=s-btn-c]::attr(uid)').extract_first()
        #头像
        user_info['user_pic'] = cards.css('.avator img::attr(src)').extract_first()
        #关注
        user_info['follow'] = cards.css('.info p span a::text').extract_first()
        #粉丝
        user_info['fans'] = cards.css('.info p span:nth-of-type(2) a::text').extract_first()
        #微博数
        user_info['contents'] = cards.css('.info p .s-nobr a::text').extract_first()
        #简介
        user_info['summary'] = cards.css('.info p:nth-child(5)::text').extract_first()
        
        #print(user_info)
    
        print('开始对用户信息做入库处理：%s'  % user_info.items())    

        mongo_info.insert_item(user_info)


weibo_spider()