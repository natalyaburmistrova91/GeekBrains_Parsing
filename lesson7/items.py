# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import MapCompose, TakeFirst


def make_int(value):
    if value.isdigit():
        return float(value)
    return value


def params_cleaner(params):
    for i in params:
        params[i] = ' '.join(params[i].split())
        if params[i].isdigit():
            params[i] = float(params[i])
    return params


class ShopparserItem(scrapy.Item):
    # define the fields for your item here like:
    _id = scrapy.Field()
    name = scrapy.Field(output_processor=TakeFirst())  # список
    photos = scrapy.Field(input_processor=MapCompose())
    link = scrapy.Field(output_processor=TakeFirst())
    price = scrapy.Field(input_processor=MapCompose(make_int), output_processor=TakeFirst())  # список
    params = scrapy.Field(input_processor=MapCompose(params_cleaner), output_processor=TakeFirst())
