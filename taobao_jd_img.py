#coding=utf-8

import os
import requests
import re
import cryptography
import OpenSSL
import certifi
import time
import json
print('***\n支持的内容\n>京东：图片、视频(有水印)\n>淘宝：图片\n>天猫：图片、视频\n***')
print('请输入创建的文件夹名称：\n')
goodsFold = str(input())
#创建文件夹
os.mkdir(goodsFold)
os.chdir(goodsFold)
with open('C为橱窗图D为详情图video为商品介绍视频.txt', 'w') as f:
    f.write('C为橱窗图D为详情图video为商品介绍视频')
#输入商品详情链接
print('\n输入商品链接：\n')
goodsUrl = str(input())

#定义headers
httpHeaders = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36',
    'cookie': 'hng=CN%7Czh-CN%7CCNY%7C156; cna=gFTvF67nHDACAXTqJAQZ2FCZ; enc=JGslYS7m6K%2FVOVhGxZtSi7WVZeVkG4qMYEVb3gsxCXiXEAqDQUfHbux1Od6e%2BjOSrWl1ojw2LtghPAihRjFvIA%3D%3D; sgcookie=E100Jr10As3yo0jUyAVW%2BJdikgbSYwNwgXy%2BVCafOfyezZJ40Cl7rfXzcD9YmVXDlZFffDDhgmKJlBFGN%2BJA%2B%2FF%2BJg%3D%3D; t=b1e7914e023eee12c92942841f2a225b; uc3=vt3=F8dCufeBxDvSexV0EVU%3D&id2=W8rr7y5Ot8PI&lg2=W5iHLLyFOGW7aA%3D%3D&nk2=pzXIr2pV; tracknick=%5Cu51DD%5Cu6728%5Cu96E8; uc4=id4=0%40Wenha11C8mDKx%2Bb05wOetTH5oE4%3D&nk4=0%40pQNGP2AhNEhSKEMqtSonlYc%3D; lgc=%5Cu51DD%5Cu6728%5Cu96E8; _tb_token_=e65814e43613; cookie2=10c1d026831411cbe86795a88bc372ac; xlly_s=1; cq=ccp%3D1; pnm_cku822=098%23E1hvYpvUvbpvUpCkvvvvvjiWP2qWQjEbnLs9AjYHPmPU1jrbPF5pAjEjRFSU1j3Wn29CvvpvvvvvvvhvC9vhvvCvpU9CvvOUvvVvJh0IvpvUvvmvKDHPi84gvpvIvvvvvhCvvvvvvU8bphvWi9vv96CvpC29vvm2phCvhhvvvUnvphvppv9CvhQpzGGvC0Er0jc6%2BultEEkxfamKHkx%2F6jc6%2Ff8rakKQD7zZd3wQBw03IE7rV366%2BExr68TJEcqwaNFgeCr%2Bm7zOaNpXVc3LD7zhaB4A29hvCvvvMM%2Fevpvhvvmv99%3D%3D; tfstk=cygdBRmNNdv38yFtgDKGPyqTKFuRZWJ8C6wlyIi_375wUy_RiQ3mkm0vA76LWCC..; l=eBaQed8qOHVwaGHQBOfwourza77OSIRAguPzaNbMiOCP_yf65RJlWZ5XT38BC3GVh6jwR3RSn5QgBeYBqQAonxvOa6Fy_Ckmn; isg=BE9PlKxUTMdik0hRrKQmfsDI3uNZdKOWhR6AEmFc677FMG8yaUQz5k0iMmCOSHsO',
}
tbHeaders = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36',
    'cookie': 't=311fa663cdc37ea0a9c21386cf7a0e10; v=0; _tb_token_=eb76bbd5765b3; _m_h5_tk=4c5266376770ac3a8152e292aa08dd7f_1603186709426; _m_h5_tk_enc=8dfbf2516ffce43fa9437c1bdfc4ecd0; cna=hXkVGAZ0Ji4CATol5GGwUaBF; xlly_s=1; cookie2=1fc2f0e23dc07ddb2c55743458a555c6; lLtC1_=1; miid=285175652026058109; _samesite_flag_=true; tfstk=clpABwOzf40DtjIJYIhuCgPMKcRAZT0OPo_gBD6YlQJnUa2OiFpHpBvKGGaAe0C..; l=eBPeQd2lOoBs35pMBOfwourza77OSIRAguPzaNbMiOCPOg595C0cWZ5ENA8pC3GVhs_yR3-wPvU8BeYBqoxIdJfZe5DDwQHmn; isg=BKCgGlXY621d6ldpQSjBVIhQca5yqYRzsZIjFBqxbLtOFUA_wrlUA3ajrb2VpTxL'
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
    print('\n获取到商品橱窗图 %d 张' %len(coverImgs))
    #下载商品橱窗图
    print('\n开始下载商品橱窗图\n……\n')
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
    print('\n获取到商品详情图 %d 张' %len(descImg))
    time.sleep(2)
    #下载商品详情图
    print('\n开始下载商品详情图\n……\n')
    for i in descImg:
        imgname = 'D' + str(descImg.index(i)) + '.jpg'
        with open(imgname, 'wb') as f:
            f.write(requests.get(i).content)
            time.sleep(1)

    #获取商品展示视频
    imgVedioUrl = re.findall(r'imgVedioUrl":"(.*?)swf', goodsRes)[0]
    if  len(imgVedioUrl) != 0:
        videoUrltmp1 = imgVedioUrl.split('/e/')[0]
        videoUrltmp2 = imgVedioUrl.split('/', 12)[-1]
        videotmp = videoUrltmp1 + '/e/6/t/1/' + videoUrltmp2
        print('\n获取到商品介绍视频\n开始下载\n……\n')
    video = 'https:' + str(videotmp) + 'mp4'

    #利用session来获取ResponseHeathers里的location，这里的location是视频的真是下载地址
    videosession = requests.Session()
    videoRes = requests.Session().get(url=video, headers=httpHeaders, allow_redirects=False)    #allow_redirects=False 必填
    videoUrl = videoRes.headers['location']
    with open('video.mp4', 'wb') as f:
        f.write(requests.get(videoUrl).content)
    print('\n商品介绍视频已下载\n')
    print('=====下载已完成，5秒后自动关闭=====')
    time.sleep(5)

