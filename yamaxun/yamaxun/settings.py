# Scrapy settings for yamaxun project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'yamaxun'

SPIDER_MODULES = ['yamaxun.spiders']
NEWSPIDER_MODULE = 'yamaxun.spiders'

DOWNLOAD_FAIL_ON_DATALOSS = False
# LOG_FILE = "amazonLog.log"
# Crawl responsibly by identifying yourself (and your website) on the user-agent
# USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.88 Safari/537.36'
# redis配置
# 去重容器类配置 作用：redis的set集合来存储请求的指纹数据，从而实现去重的持久化
DUPEFILTER_CLASS = "scrapy_redis.dupefilter.RFPDupeFilter"
# 使用scrapy-redis的调度器
SCHEDULER = "scrapy_redis.scheduler.Scheduler"
SCHEDULER_QUEUE_CLASS = "scrapy_redis.queue.SpiderQueue"
SCHEDULER_PERSIST = True

# 链接redis数据库
# REDIS_HOST = "127.0.0.1"
# REDIS_PORT = 6379
# REDIS_URL = 'redis://192.168.1.101:6379'
REDIS_URL = 'redis://127.0.0.1:6379'

# 下载中间件
ITEM_PIPELINES = {
    'scrapy_redis.pipelines.RedisPipeline': 300,
    # 'yamaxun.pipelines.YamaxunPipeline': 301
}

# 注册随机请求头中间件
DOWNLOADER_MIDDLEWARES = {
    'yamaxun.middlewares.Middlewares': 543,
    # 'yamaxun.middlewares.YamaxunDownloaderMiddleware': 543,
}

# Obey robots.txt rules
ROBOTSTXT_OBEY = False


# 网络请求报错的是哪个状态码就填哪个状态码,如:[503]，意思是忽略这个错误请求继续进行下一个请求
# HTTPERROR_ALLOWED_CODES = [503]
# 加这个亚马逊反爬成功
DOWNLOADER_CLIENT_TLS_CIPHERS = "DEFAULT:!DH"
# 异常状态码
RETRY_HTTP_CODES = [500, 502, 503, 504, 522, 524, 408]
# 重试次数
RETRY_TIMES = 0
#下载延迟
DOWNLOAD_DELAY = 3.5
# # 编码
# FEED_EXPORT_ENCODING = 'utf-8'


# 请求头
USER_AGENT_LIST = [
    "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/532.5 (KHTML, like Gecko) Chrome/4.0.249.0 Safari/532.5",
    "Mozilla/5.0 (Windows; U; Windows NT 5.2; en-US) AppleWebKit/532.9 (KHTML, like Gecko) Chrome/5.0.310.0 Safari/532.9",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/534.7 (KHTML, like Gecko) Chrome/7.0.514.0 Safari/534.7",
    "Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US) AppleWebKit/534.14 (KHTML, like Gecko) Chrome/9.0.601.0 Safari/534.14",
    "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.14 (KHTML, like Gecko) Chrome/10.0.601.0 Safari/534.14",
    "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.20 (KHTML, like Gecko) Chrome/11.0.672.2 Safari/534.20",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534.27 (KHTML, like Gecko) Chrome/12.0.712.0 Safari/534.27",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/13.0.782.24 Safari/535.1",
    "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/535.2 (KHTML, like Gecko) Chrome/15.0.874.120 Safari/535.2",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.7 (KHTML, like Gecko) Chrome/16.0.912.36 Safari/535.7",
    "Mozilla/5.0 (Windows; U; Windows NT 6.0 x64; en-US; rv:1.9pre) Gecko/2008072421 Minefield/3.0.2pre",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.10) Gecko/2009042316 Firefox/3.0.10",
    "Mozilla/5.0 (Windows; U; Windows NT 6.0; en-GB; rv:1.9.0.11) Gecko/2009060215 Firefox/3.0.11 (.NET CLR 3.5.30729)",
    "Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6 GTB5",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; tr; rv:1.9.2.8) Gecko/20100722 Firefox/3.6.8 ( .NET CLR 3.5.30729; .NET4.0E)",
    "Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
    "Mozilla/5.0 (Windows NT 5.1; rv:5.0) Gecko/20100101 Firefox/5.0",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:6.0a2) Gecko/20110622 Firefox/6.0a2",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:7.0.1) Gecko/20100101 Firefox/7.0.1",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:2.0b4pre) Gecko/20100815 Minefield/4.0b4pre",
    "Mozilla/4.0 (compatible; MSIE 5.5; Windows NT 5.0 )",
    "Mozilla/4.0 (compatible; MSIE 5.5; Windows 98; Win 9x 4.90)",
    "Mozilla/5.0 (Windows; U; Windows XP) Gecko MultiZilla/1.6.1.0a"
]
PROXY_LIST = ['27.156.213.46:4368']

# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# 当COOKIES_ENABLED没有注释，设置为False的时候scrapy默认使用了settings里面的cookie,为True的时候scrapy就会把settings的cookie关掉，使用自定义cookie
COOKIES_ENABLED = False
DEFAULT_REQUEST_HEADERS = {
    'cookie':'thw=cn; enc=aXFwgFZHBKRR%2FvlcZp6RzWY4LBjMnDaEFLR74GOZxMxSUgc%2BiHLPpnk%2F8nQhOR4kToD%2FU8a24PQqT4aZMMXh7g%3D%3D; lgc=tb77188312; tracknick=tb77188312; cna=s26bGxtKymoCAXFtHpxgoagz; sgcookie=E100%2F0Dp1qRWBVb4kR6N9WzgLdRw6J%2BPdntjqRxhWEwXFUH84khu9qhQ0fxAXLsOv1lUUcllNvEIeY522BmYh5%2BHkhaGL196ZRqseezC%2Bv4Au4EtegeohUqym%2BUEbnzC3tUW; uc3=nk2=F5RCYrtywyjivg%3D%3D&id2=Uoncj3WS8M%2FmOg%3D%3D&vt3=F8dCv4fSBbPWdfOGk4Y%3D&lg2=URm48syIIVrSKA%3D%3D; uc4=nk4=0%40FY4JjC8oLE5TWfozqVTgHWi9cb%2BG&id4=0%40UOE2SK0sB1DE3I1K%2Fe%2Fg3Ho7ckXQ; _cc_=V32FPkk%2Fhw%3D%3D; _m_h5_tk=f09c896bb919991a031fcdaf9ae2064f_1662471364657; _m_h5_tk_enc=fc82ab13ce4fb7403bfcfed03c84a6f3; mt=ci=-1_0; xlly_s=1; x5sec=7b227365617263686170703b32223a2264333232333736656466383462323832346264343362613136353837303063334349794734706747454e664c2b3566636a72536152426f4d4d5467334e6a59304f4445314e5473784d4b6546677037382f2f2f2f2f77464141773d3d227d; JSESSIONID=112F7932F7910291E04CD5F38E85A90C; tfstk=cUfCB_YujDmQQSE6bpaaYXsvJjO5Zzq6SJtdRlkcvPug0n7Cijc2cs2OEcAyyF1..; l=eBMm052HTTkBbSqoBOfZnurza779IIRAguPzaNbMiOCP_51p5PvdW6kOIs89CnGVh6byR35Wn1oBBeYBqnY4n5U62j-la_Hmn; isg=BHFxLT24thh8jRoG_Z7f-SXGgP0LXuXQd4Tg7lOGbzhXepHMm62KobKYmA4csn0I',
    'referer':'https://s.taobao.com/search?q=%E7%BE%8E%E5%A6%86&tab=mall&bcoffset=297&ntoffset=297&p4ppushleft=%2C44&s=0',
    'sec-ch-ua':'"Chromium";v="104", " Not A;Brand";v="99", "Google Chrome";v="104"',
    'sec-ch-ua-mobile':'?0',
    'sec-ch-ua-platform':'"Windows"',
    'sec-fetch-dest':'document',
    'sec-fetch-mode':'navigate',
    'sec-fetch-site':'same-origin',
    'sec-fetch-user':'?1',
    'upgrade-insecure-requests': '1',
    'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36'
}

# 运行多个py的设置文件
COMMANDS_MODULE = "yamaxun.commands"
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!













# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs

# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)


# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:










# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'yamaxun.middlewares.YamaxunSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html



# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'
