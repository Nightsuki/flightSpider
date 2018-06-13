# coding=utf-8
import json
import os
from time import sleep
from urllib import request

import scrapy
import logging

from ..Item.FeichangZhunItem import FeiChangZhunItem


class FeiChangZhunSpider(scrapy.Spider):
    name = "FeiChangZhun"
    yzm = ""

    def start_requests(self):
        flights = 'MU9152'
        date = "2018-06-06"
        url = "http://webapp.veryzhun.com/h5/flightsearch?fnum=" + flights + "&date=" + date + "&token" \
                                                                                               "=f1c9dae3737f47d45ceeb72cfa3c8094 "
        header = {
            "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML"
                          ", like Gecko) Version/11.0 Mobile/15A372 Safari/604.1"
        }
        yield scrapy.Request(url=url, callback=self.parse, headers=header)

    def parse(self, response):
        js = json.loads(response.body)
        if type(js) != list:
            if 'error_code' in js:
                yield scrapy.Request(url=response.url, callback=self.parse)
            # todo
            if 'code' in js and js['code'] == 401:
                # if js['msg'] == '验证码错误或已失效':
                if js['msg'] == '频繁查询请休息片刻':
                    sleep(10)

                localPath = '/capatcha/capatcha.jpg'
                request.urlretrieve(js['data']['limitYzmUrl'], localPath)
                # todo
                capatchaNum = input()
                self.yzm = capatchaNum
                # if js['msg'] == "您的请求过于频繁,请输入验证码":
                #     localPath = '/capatcha/capatcha.jpg'
                #     request.urlretrieve(js['data']['limitYzmUrl'], localPath)
                #     capatchaNum = input()
                #     self.yzm = capatchaNum
                yield scrapy.Request(url=response.url + "&limityzm=" + self.yzm, callback=self.parse)
        else:
            self.next(js)

        pass

    def next(self, js):
        print(js)
        for flight in js:
            item = FeiChangZhunItem()
            airline = flight['FlightNo']
            expDeptTime = flight['FlightDeptimePlanDate']
            expArrTime = flight['FlightArrtimePlanDate']
            actDeptTime = flight['FlightDeptimeReadyDate']
            actArrTime = flight['FlightArrtimeReadyDate']
            # 			航班状态 1：计划 2：起飞 3：到达 4：延误 5：取消 6：备降
            status = flight['FlightState']

            airlineCorp = flight['FlightCompany']
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