elif goodsHost == 'item.jd.com':
    goodsRes = requests.get(goodsUrl, headers= httpHeaders).text

    time.sleep(2)

    #获取商品橱窗图，生成列表
    coverImg = re.findall(r'imageList:(.*?)],', goodsRes)[0]
    coverImg = re.findall(r'"(.*?)"', coverImg)
    print('\n获取到商品橱窗图 %d 张' %len(coverImg))

    #获取商品详情图，生成列表
    descUrl = re.findall(r"desc: '(.*?)'", goodsRes)[0]
    descUrl = 'https:' + descUrl
    descUrlRes = requests.get(descUrl, headers=httpHeaders).text
    descImg = re.findall(r'(//[^\s]*)\)', descUrlRes)
    print('\n获取到商品详情图 %d 张' %len(descImg))

    # 获取商品视频链接
    vid = re.findall(r'"mainVideoId":"(.*?)"', goodsRes)[0]
    if  len(vid) == 0:
        print('没有获取到视频')
    else:
        print('发现商品视频介绍')
    vidUrl = 'https://c.3.cn/tencent/video_v3?callback=jQuery2419633&vid=' + str(vid)
    vidRes = requests.get(vidUrl).text
    playUrl = re.findall(r'playUrl":"(.*?)\?dockingId', vidRes)[0]
    #print(playUrl)
    
    #下载商品橱窗图
    print('\n开始下载商品橱窗图\n')
    for i in coverImg:
        coverImgname = 'C' + str(coverImg.index(i)) + '.jpg'
        coverImgurl = 'http://img10.360buyimg.com/cms/' + i
        
        with open(coverImgname, 'wb') as f:
            f.write(requests.get(coverImgurl).content)
            time.sleep(1)
    
    #下载商品详情图
    print('\n开始下载商品详情图\n……\n')
    for i in descImg:
        descImgname = 'D' + str(descImg.index(i)) + '.jpg'
        descImgurl = 'http:' + i
        with open(descImgname, 'wb') as f:
            f.write(requests.get(descImgurl).content)
            time.sleep(1)
    print('=详情图片下载完成=')
    #下载商品视频
    print('\n开始下载视频\n……\n')
    with open('Video.mp4', 'wb') as f:
        f.write(requests.get(playUrl).content)
        time.sleep(1)
    print('=商品视频已下载=')

    print('=====下载已完成，5秒后自动关闭=====')
    time.sleep(5)

