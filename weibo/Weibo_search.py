#coding=utf-8

import requests
import json
import re
import time
import pandas as pd
from parsel import Selector
from lxml import etree
import jieba
import numpy as np
import matplotlib.pyplot as plt
from wordcloud import WordCloud, ImageColorGenerator, STOPWORDS
from PIL import Image


keyword = input('请输入要搜索的关键词：')
search_url = 'https://s.weibo.com/weibo?q=' + keyword + '&Refer=top'

# 获取搜索到的第一个微博内容
def weibo_spider(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.87 Safari/537.36'
    }
    response = requests.get(url=search_url, headers=headers)

    #构造css文本
    css_text = Selector(text=response.text)
    wrap_list = css_text.css('.card')
    #搜索结果的第一个    
    weibo_detail_url = 'https:' + wrap_list[0].css('.content .from a[target=_blank]::attr(href)').extract_first()
    print('本次搜索排第一的内容页面 --> %s ' % weibo_detail_url)
    #评论链接的id获取
    comment_id = css_text.css('.card-wrap')[0].css('::attr(mid)').extract_first()
    print('该内容的comment_id --> %s ' % comment_id)
    #用户名
    user_name = wrap_list[0].css('.info div a[class=name]::attr(nick-name)').extract_first() #a[class=name]
    print('发布该内容的用户 --> %s ' % user_name)
    #uid
    user_uid = wrap_list[0].css('.info div a[class=s-btn-c]::attr(uid)').extract_first()
    print('该用户的UID --> %s ' % user_uid)
    #个人页面
    personal_page = wrap_list[0].css('.info div a[class=name]::attr(href)').extract_first()
    print('该用户的个人页面 --> %s ' % personal_page)
        
    return comment_id





#采集评论
def crawl_comment(comment_id, page):
    #创建评论列表
    comments = []
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.87 Safari/537.36',
        'Cookie': 'SINAGLOBAL=9448298116720.574.1558335309181; SCF=As2f_HJRbKdL-tAK9BOhncmeB2QSaK4gLuMCZu1cLLG5pCyPq4gxXFiLAtXNZGbze7iSPWMrkW6PbyLEWXfLHMA.; SUHB=0z1x-lgCzNXYZT; SUBP=0033WrSXqPxfM72wWs9jqgMF55529P9D9WhcVjRomGSjINZvpscny1fJ5JpV2h.7SKBNeKzXSXWpMC4odcXt; SUB=_2AkMqOt4idcPxrAFRm_oQyG3ibYxH-jyZ77fUAn7uJhMyAxgv7lkzqSVutBF-XKaJF7OBAccva0Mv2LwDkUtNN8ZT; UOR=,,117.78.42.153; YF-V5-G0=3751b8b40efecee990eab49e8d3b3354; login_sid_t=6911d9c5e681035a9d8d5626304de584; cross_origin_proto=SSL; Ugrow-G0=9ec894e3c5cc0435786b4ee8ec8a55cc; _s_tentry=-; Apache=3638807813792.7837.1572844964497; ULV=1572844964504:30:1:1:3638807813792.7837.1572844964497:1572498230103; WBStorage=384d9091c43a87a5|undefined; YF-Page-G0=aedd5f0bc89f36e476d1ce3081879a4e|1572949564|1572949291'
        }
    
    proxies = {
        'http': 'http://:183.146.213.157:80',
        'http': 'http://36.25.243.51:80',
        }

    for i in range(0, page):

        comment_url = 'https://weibo.com/aj/v6/comment/big?ajwvr=6&id='+ comment_id + '&root_comment_max_id_type=0&root_comment_ext_param=&page=' + str(i + 1) + '&filter=hot&sum_comment_number=1300&filter_tips_before=0&from=singleWeiBo&__rnd=' + str(int(round(time.time() * 1000)))
        print(comment_url)        
        response = requests.get(url=comment_url, headers=headers, proxies=proxies)
        time.sleep(1)
        comment_dict = json.loads(response.text)['data']['html']
        #print(comment_dict)
        comment_html = etree.HTML(comment_dict)
        #comments_data = comment_html.xpath('//div[@class="list_li S_line1 clearfix"]/div[@class="list_con"]/div[@class="WB_text"]/text()')
        comments_data = comment_html.xpath('//div[@class="WB_text"]/text()')
        print(len(comments_data))
        for i in comments_data:
            comments.append(i.replace('：' ,'').replace(' ', '').replace('转发微博', ''))
        for j in comments:
            if j == '\n' or j == '':
                comments.remove(j)
        time.sleep(10)
    print(len(comments))
    return comments

#生成评论的CSV文件
def comment_csv():
    ID = weibo_spider(search_url)
    comment = crawl_comment(ID, 100)
    comment_pd = pd.DataFrame(columns=['comment'], data=comment)
    csv_name = str(keyword.replace('#', '')) + '.csv'
    comment_pd.to_csv(csv_name, encoding='utf-8')
    print('成功写入评论的CSV文件 %s ' % csv_name)

#生成词云
def Words_Cloud():
    #打开CSV文件
    csv_name = str(keyword.replace('#', '')) + '.csv'
    file_text = pd.read_csv(csv_name, usecols=[1])
    #复制内容，传入list
    #file_text_copy['comment'] = file_text['comment'].apply(lambda x: str(x).split())
    file_text_list = file_text.copy().values.tolist()
    #通过jieba的cut操作对文字进行分割
    comment_cut = jieba.cut(str(file_text_list), cut_all=False)
    #生成词云词汇
    comment_words = ''.join(comment_cut)
    #设置WordCloud参数
    comment_cloud = WordCloud(scale=4, max_font_size=200, mask=img_shape, mode='RGBA', background_color='white', font_path=font, stopwords=STOPWORDS, )
    #开始generate
    comment_cloud.generate(comment_words)
    #生成图片
    img_name = str(keyword.replace('#', '')) + '.png'
    comment_cloud.to_file(img_name)
    print('^^词云图片生成完成^^')

# 字体参数
font = r'C:\\Windows\\Fonts\\电影海报字体.TTF'
# 图片模板
img_shape = np.array(Image.open('C:\\Users\\ssj\\Pictures\china.png'))
#停用词
STOPWORDS = {'回复',}


if __name__ == '__main__':
    
    comment_csv()
    Words_Cloud()

