import json
import re
import time

import scrapy
from ..Item.KunMingItems import KunMingItems


class KunMingSpider(scrapy.Spider):
    name = "KunMing"

    def start_requests(self):
        flightNo = "KY8220"
        # flightTime -昨天  +明天  .今天
        flightDate = "2018-06-09"
        url = "http://wap.airkunming.com/search/trip/flight?flightDate="+flightDate+"&flightNo="+flightNo
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
            item['actDeptTime'] = flight['depReadyDate']
            item['actArrTime'] = flight['arrReadyDate']
            item['status'] = flight['flightState']
            yield item
        pass
