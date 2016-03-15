# coding=utf-8

import re,datetime

from scrapy.contrib.spiders import Rule, CrawlSpider
from scrapy.contrib.loader import ItemLoader
from scrapy.selector import Selector
from scrapy.http import Request
from ..items import IndexNewsItem


class NewsSpider(CrawlSpider):
    name = "indexnews"
    allowed_domains = ["99.com.cn"]
    start_urls = ["http://www.99.com.cn/"]

    def parse(self, response):
        response_selector = Selector(response)
        for label_a in response_selector.xpath("//div[@class='pic']/ul/li/a").extract():
            detail_link = re.findall(r'''<a\shref="(.*?)"''', label_a)[0]
            index_img = re.findall(r'''<img\ssrc="(.*?)"''', label_a)[0]
            request = Request(url=detail_link, callback=self.parse_detail)
            request.meta['indeximg'] = index_img
            yield request

    def parse_detail(self, response):
        el = ItemLoader(item=IndexNewsItem(), response=response)
        el.add_xpath('title', "//div[@class='title']/h1/text()")
        el.add_xpath('time', "//span[@rel='pubdate']/text()")
        el.add_xpath('source', "//font[@rel='source']/text()")
        el.add_xpath('classf', "//div[@class='l_path']/span/a/text()")
        el.add_xpath('body', "//div[@class='detail_con']")
        el.add_value('thumbnail', response.meta['indeximg'])
        el.add_value('url', response.url)
        return el.load_item()
