import json

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
        flights = js['data']['fds']
        for flight in flights:
            item = GuiZhouItems()
            airline = flight['flightNo']
            expDeptTime = flight['departureTime']
            expArrTime = flight['arrivalTime']
            actDeptTime = flight['actualDepartureTime']
            actArrTime = flight['actualArrivalTime']
            status = flight['status']

            airlineCorp = '多彩贵州航空'
            item['airline'] = airline
            item['airlineCorp'] = airlineCorp
            item['status'] = status
            item['expDeptTime'] = expDeptTime
            item['expArrTime'] = expArrTime
            item['actDeptTime'] = actDeptTime
            item['actArrTime'] = actArrTime
            yield item
            return item
