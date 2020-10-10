#coding=utf-8

import os
import requests
import re
import cryptography
import OpenSSL
import certifi
import time


print('请输入创建的文件夹名称：\n')
goodsFold = str(input())
#创建文件夹
os.mkdir(goodsFold)
os.chdir(goodsFold)
with open('C为橱窗图D为详情图.txt', 'w') as f:
    f.write('C为橱窗图D为详情图')
#输入商品详情链接
print('\n输入商品链接：\n')
goodsUrl = str(input())

#定义headers
httpHeaders = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36',
    'cookie': 'hng=CN%7Czh-CN%7CCNY%7C156; cna=gFTvF67nHDACAXTqJAQZ2FCZ; enc=JGslYS7m6K%2FVOVhGxZtSi7WVZeVkG4qMYEVb3gsxCXiXEAqDQUfHbux1Od6e%2BjOSrWl1ojw2LtghPAihRjFvIA%3D%3D; sgcookie=E100Jr10As3yo0jUyAVW%2BJdikgbSYwNwgXy%2BVCafOfyezZJ40Cl7rfXzcD9YmVXDlZFffDDhgmKJlBFGN%2BJA%2B%2FF%2BJg%3D%3D; t=b1e7914e023eee12c92942841f2a225b; uc3=vt3=F8dCufeBxDvSexV0EVU%3D&id2=W8rr7y5Ot8PI&lg2=W5iHLLyFOGW7aA%3D%3D&nk2=pzXIr2pV; tracknick=%5Cu51DD%5Cu6728%5Cu96E8; uc4=id4=0%40Wenha11C8mDKx%2Bb05wOetTH5oE4%3D&nk4=0%40pQNGP2AhNEhSKEMqtSonlYc%3D; lgc=%5Cu51DD%5Cu6728%5Cu96E8; _tb_token_=e65814e43613; cookie2=10c1d026831411cbe86795a88bc372ac; xlly_s=1; cq=ccp%3D1; pnm_cku822=098%23E1hvYpvUvbpvUpCkvvvvvjiWP2qWQjEbnLs9AjYHPmPU1jrbPF5pAjEjRFSU1j3Wn29CvvpvvvvvvvhvC9vhvvCvpU9CvvOUvvVvJh0IvpvUvvmvKDHPi84gvpvIvvvvvhCvvvvvvU8bphvWi9vv96CvpC29vvm2phCvhhvvvUnvphvppv9CvhQpzGGvC0Er0jc6%2BultEEkxfamKHkx%2F6jc6%2Ff8rakKQD7zZd3wQBw03IE7rV366%2BExr68TJEcqwaNFgeCr%2Bm7zOaNpXVc3LD7zhaB4A29hvCvvvMM%2Fevpvhvvmv99%3D%3D; tfstk=cygdBRmNNdv38yFtgDKGPyqTKFuRZWJ8C6wlyIi_375wUy_RiQ3mkm0vA76LWCC..; l=eBaQed8qOHVwaGHQBOfwourza77OSIRAguPzaNbMiOCP_yf65RJlWZ5XT38BC3GVh6jwR3RSn5QgBeYBqQAonxvOa6Fy_Ckmn; isg=BE9PlKxUTMdik0hRrKQmfsDI3uNZdKOWhR6AEmFc677FMG8yaUQz5k0iMmCOSHsO',
}

#判断商品来源
goodsHost = goodsUrl.split('//')[1].split('/')[0]

if goodsHost == 'detail.tmall.com':

    goodsRes = requests.get(goodsUrl, headers=httpHeaders).text

    time.sleep(2)

    #获取商品橱窗图，生成列表
    coverImg = re.findall(r'src="(.*?)q90.jpg', goodsRes)
    coverImgs = []
    for i in coverImg:
        coverImgs.append(i.split('jpg')[0] + 'jpg')

    time.sleep(2)

    #下载商品橱窗图
    print('\n开始下载商品橱窗图\n')
    for i in coverImgs:
        coverImgname = 'C' + str(coverImgs.index(i)) + '.jpg'
        with open(coverImgname, 'wb') as f:
            f.write(requests.get('https:' + i).content)
            time.sleep(1)

    time.sleep(2)

    #获取商品详情图，生成列表
    descUrl = 'http:' + re.findall(r'"descUrl":"(.*?)"', goodsRes)[0]
    descUrlRes = requests.get(descUrl, headers=httpHeaders).text
    descImg = re.findall(r'src="(.*?)"', descUrlRes)

    time.sleep(2)

    #下载商品详情图
    print('\n开始下载商品详情图\n')
    for i in descImg:
        imgname = 'D' + str(descImg.index(i)) + '.jpg'
        with open(imgname, 'wb') as f:
            f.write(requests.get(i).content)
            time.sleep(1)


    print('=====图片下载已完成，5秒后自动关闭=====')
    time.sleep(5)

elif goodsHost == 'item.jd.com':
    goodsRes = requests.get(goodsUrl, headers= httpHeaders).text

    time.sleep(2)

    #获取商品橱窗图，生成列表
    coverImg = re.findall(r'imageList:(.*?)],', goodsRes)[0]
    coverImg = re.findall(r'"(.*?)"', coverImg)

    #获取商品详情图，生成列表
    descUrl = re.findall(r"desc: '(.*?)'", goodsRes)[0]
    descUrl = 'https:' + descUrl
    descUrlRes = requests.get(descUrl, headers=httpHeaders).text
    descImg = re.findall(r'(//[^\s]*)\)', descUrlRes)

    #下载商品橱窗图
    print('\n开始下载商品橱窗图\n')
    for i in coverImg:
        coverImgname = 'C' + str(coverImg.index(i)) + '.jpg'
        coverImgurl = 'https://img14.360buyimg.com/n0/' + i
        with open(coverImgname, 'wb') as f:
            f.write(requests.get(coverImgurl).content)
            time.sleep(1)
    
    #下载商品详情图
    print('\n开始下载商品详情图\n')
    for i in descImg:
        descImgname = 'D' + str(descImg.index(i)) + '.jpg'
        descImgurl = 'http:' + i
        with open(descImgname, 'wb') as f:
            f.write(requests.get(descImgurl).content)
            time.sleep(1)

    print('=====图片下载已完成，5秒后自动关闭=====')
    time.sleep(5)

else:
    print('不支持当前站点的图片获取')
    print('5秒后关闭')
    time.sleep(5)