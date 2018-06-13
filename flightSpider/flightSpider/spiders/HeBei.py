# coding=utf-8
import json

import scrapy
from scrapy.http.response import xml

# if (json[i].atd != null) {
# json[i].state = "起飞";
# } else if (json[i].state == "0") {
# json[i].state = "计划";
# } else if (json[i].state == "1") {
# json[i].state = "延误";
# } else if (json[i].state == "2") {
# json[i].state = "备降";
# } else if (json[i].state == "3") {
# json[i].state = "取消";
# }
# if (json[i].ata != null) {
# json[i].state = "到达";
# }
from ..Item.HeBeiItems import HeBeiItems

statusMsg = {
    "0": "计划",
    "1": "延误",
    "2": "备降",
    "3": "取消",
}


class HeBeiSpider(scrapy.Spider):
    name = "HeBei"

    def __init__(self, flightNo=None, flightDate=None, *args, **kwargs):
        super(HeBeiSpider, self).__init__(*args, **kwargs)
        self.flightNo = flightNo
        self.flightDate = flightDate

    def start_requests(self):

        url = "http://www.hbhk.com.cn/webapi/flight/status?date=" + self.flightDate + "&fltNum=" + self.flightNo
        yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        selector = scrapy.Selector(text=response.body)
        flights = json.loads(response.body)
        for flight in flights:
            item = HeBeiItems()
            airlineCorp = '河北航空'
            # print(selector.extract())
            # airline = flight.xpath('./fltnum/text()').extract_first()
            # expDeptTime = flight.xpath('./std/text()').extract_first()
            # expArrTime = flight.xpath('./sta/text()').extract_first()
            # actDeptTime = flight.xpath('./atd/text()').extract_first()
            # actArrTime = flight.xpath('./ata/text()').extract_first()
            # status = flight.xpath('./state/text()').extract_first()
            airline = flight['fltNum']
            expDeptTime = flight['std']
            expArrTime = flight['sta']
            actDeptTime = flight['atd']
            actArrTime = flight['ata']
            status = flight['state']
            if actDeptTime != '':
                status = '起飞'
            if actArrTime != '':
                status = '到达'
            else:
                status = statusMsg[status]
            item['airline'] = airline
            item['airlineCorp'] = airlineCorp
            item['status'] = status
            item['expDeptTime'] = expDeptTime
            item['expArrTime'] = expArrTime
            item['actDeptTime'] = actDeptTime
            item['actArrTime'] = actArrTime
            yield item
        pass
