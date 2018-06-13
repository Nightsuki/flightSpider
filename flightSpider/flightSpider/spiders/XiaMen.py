# coding=utf-8
import datetime
import json

import scrapy
from ..Item.XiaMenItems import XiaMenItems


class XiaMenSpider(scrapy.Spider):
    name = "XiaMen"

    def __init__(self, flightNo=None, flightDate=None, *args, **kwargs):
        super(XiaMenSpider, self).__init__(*args, **kwargs)
        self.flightNo = flightNo
        self.flightDate = flightDate

    def start_requests(self):
        # todo
        # 航班号和航班时间  动态传参
        url = 'https://new.xiamenair.com/api/flight-dynamic/flightno/search?fnumber='+self.flightNo+'&date='+self.flightDate
        yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        js = json.loads(response.body)
        flights = js['result']['Message']
        for flight in flights:
            item = XiaMenItems()
            airline = flight['FlightNo']
            expDeptTime = flight['Etd']
            expArrTime = flight['Eta']
            actDeptTime = flight['Atd']
            actArrTime = flight['Ata']
            # ARR 落地 NDR 落地 ATA 到达 CNL 取消 DEL 延误 DEP 起飞 RTR 返航 SCH 计划
            status = flight['Status']

            airlineCorp = '厦门航空'
            # print(str(flight))

            item['airline'] = airline
            item['airlineCorp'] = airlineCorp
            item['status'] = status
            item['expDeptTime'] = expDeptTime
            item['expArrTime'] = expArrTime
            item['actDeptTime'] = actDeptTime
            item['actArrTime'] = actArrTime
            yield item
        pass
