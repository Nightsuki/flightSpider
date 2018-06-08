import json

import scrapy

from scrapy import Request

from ..Item.JiXiangItems import JiXiangItems


class JiXiangSpider(scrapy.Spider):
    name = 'JiXiang'

    def start_requests(self):
        url = 'http://www.juneyaoair.com/pages/reservemanage/flightReservation.aspx/QueryFlightStatus'
        alllines = []
        # for airline in alllines:
        #     yield scrapy.FormRequest(
        #         url=url,
        #         formdata={"searchType": "1", "flightNo": airline, "flightDate": "2018-06-04", "journeyType": "OW"},
        #         callback=self.parse
        #     )
        data = {
            "selectType": "1",
            "depCitycode": "",
            "arrCitycode": "",
            "flightNumber": "1256",
            "flightDate": "2"
        }
        yield Request(url, method="POST", body=json.dumps(data), headers={'Content-Type': 'application/json'},
                      callback=self.parse)

    def parse(self, response):
        item = JiXiangItems()
        airlineCorp = "吉祥航空"
        item['airlineCorp'] = airlineCorp
        js = json.loads(json.loads(response.body)['d'])
        airlineInfo = js['FlightInfoList'][0]
        airline = airlineInfo['FlightNo']
        item['airline'] = airline
        status = airlineInfo['FlightState']
        item['status'] = status
        expDeptTime = airlineInfo['FlightDeptimePlanDate']
        item['expDeptTime'] = expDeptTime
        expArrTime = airlineInfo['FlightArrtimePlanDate']
        item['expArrTime'] = expArrTime
        actDeptTime = airlineInfo['FlightDeptimeReadyDate']
        item['actDeptTime'] = actDeptTime
        actArrTime = airlineInfo['FlightArrtimeReadyDate']
        item['actArrTime'] = actArrTime
        yield item
        print(airline)

        pass
