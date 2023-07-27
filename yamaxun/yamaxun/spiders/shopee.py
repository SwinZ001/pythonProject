import scrapy


class ShopeeSpider(scrapy.Spider):
    name = 'shopee'
    allowed_domains = ['shopee.sg']
    start_urls = ['http://shopee.sg/']

    def parse(self, response):
        pass
