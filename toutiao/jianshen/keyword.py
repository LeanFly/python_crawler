#coding=utf-8

import requests
import time
import re
from lxml import etree
from selenium import webdriver


keyword = '健身'

def open_browser():
    #构造浏览器
    browser = webdriver.Chrome()
    #打开地址
    browser.get('https://www.toutiao.com/search/?keyword')
    #传入keyword
    browser.find_element_by_xpath('//div[@class="y-left search-content"]/input').send_keys(keyword)
    time.sleep(1)
    browser.find_element_by_xpath('//div[@class="y-right"]/button').click()
    time.sleep(1)
    
    #user_id = browser.find_element_by_xpath('//div[@class="y-left"]//a[contains(@class, "lbtn source J_source")]/@href')
    user_ids = browser.find_element_by_xpath('//div[@class="sections"]//div[contains(@class, "articleCard")]/div[contains(@class,"item")]/div[contains(@class, "item-inner")]/div[contains(@class, "normal rbox")]/div[contains(@class, "rbox-inner")]/div[contains(@class, "y-box footer")]/div[contains(@class, "y-left")]/div[contains(@class, "y-left")]/a[1]')

    user_id = (user_ids.get_attribute("href"))
    return user_id
    browser.close()

user_info = []
while True:
    user_info.append(open_browser())
    print(user_info)
