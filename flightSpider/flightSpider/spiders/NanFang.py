# coding=utf-8
import json

import scrapy
from ..Item.NanFangItems import NanFangItems
statusMsg = {
    "ARR": "落地",
    "NDR": "落地",
    "ATA": "到达",
    "CNL": "取消",
    "DEL": "延误",
    "DEP": "起飞",
    "RTR": "返航",
    "SCH": "计划"
}


class NanFangSpider(scrapy.Spider):
    name = "NanFang"

    def start_requests(self):
        flightNo = '3109'
        flightDate = '20180606'
        url = "https://b2c.csair.com/B2C40/flight/flightDynamic.ao?date=" + flightDate + "&fltNr=" + flightNo
        yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        js = json.loads(response.body)
        flights = js['data']
        for flight in flights:
            item = NanFangItems()
            print(str(flight))
            airline = flight['fltNr']
            expDeptTime = flight['crewDepDt']
            expArrTime = flight['crewArvDt']
            actDeptTime = flight['actDepDt']
            actArrTime = flight['actArvDt']
            # ARR 落地 NDR 落地 ATA 到达 CNL 取消 DEL 延误 DEP 起飞 RTR 返航 SCH 计划
            status = statusMsg[flight['fltSts']]
            airlineCorp = '南方航空'
            item['airline'] = airline
            item['airlineCorp'] = airlineCorp
            item['status'] = status
            item['expDeptTime'] = expDeptTime
            item['expArrTime'] = expArrTime
            item['actDeptTime'] = actDeptTime
            item['actArrTime'] = actArrTime
            yield item
        pass
