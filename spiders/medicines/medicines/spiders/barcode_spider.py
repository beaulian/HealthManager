#-*- coding: utf-8 -*-

import re,datetime

from scrapy.contrib.spiders import Rule, CrawlSpider
from scrapy.selector import Selector
from scrapy.http import Request
from bs4 import BeautifulSoup
from ..items import BarcodesItem


class BarcodesSpider(CrawlSpider):
	name = "barcode"
	start_urls = ["http://db.yaozh.com/instruct"]

	def parse(self, response):
		item = BarcodesItem()
		response_selector = Selector(response=response)

		for data in response_selector.xpath("//table/tbody/tr").extract():
			soup = BeautifulSoup(data)
			item["barcode"] = soup.th.text.strip()
			item["name"]    = soup.td.text
			yield item

		for i in range(2,29105):
			next_link = "http://db.yaozh.com/instruct?p={0}".format(str(i))
			yield Request(url=next_link, callback=self.parse)