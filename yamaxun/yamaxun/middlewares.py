# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html
import json
import random
from time import sleep

from scrapy import signals

# useful for handling different item types with a single interface
from itemadapter import is_item, ItemAdapter
from scrapy.core.downloader.handlers.http11 import TunnelError
from scrapy.http import HtmlResponse

from scrapy.utils.request import request_fingerprint
from selenium.webdriver.common.by import By
from twisted.internet import defer
from twisted.web._newclient import ResponseFailed
from twisted.internet.error import TimeoutError, TCPTimedOutError, ConnectionRefusedError, DNSLookupError, \
    ConnectionDone, ConnectError,ConnectionLost

import undetected_chromedriver.v2 as uc

from yamaxun.settings import USER_AGENT_LIST,PROXY_LIST,RETRY_HTTP_CODES


# 随机ip
class Middlewares(object):
    # def __init__(self):
        # self.i=0

    # 网络异常错误
    EXCEPTIONS_TO_RETRY = (defer.TimeoutError, TimeoutError, DNSLookupError, ConnectionRefusedError, ConnectionDone, ConnectError, ConnectionLost, TCPTimedOutError, ResponseFailed, IOError, TunnelError,IndexError)

    # 请求时调用
    def process_request(self, request, spider):
        print('')
        # 异常重新请求不会重新添加指纹解决（重新请求再将请求指纹添加到redis）
        # fp = request_fingerprint(request, include_headers=None)
        # spider.server.sadd(spider.name + ':dupefilter', fp)

        # 随机请求头
        # ua = random.choice(USER_AGENT_LIST)
        # request.headers['User-Agent'] = ua

        # # 随机ip
        # proxys = random.choice(PROXY_LIST)
        # proxy = 'https://'+str(proxys)
        # print(proxy)
        # request.meta['proxy'] = proxy





    # 响应时调用
    def process_response(self, request, response, spider):
        if spider.name == "skycat":
            if 'dataloss' in response.flags:
                print("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")
                fp = request_fingerprint(request, include_headers=None)
                print("指纹：" + fp)
                spider.server.srem(spider.name + ':dupefilter', fp)
                return request
            if response.status in RETRY_HTTP_CODES:
                print("CCCCCCCCCCCCCCCCCCCCCCCCCCCCCC" + str(response.status))
                fp = request_fingerprint(request, include_headers=None)
                print("指纹：" + fp)
                spider.server.srem(spider.name + ':dupefilter', fp)
                return request

            return response

        elif spider.name == "amazon":
            aa = response.xpath('//*[@class="a-last"]/text()')
            # print(self.i)
            if 'dataloss' in response.flags:
                print("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")
                fp = request_fingerprint(request, include_headers=None)
                print("指纹：" + fp)
                spider.server.srem(spider.name + ':dupefilter', fp)
                return request
            if len(aa) != 0:
                # self.i+=1
                print("BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB")
                # print(response.text)
                fp = request_fingerprint(request, include_headers=None)
                print("指纹：" + fp)
                spider.server.srem(spider.name + ':dupefilter', fp)
                return request
            if response.status in RETRY_HTTP_CODES:
                print("CCCCCCCCCCCCCCCCCCCCCCCCCCCCCC" + str(response.status))
                fp = request_fingerprint(request, include_headers=None)
                print("指纹：" + fp)
                spider.server.srem(spider.name + ':dupefilter', fp)
                return request

            return response





    # 请求异常时调用
    def process_exception(self, request, exception, spider):
        if spider.name == "skycat":
            if isinstance(exception, self.EXCEPTIONS_TO_RETRY):
                # 异常则删除请求指纹
                fp = request_fingerprint(request, include_headers=None)
                print("DDDDDDDDDDDDDDDDDDDDDDDD")
                print("指纹：" + fp)
                spider.server.srem(spider.name + ':dupefilter', fp)
                return request

        elif spider.name == "amazon":
            if isinstance(exception, self.EXCEPTIONS_TO_RETRY):
                # 异常则删除请求指纹
                fp = request_fingerprint(request, include_headers=None)
                print("DDDDDDDDDDDDDDDDDDDDDDDD")
                print("指纹：" + fp)
                spider.server.srem(spider.name + ':dupefilter', fp)
                return request







