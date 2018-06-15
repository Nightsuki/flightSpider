# coding=utf-8
import datetime
import json

import scrapy
from ..Item.NanFangItems import NanFangItems

# case "DLY" :
# 					result = [flLang.fs019,flLang.fs019]
# 				break;
# 				case "AIR" :
# 					result = [flLang.fs020,flLang.fs019]
# 				break;
# 				case "ARV" :
# 					result =  [flLang.fs020,flLang.fs020]
# 				break;
# 				case "SCH" :
# 					result = [flLang.fs019,flLang.fs019]
# 				break;
# 				case "ALT" :
# 					result =  [flLang.fs020,flLang.fs020]
# 				break;
# 				case "REV" :
# 					result =  [flLang.fs020,flLang.fs020]
statusMsg = {
    "DLY": "延误",
    "AIR": "起飞",
    "ARV": "到达",
    "SCH": "计划",
    "CNL": "取消",
    "ALT": "备降",
    "REV": "返航",

}


class NanFangSpider(scrapy.Spider):
    name = "NanFang"

    def __init__(self, flightNo=None, flightDate=None, *args, **kwargs):
        super(NanFangSpider, self).__init__(*args, **kwargs)
        self.flightNo = flightNo
        flightDate = datetime.datetime.strptime(flightDate, '%Y-%m-%d')
        flightDate = flightDate.strftime('%Y%m%d')
        self.flightDate = flightDate

    def start_requests(self):
        # flightNo = '3109'
        # flightDate = '20180606'
        url = "https://b2c.csair.com/B2C40/flight/flightDynamic.ao?date=" + self.flightDate + "&fltNr=" + self.flightNo[
                                                                                                          2:]
        yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        js = json.loads(response.body)
        flights = js['data']
        for flight in flights:
            item = NanFangItems()
            # print(str(flight))
            airline = flight['fltNr']
            expDeptTime = flight['crewDepDt']
            expArrTime = flight['crewArvDt']
            actDeptTime = flight['actDepDt']
            actArrTime = flight['actArvDt']
            # ARR 落地 NDR 落地 ATA 到达 CNL 取消 DEL 延误 DEP 起飞 RTR 返航 SCH 计划
            status = statusMsg[flight['fltSts']]
            airlineCorp = '南方航空'

            expDeptTime = datetime.datetime.strptime(expDeptTime,
                                                     '%Y-%m-%d %H:%M').strftime("%Y-%m-%d %H:%M:%S")
            expArrTime = datetime.datetime.strptime(expArrTime,
                                                    '%Y-%m-%d %H:%M').strftime("%Y-%m-%d %H:%M:%S")

            if actDeptTime != '':
                actDeptTime = datetime.datetime.strptime(actDeptTime, '%Y-%m-%d %H:%M').strftime("%Y-%m-%d %H:%M:%S")

            if actArrTime != '':
                actArrTime = datetime.datetime.strptime(actArrTime, '%Y-%m-%d %H:%M').strftime("%Y-%m-%d %H:%M:%S")

            item['airline'] = airline
            item['airlineCorp'] = airlineCorp
            item['status'] = status
            item['expDeptTime'] = expDeptTime
            item['expArrTime'] = expArrTime
            item['actDeptTime'] = actDeptTime
            item['actArrTime'] = actArrTime
            yield item
        pass
