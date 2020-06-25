# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class BookparserItem(scrapy.Item):
    # define the fields for your item here like:
    _id = scrapy.Field()
    name = scrapy.Field()
    author = scrapy.Field()
    book_link = scrapy.Field()
    wo_bonus_price = scrapy.Field()
    bonus_price = scrapy.Field()
    no_bonus_price = scrapy.Field()
    rate = scrapy.Field()

