# -*- coding: utf-8 -*-

# Scrapy settings for medicines project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'medicines'

SPIDER_MODULES = ['medicines.spiders']
NEWSPIDER_MODULE = 'medicines.spiders'

# log
LOG_ENABLED = True
LOG_FILE = "medicine.log"
LOG_STDOUT = True

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'medicines (+http://www.yourdomain.com)'

DOWNLOAD_DELAY = 3
DNSCACHE_ENABLED = True

AUTOTHROTTLE_ENABLED = True

MONGO_URI = "localhost"
MONGO_PORT = 27017
MONGO_DB = "healthmanager"
DUPEFILTER_CLASS = 'scrapy.dupefilter.RFPDupeFilter'

ITEM_PIPELINES = {
	'medicines.pipelines.ypipeline.BarcodesPipeline',
    'medicines.pipelines.dpipeline.MedicinesPipeline',
}

DOWNLOADER_MIDDLEWARES = {
	'scrapy.contrib.downloadermiddleware.useragent.UserAgentMiddleware': None,
	'medicines.contrib.downloadermiddleware.useragent.RotateUserAgentMiddleware': 400,
	# 'medicines.contrib.downloadermiddleware.proxy.ProxyMiddleware': 400,
}

#disenable cookie
COOKIES_ENABLED = False

USER_AGENT = ''

HTTP_PROXY = 'http://127.0.0.1:8118'

