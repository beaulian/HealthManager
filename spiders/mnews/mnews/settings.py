# -*- coding: utf-8 -*-

# Scrapy settings for mnews project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'mnews'
DEPTH_LIMIT = 1
DOWNLOAD_DELAY = 0.15  # 150ms

MONGO_URI = "localhost"
MONGO_PORT = 27017
MONGO_DB = "healthmanager"
DUPEFILTER_CLASS = 'scrapy.dupefilter.RFPDupeFilter'

SPIDER_MODULES = ['mnews.spiders']
NEWSPIDER_MODULE = 'mnews.spiders'

# DUPEFILTER_CLASS = "news.mydupfilter.SeenURLFilter"
# LOG_FILE = "cqunews.log"
# LOG_STDOUT = True

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'mnews (+http://www.yourdomain.com)'

ITEM_PIPELINES = {
    'mnews.pipelines.MnewsPipeline': 300,
}

