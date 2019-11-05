#coding=utf-8

#导入pymongo包
import pymongo
from pymongo.collection import Collection

#构造MongoDB函数
class Connect_mongo(object):
    #初始化
    def __init__(self):
        self.client = pymongo.MongoClient(host='127.0.0.1', port=27017)
        self.user_data = self.client['weibo_user']
    #数据入库
    def insert_item(self, item):
        db_connection = Collection(self.user_data, 'weibo_user_item')
        db_connection.insert(item)
    #数据拉取
    def get_item(self):
        db_connection = Collection(self.user_data, 'weibo_user_item')
        return db_connection.find_one({})

mongo_info = Connect_mongo()
#print(mongo_info.get_item())