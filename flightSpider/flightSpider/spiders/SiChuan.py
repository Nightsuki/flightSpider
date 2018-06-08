# coding=utf-8
import json

import scrapy
from ..Item.SiChuanItems import SiChuanItems


class SiChuanSpider(scrapy.Spider):
    name = 'SiChuan'

    def start_requests(self):
        url = "http://m.sichuanair.com/tribe-touch-web-h5/tribe/flight/flightStatus"
        data = {"body": {"conditionList": [{"flightNo": "3U8896", "flightDate": "2018-06-07"}]},
                "head": {"platformId": 3}}
        yield scrapy.Request(url, method="POST", body=json.dumps(data), headers={'Content-Type': 'application/json'},
                             callback=self.parse)

    def parse(self, response):
        js = json.loads(response.body)
        flights = js['body']['flightStatusItemList']
        for flight in flights:
            item = SiChuanItems()
            airline = flight['flightNo']
            expDeptTime = flight['planTakeoffTime']
            expArrTime = flight['planArriveTime']
            actDeptTime = flight['actualTakeoffTime']
            actArrTime = flight['actualArriveTime']
            status = flight['flightStaus']

            airlineCorp = '四川航空'
            # print(str(flight))

            item['airline'] = airline
            item['airlineCorp'] = airlineCorp
            item['status'] = status
            item['expDeptTime'] = expDeptTime
            item['expArrTime'] = expArrTime
            item['actDeptTime'] = actDeptTime
            item['actArrTime'] = actArrTime
            yield item
