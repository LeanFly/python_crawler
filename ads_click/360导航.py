#coding=utf-8

from selenium import webdriver
import time

chrome = webdriver.Chrome()

#打开导航页
chrome.get('https://hao.360.com/')
time.sleep(1)
#窗口最大化
#chrome.maximize_window()
time.sleep(2)
#开始滚动页面
chrome.execute_script('window.scrollBy(0,400);')
time.sleep(1)
chrome.execute_script('window.scrollBy(0,300);')
time.sleep(3)
chrome.execute_script('window.scrollBy(0,400);')
time.sleep(2)
chrome.execute_script('window.scrollBy(0,300);')
time.sleep(2)
chrome.execute_script('window.scrollBy(0,400);')
time.sleep(2)
chrome.execute_script('window.scrollBy(0,400);')
time.sleep(2)
chrome.execute_script('window.scrollBy(0,200);')
time.sleep(2)
chrome.execute_script('window.scrollBy(0,200);')
time.sleep(1)

'''
#开始点击娱乐头条内容
chrome.find_element_by_xpath('//div[@id="service-relax"]/div/div[@class="service-bd gclearfix"]/div[@data-tab-cate="yuletoutiao-tab1"]/div[@class="newver"]/div[@class="yule-left"]/div[@class="infoflow-tab1"]/div[@class="infoflow-list"]/div[1]/div[@class="img-wrap"]').click()
time.sleep(2)

chrome.find_element_by_xpath('//div[@id="service-relax"]/div/div[@class="service-bd gclearfix"]/div[@data-tab-cate="yuletoutiao-tab1"]/div[@class="newver"]/div[@class="yule-left"]/div[@class="infoflow-tab1"]/div[@class="infoflow-list"]/div[2]/div[@class="img-wrap"]').click()
time.sleep(2)

chrome.find_element_by_xpath('//div[@id="service-relax"]/div/div[@class="service-bd gclearfix"]/div[@data-tab-cate="yuletoutiao-tab1"]/div[@class="newver"]/div[@class="yule-left"]/div[@class="infoflow-tab1"]/div[@class="infoflow-list"]/div[3]/div[@class="img-wrap"]').click()
time.sleep(2)

chrome.find_element_by_xpath('//div[@id="service-relax"]/div/div[@class="service-bd gclearfix"]/div[@data-tab-cate="yuletoutiao-tab1"]/div[@class="newver"]/div[@class="yule-left"]/div[@class="infoflow-tab1"]/div[@class="infoflow-list"]/div[4]/div[@class="img-wrap"]').click()
time.sleep(2)

chrome.find_element_by_xpath('//div[@id="service-relax"]/div/div[@class="service-bd gclearfix"]/div[@data-tab-cate="yuletoutiao-tab1"]/div[@class="newver"]/div[@class="yule-left"]/div[@class="infoflow-tab1"]/div[@class="infoflow-list"]/div[5]/div[@class="img-wrap"]').click()
time.sleep(2)

chrome.find_element_by_xpath('//div[@id="service-relax"]/div/div[@class="service-bd gclearfix"]/div[@data-tab-cate="yuletoutiao-tab1"]/div[@class="newver"]/div[@class="yule-left"]/div[@class="infoflow-tab1"]/div[@class="infoflow-list"]/div[6]/div[@class="img-wrap"]').click()
time.sleep(2)

chrome.find_element_by_xpath('//div[@id="service-relax"]/div/div[@class="service-bd gclearfix"]/div[@data-tab-cate="yuletoutiao-tab1"]/div[@class="newver"]/div[@class="yule-left"]/div[@class="infoflow-tab1"]/div[@class="infoflow-list"]/div[8]/div[@class="img-wrap"]').click()
time.sleep(2)

chrome.find_element_by_xpath('//div[@id="service-relax"]/div/div[@class="service-bd gclearfix"]/div[@data-tab-cate="yuletoutiao-tab1"]/div[@class="newver"]/div[@class="yule-left"]/div[@class="infoflow-tab1"]/div[@class="infoflow-list"]/div[7]/div[@class="img-wrap"]').click()
time.sleep(2)
'''

yuletoutiao = chrome.find_element_by_xpath('//div[@id="service-relax"]/div/div[@class="service-bd gclearfix"]/div[@data-tab-cate="yuletoutiao-tab1"]/div[@class="newver"]/div[@class="yule-left"]/div[@class="infoflow-tab1"]/div[@class="infoflow-list"]/*')
