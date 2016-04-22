# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field


class MnewsItem(Item):
    title          = Field()
    time           = Field()
    source         = Field()
    classf         = Field()
    body           = Field()
    thumbnail      = Field()
    url            = Field()     # 用来实现增量式爬虫
    news_type      = Field()
