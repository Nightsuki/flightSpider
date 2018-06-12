import scrapy


class FuZhouCaptchaItem(scrapy.Item):
    image_url = scrapy.Field()  # 保存图片地址
    images = scrapy.Field()  # 保存图片的信息
    flightNo = scrapy.Field()
    flightDate = scrapy.Field()
