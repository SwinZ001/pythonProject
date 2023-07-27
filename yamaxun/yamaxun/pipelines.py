# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import json

from itemadapter import ItemAdapter


class YamaxunPipeline:
    def open_spider(self, spider):
        if spider.name == "amazon":
            self.file = open(spider.name + ".json", 'w', encoding='utf-8')

    def process_item(self, item, spider):
        if spider.name == "amazon":
            item = dict(item)
            data = json.dumps(item, ensure_ascii=False) + ',\n'
            self.file.write(data)
        return item

    def close_spider(self, spider):
        if spider.name == "amazon":
            self.file.close()

