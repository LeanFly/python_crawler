# -*- coding: utf-8 -*-
'''
@File    :   gen_article_api.py
@Time    :   2023/09/08 10:25:46
@Author  :   leanfly 
@Version :   1.0
'''


import concurrent.futures
from fastapi import FastAPI, responses
import uvicorn
import time
import re
import requests

# from playwright.async_api import async_playwright

import asyncio

import yaml


import redis
import json

from loguru import logger


def fetch_data():
    # 创建一个 Redis 对象
    r = redis.Redis(host='', port=6379, db=15)
    # 从 Redis 获取数据
    data = r.get("wechat")
    return json.loads(data)

user_list = [{"name": "托尼酒局", "id": "Mzg3MDU2MDk2Mg=="}]


def get_article_list(account_id, cookie, token, page_num) -> list:
    """ 传入公众号标识 ID、cookie、token、页码，返回一个文章列表 """

    # 设定基础请求接口
    base_url = "https://mp.weixin.qq.com/cgi-bin/appmsg"

    # 请求参数
    params = {
        "action": "list_ex",
        "begin": page_num * 5,  # 查询起始页，#页数
        "count": 5,  # 每次允许拉 5 次发布的文章
        "fakeid": account_id,  # 公众号的标识ID
        "type": 9,
        "query": "",
        "token": token,  # 微信公众号的查询token,每天都会变化
        "lang": "zh_CN",
        "f": "json",
        "ajax": 1
    }

    # 设置请求头，参数为微信公众平台-订阅号cookie
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36',
        'Cookie': f'{cookie}'
    }

    # 向指定公众号的文章查询接口发送信息，并解析为json格式
    resp = requests.get(url=base_url, headers=headers, params=params).json()
    # logger.info(resp)


    if resp['base_resp']['err_msg'] == 'freq control':
        print("请求频率过高，需要等一段时间")
        return resp
    if 'invalid' in resp['base_resp']['err_msg']:
        print("请检查请求参数")
        return resp
    # 返回结果为该公众号最近2天次已发布文章概要信息
    lists = []
    lists = resp['app_msg_list']
    return lists


def get_article() -> list:
    # 读取 cookie、token
    # with open(r"C:\Users\ningm\Documents\python\API\wechat_article\params.yml", "r", encoding="utf-8") as f:
    #     data = yaml.load(f, yaml.FullLoader)
    # 改为从 redis 中读取
    data = fetch_data()

    id = user_list[0]["id"]
    articles = get_article_list(
        account_id=id, cookie=data["cookie"], token=data["token"], page_num=0)
    return articles


def get_video() -> list:
    # 读取 cookie、token
    # with open(r"C:\Users\ningm\Documents\python\API\wechat_article\params.yml", "r", encoding="utf-8") as f:
    #     data = yaml.load(f, yaml.FullLoader)

    # 改为从 redis 中读取
    data = fetch_data()
    
    api = "https://mp.weixin.qq.com/cgi-bin/videosnap"
    params = {
        "action": "get_feed_list",
        "username": "v2_060000231003b20faec8c6ea8a11c0d5cf07ef3db0775b1d6cff2e9a10f4a23f1fd1a26bca9c@finder",
        "buffer": "",
        "count": 5,
        "scene": 0,
        "token": data["token"],
        "lang": "zh_CN",
        "f": "json",
        "ajax": 1
    }

    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36",
        "cookie": data["cookie"],
    }
    req = requests.get(url=api, params=params, headers=headers)
    if req.status_code != 200:
        return []
    videos = req.json()
    videos = videos["list"]
    return videos


app = FastAPI()


@app.get("/article")
async def article():

    articles = get_article()

    return responses.JSONResponse(content=articles)


@app.get("/video")
async def video():

    videos = get_video()

    return responses.JSONResponse(content=videos)


if __name__ == "__main__":
    uvicorn.run("gen_article_api:app", host="0.0.0.0", port=13130, reload=True)
