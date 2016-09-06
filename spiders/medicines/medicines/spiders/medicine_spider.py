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
<<<<<<< HEAD
		return int(l_url[-1].split("=")[1])
=======
		return l_url[-2]
	return None

def split_url(url):
	if "?" in url:
		return url.split("?")[0]
	return url
>>>>>>> origin/front_one

class MedicineSpider(CrawlSpider):
	name = "medicine"
	start_urls = ["http://yao.dxy.com/"]

	rules = (
		Rule(LinkExtractor(allow='category/\d+?\.htm'), callback="parse_page", follow=False),
	)
	# def parse(self, response):
	# 	for link in re.findall('http://yao\.dxy\.com/category/\d+?\.htm', response.body):
	# 		yield Request(url=link, callback=self.parse_page)

	def parse_page(self, response):
		response_selector = Selector(response=response)
		for detail_link in response_selector.xpath("//div[@class='drugs-ser-list']/div/h3/a/@href").extract():
			yield Request(url=detail_link, callback=self.parse_detail)

<<<<<<< HEAD
		count = clear_url(response_selector.xpath("//div[@class='drugs-content clearfix']/p/a/@href").extract())
		if count:
			for i in range(2, count+1):
				yield Request(url=response.url+"?&page={0}".format(str(i)), callback=self.parse_page)
=======
		next_page = clear_url(response_selector.xpath("//div[@class='drugs-content clearfix']/p/a/@href").extract())
		if next_page:
			yield Request(url=split_url(response.url)+next_page, callback=self.parse_page)
>>>>>>> origin/front_one

	def parse_detail(self, response):
		el = ItemLoader(item=MedicinesItem(), response=response)
		el.add_xpath('name', "//div[@class='content-inner']/div[@class='content-header']/h2/text()")
		el.add_xpath('feature', "//div[@class='content-inner']/div[@class='content-drugs-describe']/div[4]/p/text()")
		el.add_xpath('company', "//div[@class='content-inner']/div[@class='content-drugs-describe']/div[2]/p/text()")
		el.add_xpath('usage', "//div[@class='content-inner']/div[@class='content-drugs-describe']/div[6]/p/text()")
		el.add_xpath('taboo', "//div[@class='content-inner']/div[@class='content-drugs-describe']/div[8]/p/text()")
		return el.load_item()
