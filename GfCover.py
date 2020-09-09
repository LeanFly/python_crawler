# coding=utf-8

import os
import urllib.request
import re
from PIL import Image

def GfCoverDownload():
    print('请输入视频代号：')
    keyInput = input()
    imgName = str(keyInput) + 'Cover' + '.jpg'
    searchUrl = 'http://www.javlibrary.com/cn/vl_searchbyid.php?keyword=' + str(keyInput)
    #print(searchUrl)
    headers = {
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36'
    }
    req = urllib.request.Request(url=searchUrl, headers=headers)
    res = urllib.request.urlopen(req)
    #print(res.read().decode('utf-8'))
    htmlContent = res.read().decode('utf-8')
    imgSrc = re.findall(r'id="video_jacket_img" src="(.*?) width', htmlContent)
    imgSrc = 'http:' + imgSrc[0].split('"')[0]
    print('获取到封面链接 %s' % imgSrc)
    with open(imgName, 'wb') as ff:
        imgReq = urllib.request.Request(url=imgSrc,headers=headers)
        imgRes = urllib.request.urlopen(imgReq).read()
        ff.write(imgRes)
            
    print('已下载 %s 的封面图' % keyInput)
    imgTemp = Image.open(imgName)
    imgSize = imgTemp.size
    print('当前封面的尺寸{}'.format(imgSize))
    '''
    裁剪：传入一个元组作为参数
    元组里的元素分别是：（距离图片左边界距离x， 距离图片上边界距离y，距离图片左边界距离+裁剪框宽度x+w，距离图片上边界距离+裁剪框高度y+h）
    '''
    # 截取图片中一块宽400高439的
    x = 400
    y = 0
    w = 400
    h = 538
    region = imgTemp.crop((x, y, x+w, y+h))
    region.save(imgName)
    print('封面图已裁剪完成')
if __name__ == '__main__':
    GfCoverDownload()