# -*- coding: utf-8 -*-

from scrapy.item import Item, Field


class IndexNewsItem(Item):
    title = Field()
    time = Field()
    source = Field()
    classf = Field()
    body = Field()
    thumbnail = Field()
    url = Field()     # 用来实现增量式爬虫




