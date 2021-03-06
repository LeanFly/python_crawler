#coding=utf-8

import jieba
import pandas as pd
import numpy as np
from wordcloud import WordCloud, ImageColorGenerator, STOPWORDS
from PIL import Image

#字体参数
font = r'C:\\Windows\\Fonts\\电影海报字体.TTF'
#停止词
STOPWORDS = {'回复',}
#图片模板
img_shape = np.array(Image.open('C:\\Users\\ssj\\Pictures\hk.jpg'))

def word_cloud():
    df = pd.read_csv('Hong Kong.csv', usecols=[1])
    df_copy = df.copy()
    df_copy['comment'] = df_copy['comment'].apply(lambda x: str(x).split())    #去空格
    df_list = df_copy.values.tolist()
    comment = jieba.cut(str(df_list), cut_all=False)
    words = ' '.join(comment)
    #word_c = WordCloud(width=2000, height = 2000, background_color='white', font_path=font, stopwords=STOPWORDS, contour_width=3, contour_color='steelblue')
    word_c = WordCloud(scale=1, mask=img_shape, background_color='white', font_path=font, stopwords=STOPWORDS, max_font_size=200, contour_width=3, contour_color='steelblue')
    word_c.generate(words)
    word_c.to_file('hk.png')
    print('Done')
word_cloud()