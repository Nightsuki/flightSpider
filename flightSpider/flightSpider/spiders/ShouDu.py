import json

import scrapy

from ..Item.ShouDuItems import ShouDuItems


class ShouDuSpider(scrapy.Spider):
    name = "ShouDu"

    def __init__(self, flightNo=None, flightDate=None, *args, **kwargs):
        super(ShouDuSpider, self).__init__(*args, **kwargs)
        self.flightNo = flightNo
        self.flightDate = flightDate

    # def start_requests(self):
    #     url = "http://www.jdair.net/b2c-flight/searchFocFlight.action"
    #     yield scrapy.Request(url=url, callback=self.parse)

    def start_requests(self):
        # selector = scrapy.Selector(response)
        # _desc = selector.xpath('//input[@id="desc"]/@value')
        # _desc = _desc.extract()
        UserAgent = "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36"
        _desc = "coBPtm4BZy5Ly7E1arnljyaRRakttM4KWG9nCgl82GiylHlwYc%2BQbC0c2oGzS8TE"
        url = "http://www.jdair.net/focflight/ajax/getFocFlight.action"
        yield scrapy.FormRequest(url=url,
                                 formdata={"desc": _desc, "focType": "flight", "depTime_f": self.flightDate,
                                           "flightNo": self.flightNo},
                                 callback=self.parse,
                                 headers={"User-Agent": UserAgent})

    def parse(self, response):
        js = json.loads(response.body)
        flights = js['FocFlightList']
        for flight in flights:
            item = ShouDuItems()
            airline = flight['flightNo']
            expDeptTime = flight['stdChn']
            expArrTime = flight['staChn']
            actDeptTime = flight['atdChn']
            actArrTime = flight['tDwnChn']
            # ARR 落地 NDR 落地 ATA 到达 CNL 取消 DEL 延误 DEP 起飞 RTR 返航 SCH 计划
            status = flight['status']

            airlineCorp = '首都航空'
            item['airline'] = airline
            item['airlineCorp'] = airlineCorp
            item['status'] = status
            item['expDeptTime'] = expDeptTime
            item['expArrTime'] = expArrTime
            item['actDeptTime'] = actDeptTime
            item['actArrTime'] = actArrTime
            yield item
