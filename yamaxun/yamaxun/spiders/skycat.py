import copy
import json
import pprint
import re
from scrapy_redis.spiders import RedisSpider
import scrapy
from yamaxun.items import YamaxunItem


class SkycatSpider(RedisSpider):
    name = 'skycat'
    redis_key = 'py21'

    def __init__(self,*args,**kwargs):
        domain = kwargs.pop('domain','')
        self.allowed_domains = list(filter(None,domain.split(',')))
        super(SkycatSpider,self).__init__(*args,**kwargs)

    def make_requests_from_url(self, url):
        item = YamaxunItem()
        item['startUrl'] = url
        return scrapy.Request(url,
                              dont_filter=True,
                              meta={'item': copy.deepcopy(item)},
                              )

    def parse(self, response):
        item = response.meta['item']
        print(response.text)
        html_data = re.findall('g_page_config = (.*);',response.text)[0]
        # 页面总数据
        json_data = json.loads(html_data)
        # 总页数
        totalPage = json_data['mods']['pager']['data']['totalPage']
        # 页数倍数
        pageSize = json_data['mods']['pager']['data']['pageSize']
        # 循环构造页数链接
        for index in range(0, int(totalPage)):
            page_num = pageSize * index
            print(page_num)
            page_url = 'https://s.taobao.com/search?q=%E7%BE%8E%E5%A6%86&tab=mall&s='+str(page_num)
            yield scrapy.Request(
                url=page_url,
                callback=self.get_item_data,
                dont_filter=True,
                meta={'item': copy.deepcopy(item)}
            )



    def get_item_link(self, response):
        print(response.text)
        item = response.meta['item']
        # 解析页面
        html_data = re.findall('g_page_config = (.*);', response.text)[0]
        # 页面总数据
        json_data = json.loads(html_data)
        # 获取商品nid
        item_data = json_data['mods']['itemlist']['data']['auctions']
        for index in item_data:
            nid = index['nid']
            print(nid)
            # Detail_Pages_url = 'https://detail.tmall.com/item.htm?id='+nid
            # yield scrapy.Request(
            #     url=Detail_Pages_url,
            #     callback=self.get_pages,
            #     meta={'item': copy.deepcopy(item)},
            #     dont_filter=True
            # )

    def get_item_data(self, response):
        print(response.text)
        item = response.meta['item']