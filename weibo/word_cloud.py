#coding=utf-8

import jieba
import pandas as pd
from wordcloud import WordCloud
import numpy as np

font = r'C:\\Windows\\Fonts\\电影海报字体.TTF'
STOPWORDS = {'回复',}

def word_cloud():
    df = pd.read_csv('linzhiling.csv', usecols=[1])
    df_copy = df.copy()
    df_copy['lin_zhi_ling'] = df_copy['lin_zhi_ling'].apply(lambda x: str(x).split())    #去空格
    df_list = df_copy.values.tolist()
    comment = jieba.cut(str(df_list), cut_all=False)
    words = ' '.join(comment)
    word_c = WordCloud(width=2000, height = 2000, background_color='white', font_path=font, stopwords=STOPWORDS, contour_width=3, contour_color='steelblue')
    word_c.generate(words)
    word_c.to_file('linzhiling.png')

word_cloud()