#coding=utf-8

import jieba
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from wordcloud import WordCloud, ImageColorGenerator, STOPWORDS
from PIL import Image

#字体参数
font = r'C:\\Windows\\Fonts\\电影海报字体.TTF'
#图片模板
img_shape = np.array(Image.open('C:\\Users\\ssj\\Pictures\\13.2.2.png'))

#停用词
STOPWORDS = {'回复', '"'}
#CSV文件名
file_name = 'ios13.2.2更新.csv'
#图片名
img_name = file_name.split('.')[0]

def word_cloud():
    
    df = pd.read_csv(file_name, usecols=[1])
    df_copy = df.copy()
    df_copy['comment'] = df_copy['comment'].apply(lambda x: str(x).split())    #去空格
    df_list = df_copy.values.tolist()
    comment = jieba.cut(str(df_list), cut_all=False)
    words = ' '.join(comment)
    #word_c = WordCloud(width=2000, height = 2000, background_color='white', font_path=font, stopwords=STOPWORDS, contour_width=3, contour_color='steelblue')
    word_c = WordCloud(scale=4, mask=img_shape, background_color='white', font_path=font, stopwords=STOPWORDS, max_font_size=200, contour_color='steelblue', mode='RGBA')
    word_c.generate(words)
    #设置图片名
    word_c.to_file(img_name + '.png')
    print('Done')
word_cloud()