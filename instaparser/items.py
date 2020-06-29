# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class InstafolowerItem(scrapy.Item):
    # define the fields for your item here like:
    _id = scrapy.Field()
    user_id = scrapy.Field()
    username = scrapy.Field()
    follower_id = scrapy.Field()
    follower_username = scrapy.Field()
    follower_fullname = scrapy.Field()
    follower_photo = scrapy.Field()


class InstafolowItem(scrapy.Item):
    # define the fields for your item here like:
    _id = scrapy.Field()
    user_id = scrapy.Field()
    username = scrapy.Field()
    user_follow_id = scrapy.Field()
    user_follow_username = scrapy.Field()
    user_follow_fullname = scrapy.Field()
    user_follow_photo = scrapy.Field()
