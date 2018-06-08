# coding=utf-8
import json
import os
from time import sleep
from urllib import request

import scrapy
import logging


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

    # def start_requests(self):
    #     flights = ['QW6001', 'QW6002', 'QW6003', 'QW6004', 'QW6007', 'QW6008', 'QW6011', 'QW6012', 'QW6021', 'QW9775',
    #                'QW9779', 'QW9785', 'QW9786', 'QW9789', 'QW9793', 'QW9794', 'QW9795', 'QW9796', 'QW9799', 'QW9800',
    #                'QW9803', 'QW9804', 'QW9805', 'QW9807', 'QW9808', 'QW9811', 'QW9815', 'QW9817', 'QW9819', 'QW9833',
    #                'QW9843', 'QW9844', 'QW9853', 'QW9865', 'QW9866', 'QW9877', 'QW9878', 'QW9881', 'QW9889', 'QW6005',
    #                'QW9771']
    #     date = "2018-06-06"
    #     header = {
    #         "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML"
    #                       ", like Gecko) Version/11.0 Mobile/15A372 Safari/604.1"
    #     }
    #     for flight in flights:
    #         url = "http://webapp.veryzhun.com/h5/flightsearch?fnum=" + flight + "&date=" + date + "&token" \
    #                                                                                               "=f1c9dae3737f47d45ceeb72cfa3c8094 "
    #         yield scrapy.Request(url=url,headers=header, callback=self.parse)

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
        pass
