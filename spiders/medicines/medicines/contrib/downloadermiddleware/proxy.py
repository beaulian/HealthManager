#-*- coding:utf-8 -*-

import random
import base64
from scrapy import log
from scrapy.conf import settings

class ProxyMiddleware(object):

	def process_request(self, request, spider):
		request.meta['proxy'] = settings.get('HTTP_PROXY')
		log.msg("Current IP: {0}".format(request.meta["proxy"]))