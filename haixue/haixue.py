#coding=utf-8

#导入webdrive模块
from selenium import webdriver
#导入时间模块
import time

#C:\\Users\ssj\\AppData\\Local\\Google\\chromedriver.exe
chrome = webdriver.Chrome()
chrome.get('http://www.haixue.com')

#窗口最大化
#chrome.maximize_window()
#停留时间
time.sleep(5)

print(chrome.title)

chrome.find_element_by_xpath('//div[@class="index-loginBox index-loginBoxCheck"]/div[@class="index-loginInputWrapper"]/input').send_keys('18901650348')
time.sleep(1)
chrome.find_element_by_xpath('//div[@class="index-loginBox index-loginBoxCheck"]/div[@class="index-loginInputWrapper mt15"]/input').send_keys('20042008wda')
time.sleep(1)
chrome.find_element_by_xpath('//div[@class="index-loginBox index-loginBoxCheck"]/button[@class="index-loginBtn index-loginBtn--login"]').click()
time.sleep(2)
chrome.find_element_by_xpath('//div[@class="courses"]/div[@class="cou-right hasul"]/ul[@class="cate-ul"]/li').click()



time.sleep(15)