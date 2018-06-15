# coding=utf-8
import datetime
import json
import logging

import scrapy
from ..Item.SiChuanItems import SiChuanItems


class SiChuanSpider(scrapy.Spider):
    name = 'SiChuan'

    def __init__(self, flightNo=None, flightDate=None, *args, **kwargs):
        super(SiChuanSpider, self).__init__(*args, **kwargs)
        self.flightNo = flightNo
        self.flightDate = flightDate

    def start_requests(self):
        url = "http://m.sichuanair.com/tribe-touch-web-h5/tribe/flight/flightStatus"
        data = {"body": {"conditionList": [{"flightNo": self.flightNo, "flightDate":self.flightDate}]},
                "head": {"platformId": 3}}
        yield scrapy.Request(url, method="POST", body=json.dumps(data), headers={'Content-Type': 'application/json'},
                             callback=self.parse)

    def parse(self, response):
        js = json.loads(response.body)
        logging.info(js)
        flightDate = datetime.datetime.strptime(self.flightDate, '%Y-%m-%d')
        flights = js['body']['flightStatusItemList']
        for flight in flights:
            item = SiChuanItems()
            airline = flight['flightNo']
            expDeptTime = flight['planTakeoffTime']
            expArrTime = flight['planArriveTime']
            expDeptTime = datetime.datetime(flightDate.year, flightDate.month, flightDate.day,
                                            int(expDeptTime.split(':')[0]),
                                            int(expDeptTime.split(':')[1]))
            expArrTime = datetime.datetime(flightDate.year, flightDate.month, flightDate.day,
                                           int(expArrTime.split(':')[0]),
                                           int(expArrTime.split(':')[1]))
            if expDeptTime > expArrTime:
                expArrTime = expArrTime + datetime.timedelta(days=1)
            actDeptTime = ''
            actArrTime = ''
            if 'actualTakeoffTime' in flight:
                actDeptTime = flight['actualTakeoffTime']
                actDeptTime = datetime.datetime(flightDate.year, flightDate.month, flightDate.day,
                                                int(actDeptTime.split(':')[0]),
                                                int(actDeptTime.split(':')[1]))
                if 'actualArriveTime' in flight:
                    actArrTime = flight['actualArriveTime']
                    actArrTime = datetime.datetime(flightDate.year, flightDate.month, flightDate.day,
                                                   int(actArrTime.split(':')[0]),
                                                   int(actArrTime.split(':')[1]))
                    if actDeptTime > actArrTime:
                        actArrTime = actArrTime + datetime.timedelta(days=1)
                    actArrTime = actArrTime.strftime("%Y-%m-%d %H:%M:%S")
                    actDeptTime = actDeptTime.strftime("%Y-%m-%d %H:%M:%S")

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
