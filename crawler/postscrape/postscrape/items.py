# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import TakeFirst


class Quelle(scrapy.Item):
    # define the fields for your item here like:
    link = scrapy.Field()
    volume = scrapy.Field()
    issue = scrapy.Field()
    date = scrapy.Field()
    checkDate = scrapy.Field()