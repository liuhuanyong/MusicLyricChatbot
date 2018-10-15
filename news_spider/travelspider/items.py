# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class TravelspiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    singer = scrapy.Field()
    url = scrapy.Field()
    song = scrapy.Field()
    album = scrapy.Field()
    geci = scrapy.Field()


