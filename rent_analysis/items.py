# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class RentAnalysisItem(scrapy.Item):
    # define the fields for your item here like:
    category = scrapy.Field()
    location = scrapy.Field()
    address = scrapy.Field()
    area = scrapy.Field()
    price = scrapy.Field()
    description = scrapy.Field()
    created = scrapy.Field()
    edited = scrapy.Field()
    agent_type = scrapy.Field()
