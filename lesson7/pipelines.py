# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import scrapy
from scrapy.pipelines.images import ImagesPipeline
from pymongo import MongoClient
import os


class DatabasePipeline:
    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.mongo_base = client.shop_scrapy

    def process_item(self, item, spider):
        collection = self.mongo_base[spider.name]
        collection.insert_one(item)
        return item


class LoadPhotosPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        if item['photos']:
            for img in item['photos']:
                try:
                    yield scrapy.Request(img, meta=item)
                except Exception as e:
                    print(e)

    def file_path(self, request, response=None, info=None):
        item = request.meta # получаем данные из мета
        index = str(request)[-7:-5]
        return f'{item["name"]}/{index}.jpg'

    def item_completed(self, results, item, info):
        if results:
            item['photos']=[itm[1] for itm in results if itm[0]]
        return item