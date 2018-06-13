# coding=utf-8
import json

import scrapy

from ..Item.HaiNanItems import HaiNanItems


class HaiNanSpider(scrapy.Spider):
    name = "HaiNan"

    def __init__(self, flightNo=None, flightDate=None, *args, **kwargs):
        super(HaiNanSpider, self).__init__(*args, **kwargs)
        self.flightNo = flightNo
        self.flightDate = flightDate

    def start_requests(self):
        url = "http://opcflt.hnair.com/hnairweb/flightJsonByNO.action"
        yield scrapy.FormRequest(url=url, formdata={"flightID": self.flightNo, "flightDate": self.flightDate},
                                 callback=self.parse)

    def parse(self, response):
        js = json.loads(response.body)
        flights = js['flightList']
        if flights is not None:
            for flight in flights:
                item = HaiNanItems()
                airline = flight['fltid'].replace(" ", "")
                expDeptTime = flight['etd']
                expArrTime = flight['eta']
                actDeptTime = flight['atd']
                actArrTime = flight['ata']
                status = flight['statusCN']

                airlineCorp = '海南航空'
                item['airline'] = airline
                item['airlineCorp'] = airlineCorp
                item['status'] = status
                item['expDeptTime'] = expDeptTime
                item['expArrTime'] = expArrTime
                item['actDeptTime'] = actDeptTime
                item['actArrTime'] = actArrTime
                yield item
