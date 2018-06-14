# coding=utf-8
import json

import scrapy

from ..Item.ShenZhenItems import ShenZhenItems


class ShenZhenSpider(scrapy.Spider):
    name = "ShenZhen"

    def __init__(self, flightNo=None, flightDate=None, *args, **kwargs):
        super(ShenZhenSpider, self).__init__(*args, **kwargs)
        self.flightNo = flightNo
        self.flightDate = flightDate

    def start_requests(self):
        url = "http://m.shenzhenair.com/weixin_front/flightDynamics.do?method=getFlightListByFlightNo"
        yield scrapy.FormRequest(url=url,
                                 formdata={"flightNo": self.flightNo, "date": self.flightDate, "onoff": "false"})

    def parse(self, response):
        print(bytes.decode(response.body))
        flights = json.loads(response.body)
        for flight in flights:
            item = ShenZhenItems()
            airline = flight['FLIGHTNO']
            expDeptTime = flight['EXPECTEDDEPTIME']
            expArrTime = flight['EXPECTEDARRTIME']
            actDeptTime = flight['DEPTIME']
            actArrTime = flight['ARRTIME']
            # 			航班状态 1：计划 2：起飞 3：到达 4：延误 5：取消 6：备降
            status = flight['STATE']

            airlineCorp = '深圳航空'
            # print(str(flight))

            item['airline'] = airline
            item['airlineCorp'] = airlineCorp
            item['status'] = status
            item['expDeptTime'] = expDeptTime
            item['expArrTime'] = expArrTime
            item['actDeptTime'] = actDeptTime
            item['actArrTime'] = actArrTime
            yield item
