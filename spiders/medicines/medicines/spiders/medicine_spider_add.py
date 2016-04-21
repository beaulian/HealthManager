#-*- coding: utf-8 -*-

import re,datetime

from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.contrib.spiders import Rule, CrawlSpider
from scrapy.contrib.loader import ItemLoader
from scrapy.selector import Selector
from scrapy.http import Request
from ..items import MedicinesItem

def clear_url(l_url):
	if l_url and "=" in l_url[-1]:
		return l_url[-2]
	return None

def split_url(url):
	if "?" in url:
		return url.split("?")[0]
	return url

class MedicineSpider(CrawlSpider):
    name = "medicineadd"
    start_urls = ["http://yao.dxy.com/"]

    def parse(self, response):
        common_medicines = [
            "银翘片","感冒片","板蓝根","氟哌酸","蛇胆川贝液","镇咳宁糖浆","强力枇杷露",
            "病毒唑","果导片","云南白药","风湿止痛膏","救心丸","桂林西瓜霜","扑热息痛",
            "六神丸","风油精","创可贴","清凉油","活络油","麝香跌打风湿膏","连翘败毒片",
            "湿润"
        ]
        for keyword in common_medicines:
        	yield Request(url="http://yao.dxy.com/search.htm?type=5&keyword="+keyword, callback=self.parse_page)

    def parse_page(self, response):
    	response_selector = Selector(response=response)
    	for detail_link in response_selector.xpath("//div[@class='drugs-ser-list']/div/h3/a/@href").extract():
    		yield Request(url=detail_link, callback=self.parse_detail)

    	next_page = clear_url(response_selector.xpath("//div[@class='drugs-content clearfix']/p/a/@href").extract())
    	if next_page:
    		yield Request(url=split_url(response.url)+next_page, callback=self.parse_page)

    def parse_detail(self, response):
    	el = ItemLoader(item=MedicinesItem(), response=response)
    	el.add_xpath('name', "//div[@class='content-inner']/div[@class='content-header']/h2/text()")
    	el.add_xpath('feature', "//div[@class='content-inner']/div[@class='content-drugs-describe']/div[4]/p/text()")
    	el.add_xpath('company', "//div[@class='content-inner']/div[@class='content-drugs-describe']/div[2]/p/text()")
    	el.add_xpath('usage', "//div[@class='content-inner']/div[@class='content-drugs-describe']/div[6]/p/text()")
    	el.add_xpath('taboo', "//div[@class='content-inner']/div[@class='content-drugs-describe']/div[8]/p/text()")
    	return el.load_item()
