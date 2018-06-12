# coding=utf-8
import json

import scrapy

from ..Item.DongHaiItems import DongHaiItems

statusMsg = {
    1: "计划",
    2: "已起飞",
    3: "已到达",
    4: "延误",
    5: "取消",
    6: "备降"
}


class DongHaiSpider(scrapy.Spider):
    name = "DongHai"

    def start_requests(self):
        url = "http://b2capi.donghaiair.cn/flight/getFlightByNo"
        flightNo = 'DZ6257'
        flightDate = '2018-06-06'
        yield scrapy.FormRequest(
            url=url,
            formdata={"flightNo": flightNo, "flightDate": flightDate,
                      "language": "zh-CN"},
            callback=self.parse
        )

    def parse(self, response):
        js = json.loads(response.body)
        flights = js['data']
        # print(str(flight))
        for flight in flights:
            item = DongHaiItems()
            airline = flight['flightNo']
            expDeptTime = flight['etdTime']
            expArrTime = flight['etaTime']
            actDeptTime = flight['atdTime']
            actArrTime = flight['ataTime']
            # 			航班状态 1：计划 2：起飞 3：到达 4：延误 5：取消 6：备降
            status = statusMsg[flight['flightStatus']]

            airlineCorp = '东海航空'
            # print(str(flight))

            item['airline'] = airline
            item['airlineCorp'] = airlineCorp
            item['status'] = status
            item['expDeptTime'] = expDeptTime
            item['expArrTime'] = expArrTime
            item['actDeptTime'] = actDeptTime
            item['actArrTime'] = actArrTime
            yield item
