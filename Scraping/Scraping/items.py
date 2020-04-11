# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class Event(scrapy.Item):
    name = scrapy.Field()
    artist = scrapy.Field()
    venue = scrapy.Field()
    url = scrapy.Field()
    time = scrapy.Field()
    ages = scrapy.Field()
    date = scrapy.Field()
