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
        headers = {
            "Accept": "application/json, text/javascript, */*;q=0.01",
            "Accept-Encoding": "gzip,deflate",
            "Accept-Language:": "zh-CN,zh;q=0.9,en;q=0.8",
            "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8",
            "Referer": "http://m.shenzhenair.com/webresource-micro/flightDyna.html",
            "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1"
        }
        yield scrapy.FormRequest(url=url,
                                 formdata={"flightNo": self.flightNo, "date": self.flightDate, "onoff": "false"},
                                 headers=headers)

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
