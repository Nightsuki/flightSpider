import datetime
import json

import scrapy
from ..Item.JinLuItems import JinLuItems

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


class JinLuSpider(scrapy.Spider):
    name = "JinLu"

    def __init__(self, flightNo=None, flightDate=None, *args, **kwargs):
        super(JinLuSpider, self).__init__(*args, **kwargs)
        self.flightNo = flightNo
        flightDate = datetime.datetime.strptime(flightDate, '%Y-%m-%d')
        year = str(int(flightDate.strftime('%Y')))
        month = str(int(flightDate.strftime('%m')))
        day = str(int(flightDate.strftime('%d')))
        flightDate = year + '-' + month + '-' + day
        self.flightDate = flightDate

    def start_requests(self):
        # todo
        # 航班号和航班时间  动态传参
        url = 'http://jdapp.jdair.net/jdh/json/flight/searchFlightDynamicsListByFltNo.json?flightNo=' + self.flightNo + '&flightDate=' + self.flightDate
        yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        js = json.loads(response.body)
        flights = js['data']
        for flight in flights:
            item = JinLuItems()
            airline = flight['flightNo']
            expDeptTime = flight['stdLocal']
            expArrTime = flight['staLocal']
            actDeptTime = flight['atdLocal']
            actArrTime = flight['ataLocal']
            # ARR 落地 NDR 落地 ATA 到达 CNL 取消 DEL 延误 DEP 起飞 RTR 返航 SCH 计划
            status = statusMsg[flight['status']]

            airlineCorp = '首都航空'
            item['airline'] = airline
            item['airlineCorp'] = airlineCorp
            item['status'] = status
            item['expDeptTime'] = expDeptTime
            item['expArrTime'] = expArrTime
            item['actDeptTime'] = actDeptTime
            item['actArrTime'] = actArrTime
            yield item
