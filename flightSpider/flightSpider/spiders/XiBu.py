import json

import scrapy
from ..Item.XiBuItems import XiBuItems


class XiBuSpider(scrapy.Spider):
    name = "XiBu"

    def __init__(self, flightNo=None, flightDate=None, *args, **kwargs):
        super(XiBuSpider, self).__init__(*args, **kwargs)
        self.flightNo = flightNo
        self.flightDate = flightDate

    def start_requests(self):
        # flightNo = "PN6232"
        # flightDate = "2018-06-07"
        url = "https://p.westair.cn/tripast/dyoptwo/query?num=" + self.flightNo + "&date=" + self.flightDate + "&queryType=1&token="
        yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        airlineCorp = '西部航空'
        item = XiBuItems()
        js = json.loads(response.body)
        flights = js['list']
        # flightInfoDetailEntity = flightInfoDetailEntity['flightInfoDetailEntity']
        for flight in flights:
            item['airlineCorp'] = airlineCorp
            item['airline'] = flight['flightNoCode']
            item['expDeptTime'] = flight['etdLocal']
            item['expArrTime'] = flight['etaLocal']
            item['actDeptTime'] = flight['tOffLocal']
            item['actArrTime'] = flight['tDwnLocal']
            item['status'] = flight['status']
            yield item
        pass
