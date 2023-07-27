# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class YamaxunItem(scrapy.Item):
    # define the fields for your item here like:
    startUrl = scrapy.Field()
    big_classification_text = scrapy.Field()
    big_classification_link = scrapy.Field()
    page_link = scrapy.Field()

    commodity_link = scrapy.Field()
    commodity_data = scrapy.Field()
    # sku_link = scrapy.Field()
    # commodity_name = scrapy.Field()
    # commodity_price = scrapy.Field()
    # commodity_Imge_link = scrapy.Field()