#coding=utf-8

import requests
import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def new_rank():
    url = 'https://www.newrank.cn/xdnphb/list/weibo_day/rank?end=2019-11-07&rank_name=%E4%B8%AA%E4%BA%BA%E8%AE%A4%E8%AF%81&rank_name_group=&start=2019-11-07&nonce=75dacb96d&xyz=03bd02ee75821a060ba316b3d4e649a6'

    headers = {
        'end':'2019-11-07',
        'rank_name':'%E4%B8%AA%E4%BA%BA%E8%AE%A4%E8%AF%81',
        'rank_name_group':'',
        'start':'2019-11-07',
        'nonce':'75dacb96d',
        'xyz':'03bd02ee75821a060ba316b3d4e649a6',
        }

    response = requests.post(url=url, headers=headers).text
    content_json = json.loads(response)
    data_list = content_json['value']['datas']
    用户名 = []
    粉丝数 = []
    发布数 = []
    评论数 = []
    转发数 = []
    新榜指数 = []
    个人主页 = []
    UID = []
    for data in data_list:

        # print(data['name'])
        用户名.append(data['name'])

        # print(data['followers_count'])
        粉丝数.append(int(data['followers_count']))

        # print(data['article_count'])
        发布数.append(int(data['article_count']))

        # print(data['comments_count'])
        评论数.append(int(data['comments_count']))

        # print(data['reposts_count'])
        转发数.append(int(data['reposts_count']))

        # print(data['newrank_index'])
        新榜指数.append(int(data['newrank_index']))

        # print(data['index_url'])
        个人主页.append(data['index_url'])

        # print(data['uid'])
        UID.append(int(data['uid']))

    table_title = ['发布数', '粉丝数', '评论数', '转发数', '新榜指数', '个人主页', 'UID']
    index = 用户名
    print(index)
    list_l = [发布数, 粉丝数, 评论数, 转发数, 新榜指数, 个人主页, UID]
    print(list_l)

    # pandas.DataFrame( data, index, columns, dtype, copy) 
    # index:行索引；columns:列索引
    data_frame = pd.DataFrame(list_l, index=table_title, columns=index)
    # 行列转换
    df = data_frame.stack().unstack(0)
    print(df)
    #写入Excel文件
    df.to_excel('new_rank1.xls')

if __name__ == '__main__':
    new_rank()


    