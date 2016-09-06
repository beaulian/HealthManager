# -*- coding: utf-8 -*-

# Scrapy settings for news project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'news'
DEPTH_LIMIT = 1
DOWNLOAD_DELAY = 0.15  # 150ms

MONGO_URI = "localhost"
MONGO_PORT = 27017
MONGO_DB = "healthmanager"
DUPEFILTER_CLASS = 'scrapy.dupefilter.RFPDupeFilter'
# DUPEFILTER_CLASS = "news.mydupfilter.SeenURLFilter"
# LOG_FILE = "cqunews.log"
# LOG_STDOUT = True

SPIDER_MODULES = ['news.spiders']
NEWSPIDER_MODULE = 'news.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
# USER_AGENT = 'news (+http://www.yourdomain.com)'
ITEM_PIPELINES = {
    'news.pipelines.NewsPipeline': 300,
}
