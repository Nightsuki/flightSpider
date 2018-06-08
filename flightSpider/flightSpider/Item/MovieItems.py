# coding=utf-8
import scrapy


class MovieItem(scrapy.Item):
    name = scrapy.Field()
    info = scrapy.Field()
    mark = scrapy.Field()
    quote = scrapy.Field()