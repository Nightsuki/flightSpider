# coding=utf-8
import scrapy


class TuniuItem(scrapy.Item):
    url = scrapy.Field()
    title = scrapy.Field()
    price = scrapy.Field()
    days = scrapy.Field()
    personNum = scrapy.Field()
    recommendNum = scrapy.Field()
    detail = scrapy.Field()