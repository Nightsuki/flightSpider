import scrapy


class LianHeItems(scrapy.Item):
    expDeptTime = scrapy.Field()
    expArrTime = scrapy.Field()
    actDeptTime = scrapy.Field()
    actArrTime = scrapy.Field()
    status = scrapy.Field()
    airline = scrapy.Field()
    airlineCorp = scrapy.Field()
