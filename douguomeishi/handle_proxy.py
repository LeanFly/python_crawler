#coding=utf-8

import requests
import random

#{"ip":"222.64.124.104","locale":""}
url = 'http://ip.hahado.cn/ip'
ip_list = ['http://39.137.69.7:8080','http://193.112.113.26:1080','http://123.207.66.220:1080']
proxies = {'http':random.choice(ip_list)}
print(proxies)
response = requests.get(url=url, proxies=proxies)
print(response.text)
