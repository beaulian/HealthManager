# coding=utf-8

import re,datetime

from scrapy.contrib.spiders import Rule, CrawlSpider
from scrapy.contrib.loader import ItemLoader
from scrapy.selector import Selector
from scrapy.http import Request
from ..items import MnewsItem


class MnewsSpider(CrawlSpider):
	name = "mainnews"
	allowed_domains = ["99.com.cn"]
	start_urls = ["http://nv.99.com.cn/",
				  "http://nan.99.com.cn/",
				  "http://zyk.99.com.cn/",
				  "http://ye.99.com.cn/",
				  "http://ys.99.com.cn/",
				  "http://jf.99.com.cn/",
				]

	def parse(self, response):
		link_and_images = re.findall(r'''<a\shref="(.*?\.htm.*?)"[^<]+?>(?=<img\ssrc="(.*?)")''', response.body)
		if len(link_and_images) > 50:
			link_and_images = link_and_images[0:50]
		for link, image in link_and_images:
			if "http" not in link:
				continue
			request = Request(url=link, callback=self.parse_detail)
			request.meta["thumbnail"] = image
			request.meta["class"] = response.url.rsplit(".")[0].split("//")[1]
			yield request

	def parse_detail(self, response):
		el = ItemLoader(item=MnewsItem(), response=response)
		el.add_xpath('title', "//div[@class='title']/h1/text()")
		el.add_xpath('time', "//span[@rel='pubdate']/text()")
		el.add_xpath('source', "//font[@rel='source']/text()")
		el.add_value('classf', response.meta["class"])
		el.add_xpath('body', "//div[@class='detail_con']")
		el.add_value('thumbnail', response.meta['thumbnail'])
		el.add_value('url', response.url)
		# el.add_xpath('classf', "//div[@class='l_path']/span/a/text()")
		# el.add_value('second_domain', response.meta["class"])
		# print el.load_item().__dict__
		# print type(el.load_item())
		return el.load_item()
