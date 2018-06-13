import json
import re
import time

import scrapy
from ..Item.KunMingItems import KunMingItems


class KunMingSpider(scrapy.Spider):
    name = "KunMing"

    def __init__(self, flightNo=None, flightDate=None, *args, **kwargs):
        super(KunMingSpider, self).__init__(*args, **kwargs)
        self.flightNo = flightNo
        self.flightDate = flightDate

    def start_requests(self):
        flightNo = "KY8220"
        # flightTime -昨天  +明天  .今天
        flightDate = "2018-06-09"
        url = "http://wap.airkunming.com/search/trip/flight?flightDate=" + self.flightDate + "&flightNo=" + self.flightNo
        yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        airlineCorp = '昆明航空'
        item = KunMingItems()
        js = json.loads(response.body)
        flights = js['values']
        # flightInfoDetailEntity = flightInfoDetailEntity['flightInfoDetailEntity']
        for flight in flights:
            item['airlineCorp'] = airlineCorp
            item['airline'] = flight['flightNo']
            item['expDeptTime'] = flight['depPlanDate']
            item['expArrTime'] = flight['arrPlanDate']
            item['actDeptTime'] = flight['depDate']
            item['actArrTime'] = flight['arrDate']
            item['status'] = flight['flightState']
            yield item
        pass
