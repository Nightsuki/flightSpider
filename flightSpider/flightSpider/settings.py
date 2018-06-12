# -*- coding: utf-8 -*-

# Scrapy settings for flightSpider project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html
IPPOOL = [
    {"ipaddr": "127.0.0.1:1080/"},
    # {"ipaddr": "116.62.128.50:16816"},
    # {"ipaddr": "114.215.174.98:16816"},
    # {"ipaddr": "122.114.214.159:16816"},
    # {"ipaddr": "121.42.148.121:16816"},
    # {"ipaddr": "120.25.71.27:16816"},
    # {"ipaddr": "116.62.113.134:16816"},
    # {"ipaddr": "122.114.234.72:16816"},
    # {"ipaddr": "116.196.107.90:16816"}
]
BOT_NAME = 'flightSpider'

SPIDER_MODULES = ['flightSpider.spiders']
NEWSPIDER_MODULE = 'flightSpider.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
# USER_AGENT = 'flightSpider (+http://www.yourdomain.com)'
# USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.'
# Obey robots.txt rules
ROBOTSTXT_OBEY = False

MYSQL_HOST = 'localhost'
MYSQL_DBNAME = 'flightspider2'
MYSQL_USER = 'root'
MYSQL_PASSWD = '1234'
# Configure maximum concurrent requests performed by Scrapy (default: 16)
CONCURRENT_REQUESTS = 1

# Configure a delay for requests for the same website (default: 0)
# See https://doc.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY = 1
# The download delay setting will honor only one of:
# CONCURRENT_REQUESTS_PER_DOMAIN = 16
CONCURRENT_REQUESTS_PER_IP = 1

# Disable cookies (enabled by default)
COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
# TELNETCONSOLE_ENABLED = False

# Override the default request headers:
# DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
# }

# Enable or disable spider middlewares
# See https://doc.scrapy.org/en/latest/topics/spider-middleware.html
SPIDER_MIDDLEWARES = {

}

# Enable or disable downloader middlewares
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
    'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
    'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': None,
    'scrapy.downloadermiddlewares.defaultheaders.DefaultHeadersMiddleware': None,
    'flightSpider.middlewares.RamdomUserAgentMiddleware.RamdomUserAgentMiddleware': 2,
    'flightSpider.middlewares.MyproxiesSpiderMiddleware.MyproxiesSpiderMiddleware': 1,
}

# Enable or disable extensions
# See https://doc.scrapy.org/en/latest/topics/extensions.html
# EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
# }

# Configure item pipelines
# See https://doc.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    # 'flightSpider.pipelines.LiaoxuefengPipeline': 300,
    #  'flightSpider.pipelines.TuniuPipeline':1
    'flightSpider.pipelines.FlightSpiderPipeline': 2,
    # 'flightSpider.pipeline.FuZhouCaptchaPipeline.FuZhouCaptchaPipeline': 1
}
IMAGES_STORE = 'images'   #存储图片的文件夹位置
# Enable and configure the AutoThrottle extension (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/autothrottle.html
# AUTOTHROTTLE_ENABLED = True
# The initial download delay
# AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
# AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
# AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
# AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
# HTTPCACHE_ENABLED = True
# HTTPCACHE_EXPIRATION_SECS = 0
# HTTPCACHE_DIR = 'httpcache'
# HTTPCACHE_IGNORE_HTTP_CODES = []
# HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'
# REDIRECT_ENABLED = True