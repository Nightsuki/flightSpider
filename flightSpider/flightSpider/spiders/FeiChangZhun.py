# coding=utf-8
import datetime
import json
import re
from time import sleep
from urllib import request

import scrapy
from PIL import Image
from pytesseract import pytesseract

from ..Item.FeichangZhunItem import FeiChangZhunItem


def convert_Image(img, standard=127.5):
    image = img.convert('L')
    pixels = image.load()
    for x in range(image.width):
        for y in range(image.height):
            if pixels[x, y] > standard:
                pixels[x, y] = 255
            else:
                pixels[x, y] = 0
    return image


class FeiChangZhunSpider(scrapy.Spider):
    name = "FeiChangZhun"
    yzm = ""
    header = {
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML"
                      ", like Gecko) Version/11.0 Mobile/15A372 Safari/604.1"
    }

    def __init__(self, flightNo=None, flightDate=None, *args, **kwargs):
        super(FeiChangZhunSpider, self).__init__(*args, **kwargs)
        self.flightNo = flightNo
        self.flightDate = flightDate
        self.url = "http://webapp.veryzhun.com/h5/flightsearch?fnum=" + self.flightNo + "&date=" + self.flightDate + "&token" \
                                                                                                                     "=f1c9dae3737f47d45ceeb72cfa3c8094 "

    def start_requests(self):

        header = {
            "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML"
                          ", like Gecko) Version/11.0 Mobile/15A372 Safari/604.1"
        }
        yield scrapy.Request(url=self.url, callback=self.parse, headers=header)

        # flights = [
        #     'QW9772', 'QW9772', 'QW6012', 'QW6007', 'QW6001', 'QW6004', 'QW6003', 'QW6011', 'QW6008', 'QW6002',
        #     'QW9779',
        #     'QW9775', 'QW9785', 'QW9786', 'QW9793', 'QW9794', 'QW9795', 'QW9796', 'QW9805', 'QW9807', 'QW9808',
        #     'QW9817',
        #     'QW9811', 'QW9815', 'QW9844', 'QW9833', 'QW9819', 'QW9843', 'QW9865', 'QW9881', 'QW9878', 'QW9866',
        #     'QW9877',
        #     'QW9889', 'QW6005', 'QW9771', 'HO1256', 'CA1832 '
        # ]
        # date = "2018-06-06"
        # for flightNo in flights:
        #
        #     if self.yzm == '':
        #         url = "http://webapp.veryzhun.com/h5/flightsearch?fnum=" + flightNo + "&date=" + date + "&token" \
        #                                                                                                 "=f1c9dae3737f47d45ceeb72cfa3c8094 "
        #         yield scrapy.Request(url=url, callback=self.parse, headers=self.header)
        #     else:
        #         url = "http://webapp.veryzhun.com/h5/flightsearch?fnum=" + flightNo + "&date=" + date + "&token" \
        #                                                                                                 "=f1c9dae3737f47d45ceeb72cfa3c8094 "
        #         yield scrapy.Request(url=url + "&limityzm=" + self.yzm, callback=self.parse, headers=self.header)

    def parse(self, response):
        js = json.loads(response.body)
        if type(js) != list:
            if 'error_code' in js:
                yield scrapy.Request(url=self.url, callback=self.parse, headers=self.header)
            # todo
            if 'code' in js and js['code'] == 401:
                # if js['msg'] == '验证码错误或已失效':

                if self.yzm == '' or js['msg'] == '频繁查询请休息片刻' or js['msg'] == '验证码错误或已失效':
                    if js['msg'] == '频繁查询请休息片刻':
                        sleep(10)
                    localPath = '/capatcha/capatcha.jpg'
                    request.urlretrieve(js['data']['limitYzmUrl'], localPath)
                    # todo
                    img = Image.open(localPath)
                    img = convert_Image(img)
                    # img.show()
                    testdata_dir_config = '--tessdata-dir "C:\\Program Files (x86)\\Tesseract-OCR\\tessdata"'
                    capatchaNum = pytesseract.image_to_string(img, config=testdata_dir_config)
                    # 去掉非法字符，只保留字母数字
                    capatchaNum = re.sub("\W", "", capatchaNum)
                    # capatchaNum = input()
                    self.yzm = capatchaNum
                yield scrapy.Request(url=self.url + "&limityzm=" + self.yzm, callback=self.parse,
                                     headers=self.header)
        else:
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
                item['airline'] = airline
                item['airlineCorp'] = airlineCorp
                item['status'] = status
                item['expDeptTime'] = expDeptTime
                item['expArrTime'] = expArrTime
                item['actDeptTime'] = actDeptTime
                item['actArrTime'] = actArrTime
                yield item
