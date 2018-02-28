# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ProxiesToBaiduItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    proxy = scrapy.Field()
    pass


class Ip66Item(scrapy.Item):
    proxy = scrapy.Field()


class KdlItem(scrapy.Item):
    proxy = scrapy.Field()


class XcdlItem(scrapy.Item):
    proxy = scrapy.Field()


class XiaoMaItem(scrapy.Item):
    proxy = scrapy.Field()


class YdlItem(scrapy.Item):
    proxy = scrapy.Field()
