# coding=utf-8
import scrapy

from ..Item.XiZangItems import XiZangItems


class XiZangSpider(scrapy.Spider):
    name = 'XiZang'

    def __init__(self, flightNo=None, flightDate=None, *args, **kwargs):
        super(XiZangSpider, self).__init__(*args, **kwargs)
        self.flightNo = flightNo
        self.flightDate = flightDate

    def start_requests(self):
        # flightNO = 'TV6019'
        # flightDate = '2018-06-07'
        url = 'https://www.tibetairlines.com.cn/tibetair/foc/findByFltNos.do?flightNO=' + self.flightNo + '&flightDate=' + self.flightDate
        yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        selector = scrapy.Selector(response)
        flights = selector.css("tr[class='changeColor']")
        for flight in flights:
            item = XiZangItems()
            airlineCorp = '西藏航空'
            # print(selector.extract())
            airline = flight.xpath('./td[1]/text()').extract_first()
            expDeptTime = flight.xpath('./td[4]/text()').extract_first()
            expArrTime = flight.xpath('./td[9]/text()').extract_first()
            actDeptTime = flight.xpath('./td[6]/text()').extract_first()
            actArrTime = flight.xpath('./td[11]/text()').extract_first()
            status = flight.xpath('./td[12]/text()').extract_first()
            item['airline'] = airline
            item['airlineCorp'] = airlineCorp
            item['status'] = status
            item['expDeptTime'] = expDeptTime
            item['expArrTime'] = expArrTime
            item['actDeptTime'] = actDeptTime
            item['actArrTime'] = actArrTime
            yield item
        pass
