# coding=utf-8
import json

import scrapy

from ..Item.DongFangItems import DongFangItems


class DongFangSpider(scrapy.Spider):
    name = "DongFang"

    def start_requests(self):
        url = "https://m.ceair.com/mobile/aoc/aoc!flightInfoDetail.shtml"
        flightNo = 'MU5101'
        flightDate = '2018-06-06'
        UA = 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) ' \
             'Version/11.0 Mobile/15A372 Safari/604.1 '
        yield scrapy.FormRequest(
            url=url,
            headers={'User-Agent': UA},
            formdata={"cond.queryFlightno": flightNo[2:], "cond.queryFlightDate": flightDate, "queryCxr": "MU",
                      "transitTag": "undefined"},
            callback=self.parse
        )

    def parse(self, response):
        js = json.loads(response.body)
        flight = js['flightDetail']
        print(str(flight))
        item = DongFangItems()
        airline = flight['flightNoDisp'].replace("&", "")
        expDeptTime = flight['planDeptTime']
        expArrTime = flight['planArrTime']
        actDeptTime = flight['realDeptTime']
        actArrTime = flight['realArrTime']
        # ARR 落地 NDR 落地 ATA 到达 CNL 取消 DEL 延误 DEP 起飞 RTR 返航 SCH 计划
        status = flight['statusCode']

        airlineCorp = '东方航空'
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
