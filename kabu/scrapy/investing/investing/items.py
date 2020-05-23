# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class StockItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    stock_date= scrapy.Field()
    stock_end = scrapy.Field()
    stock_begin = scrapy.Field()
    stock_high = scrapy.Field()
    stock_low = scrapy.Field()
    stock_vol = scrapy.Field()
    stock_ratio = scrapy.Field()
