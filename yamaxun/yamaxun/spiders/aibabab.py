import scrapy


class AibababSpider(scrapy.Spider):
    name = 'aibabab'
    allowed_domains = ['p4psearch.1688.com']
    start_urls = ['http://p4psearch.1688.com/']

    def parse(self, response):
        pass