elif goodsHost == 'item.taobao.com':
    goodsRes = requests.get(goodsUrl, headers=tbHeaders).text
    time.sleep(1)

    #获取橱窗图，生成列表
    coverImg = re.findall(r'\[.*?]', goodsRes)[0]
    coverImg = re.findall(r'"(.*?)"', coverImg)
    print('\n获取到商品橱窗图 %d 张' %len(coverImg))
    #获取详情图片，生成列表
    desc = 'http:' + re.findall(r"location.protocol==='http:' \? '(.*?)'", goodsRes)[0]
    detailRes = requests.get(desc).text
    descImg = re.findall(r'img align="absmiddle" src="(.*?)" style=', detailRes)
    print('\n获取到商品详情图 %d 张' %len(descImg))

    #下载橱窗图
    print('\n开始下载橱窗图\n……\n')
    for i in coverImg:
        imgname = 'C' + str(coverImg.index(i)) + '.jpg'
        imgsrc = 'http:' + str(i)
        with open(imgname, 'wb') as f:
            f.write(requests.get(imgsrc).content)
            time.sleep(1)
    print('\n图片下载完成\n')

    #下载详情图
    print('\n开始下载详情图\n……\n')
    for i in descImg:
        imgname = 'D' + str(descImg.index(i)) + '.jpg'
        with open(imgname, 'wb') as f:
            f.write(requests.get(i).content)
            time.sleep(1)
    print('\n图片下载完成\n')

    #获取商品介绍视频
    '''
        https://h5api.m.taobao.com/h5/mtop.taobao.cloudvideo.video.queryforh5/1.0/
        ?jsv=2.4.2
        &appKey=12574478
        &t=1603165408854
        &sign=b48a4fb676d7d4179569391ec6863fe8
        &api=mtop.taobao.cloudvideo.video.queryForH5
        &v=1.0
        &timeout=1000
        &type=jsonp
        &dataType=jsonp
        &callback=mtopjsonp1
        &data=%7B%22videoId%22%3A%22212278162593%22%2C%22from%22%3A%22detail%22%7D
        &data=%7B"videoId"%3A"212278162593"%2C"from"%3A"detail"%7D
        (data: {"videoId":"212278162593","from":"detail"})
    '''
    # 迫于未能解析请求参数中的sign值，视频API请求失败
    # videoId = re.findall(r'"videoId":"(.*?)"', goodsRes)[0]
    # print(videoId)
    # if len(videoId) != 0:
    #     print('获取到视频ID，开始进行下载\n\n……\n')
    #     timestamp = int(time.time()*1000)
    #     videoApi = 'https://h5api.m.taobao.com/h5/mtop.taobao.cloudvideo.video.queryforh5/1.0/' + '?jsv=2.4.2' + '&appKey=12574478' + '&t=' + str(timestamp) + '&sign=993121a31b84f24b08f3e13c8c7af2a6' + '&api=mtop.taobao.cloudvideo.video.queryForH5' + '&v=1.0' + '&timeout=1000' + '&type=jsonp' + '&dataType=jsonp' + '&callback=mtopjsonp1' + '&data=%7B%22' + 'videoId' + '%22%3A%22' +  str(videoId) + '%22%2C%22' + 'from' + '%22%3A%22' + 'detail' + '%22%7D'
    #     print(videoApi)
    #     videoApiRes = requests.get(videoApi).text
    #     video_url = re.findall(r'"video_url":"(.*?)"', videoApiRes)
    #     print(video_url)
    #     with open('video.mp4', 'wb') as f:
    #         f.write(requests.get(video_url).content)
    #     print('\n商品介绍视频已下载\n')

    print('=====下载已完成，5秒后自动关闭=====')
    time.sleep(5)

else:
    print('不支持当前站点的图片获取')
    print('5秒后关闭')
    time.sleep(5)