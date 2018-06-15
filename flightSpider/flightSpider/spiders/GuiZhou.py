import datetime
import json
import logging

import scrapy

from ..Item.GuiZhouItems import GuiZhouItems


class GuiZhou(scrapy.Spider):
    name = "GuiZhou"

    # flightNo = "GY7107"
    # flightDate = "2018-06-06"

    def __init__(self, flightNo=None, flightDate=None, *args, **kwargs):
        super(GuiZhou, self).__init__(*args, **kwargs)
        self.flightNo = flightNo
        self.flightDate = flightDate

    def start_requests(self):
        url = "http://www.dcair.com.cn/yss/flight-dynamics/search"
        yield scrapy.FormRequest(url=url, formdata={"depCityCode": "", "arrCityCode": "", "flightNo": self.flightNo,
                                                    "flightDate": self.flightDate}, callback=self.parse)

    def parse(self, response):
        js = json.loads(response.body)
        logging.info(js)
        flightDate = datetime.datetime.strptime(self.flightDate, '%Y-%m-%d')
        flights = js['data']['fds']
        for flight in flights:
            item = GuiZhouItems()
            airline = flight['flightNo']
            expDeptTime = flight['departureTime']
            expArrTime = flight['arrivalTime']
            actDeptTime = flight['actualDepartureTime']
            actDeptTimeStr = actDeptTime
            actArrTime = flight['actualArrivalTime']
            status = flight['status']

            airlineCorp = '多彩贵州航空'

            expDeptTime = datetime.datetime(flightDate.year, flightDate.month, flightDate.day,
                                            int(expDeptTime.split(':')[0]),
                                            int(expDeptTime.split(':')[1]))
            expArrTime = datetime.datetime(flightDate.year, flightDate.month, flightDate.day,
                                           int(expArrTime.split(':')[0]),
                                           int(expArrTime.split(':')[1]))
            if expDeptTime > expArrTime:
                expArrTime = expArrTime + datetime.timedelta(days=1)
            if actDeptTime is not None:
                actDeptTime = datetime.datetime(flightDate.year, flightDate.month, flightDate.day,
                                                int(actDeptTime.split(':')[0]),
                                                int(actDeptTime.split(':')[1]))
                actDeptTimeStr = actDeptTime.strftime("%Y-%m-%d %H:%M:%S")
            if actArrTime is not None:
                actArrTime = datetime.datetime(flightDate.year, flightDate.month, flightDate.day,
                                               int(actArrTime.split(':')[0]),
                                               int(actArrTime.split(':')[1]))
                if actDeptTime > actArrTime:
                    actArrTime = actArrTime + datetime.timedelta(days=1)
                    actArrTime = actArrTime.strftime("%Y-%m-%d %H:%M:%S")
            item['airline'] = airline
            item['airlineCorp'] = airlineCorp
            item['status'] = status
            item['expDeptTime'] = expDeptTime
            item['expArrTime'] = expArrTime
            item['actDeptTime'] = actDeptTimeStr
            item['actArrTime'] = actArrTime
            yield item
