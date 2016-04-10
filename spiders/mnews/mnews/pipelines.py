# -*- coding: utf-8 -*-

from utils import clear_html
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError


class MnewsPipeline(object):
    def __init__(self, mongo_uri, mongo_port, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_port = mongo_port
        self.mongo_db = mongo_db
        self.collection_name = "HealthNews"

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get("MONGO_URI"),
            mongo_port=crawler.settings.get("MONGO_PORT"),
            mongo_db=crawler.settings.get("MONGO_DB")
        )

    def open_spider(self, spider):
        self.client = MongoClient(self.mongo_uri, self.mongo_port)
        self.db = self.client[self.mongo_db]
        self.db[self.collection_name].ensure_index('url', unique=True)    # 设置url为唯一索引,从而实现增量式爬虫

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
    	class_map = {
			"nv"  : "女性",
			"nan" : "男性",
			"zyk" : "中医",
			"ye"  : "育儿",
			"ys"  : "饮食",
			"jf"  : "减肥"
		}

        item['title']        = item['title'][0]
        item['time']         = item['time'][0]
        item['source']       = item['source'][0]
        item['classf']       = class_map[item['classf'][0]]
        item['body']         = clear_html(item['body'][0])
        item['thumbnail']    = item['thumbnail'][0]
        item['url']          = item['url'][0]
        item['news_type']    = item['news_type'][0]

        try:
            self.db[self.collection_name].insert(dict(item))
        except DuplicateKeyError:
            print "skip %s" % item['url']

        return item
