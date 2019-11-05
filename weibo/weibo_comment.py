#coding=utf-8

import requests
import json
from lxml import etree
import pandas as pd

#微博的详情页地址
#'https://weibo.com/' + uid + '/' + 链接参数(Ib84jgPcQ)

#采集评论
def crawl_comment(page):
    #创建评论列表
    comments = []
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.87 Safari/537.36',
        'Cookie': 'SINAGLOBAL=9448298116720.574.1558335309181; SCF=As2f_HJRbKdL-tAK9BOhncmeB2QSaK4gLuMCZu1cLLG5pCyPq4gxXFiLAtXNZGbze7iSPWMrkW6PbyLEWXfLHMA.; SUHB=0z1x-lgCzNXYZT; SUBP=0033WrSXqPxfM72wWs9jqgMF55529P9D9WhcVjRomGSjINZvpscny1fJ5JpV2h.7SKBNeKzXSXWpMC4odcXt; SUB=_2AkMqOt4idcPxrAFRm_oQyG3ibYxH-jyZ77fUAn7uJhMyAxgv7lkzqSVutBF-XKaJF7OBAccva0Mv2LwDkUtNN8ZT; UOR=,,117.78.42.153; YF-V5-G0=3751b8b40efecee990eab49e8d3b3354; login_sid_t=6911d9c5e681035a9d8d5626304de584; cross_origin_proto=SSL; Ugrow-G0=9ec894e3c5cc0435786b4ee8ec8a55cc; _s_tentry=-; Apache=3638807813792.7837.1572844964497; ULV=1572844964504:30:1:1:3638807813792.7837.1572844964497:1572498230103; WBStorage=384d9091c43a87a5|undefined; YF-Page-G0=aedd5f0bc89f36e476d1ce3081879a4e|1572949564|1572949291'
        }
    
    for i in range(0, page):
        comment_url = 'https://weibo.com/aj/v6/comment/big?ajwvr=6&id=4402673648027428&page=' + str(i + 1)
        #print(comment_url)
        response = requests.get(url=comment_url, headers=headers)
        comment_dict = json.loads(response.text)['data']['html']
        comment_html = etree.HTML(comment_dict)
        comments_data = comment_html.xpath('//div[@class="list_li S_line1 clearfix"]/div[@class="list_con"]/div[@class="WB_text"]/text()')
        #comments_data1 = comment_html.xpath('//div[@class="list_box"]/div[@class="list_ul"]/div/div[@class="list_con"]/div[@class="list_box_in S_bg3"]//div[@class="WB_text"]/text()')
        #print(len(comments_data))
        for i in comments_data:
            print('开始采集评论--》 %s' % i)
            if i == '\n            ':
               comments_data.remove(i)
            elif i == '：回复':
                comments_data.remove(i)
            else:
                i = i.replace(':' ,'').replace(' ', '')
                comments.append(i)
    for j in comments:
        if j == '':
            comments.remove(j)    
    return comments

#生成评论的CSV文件
def comment_csv():
    lin_zhi_ling = crawl_comment(100)
    lin_zhi_ling_pd = pd.DataFrame(columns=['lin_zhi_ling'], data=lin_zhi_ling)
    lin_zhi_ling_pd.to_csv('linzhiling.csv', encoding='utf-8')


#执行生成操作
if __name__ == '__main__':
    comment_csv()

