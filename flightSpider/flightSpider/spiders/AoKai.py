import datetime

import scrapy

from ..Item.AoKaiItems import AoKaiItems


class AoKaiSpider(scrapy.Spider):
    name = 'AoKai'

    def start_requests(self):
        url = 'http://okair.feeyo.com/flightDynamic/index.php?fnum=' + self.flightNo
        yield scrapy.Request(url=url, callback=self.parse)

    def __init__(self, flightNo=None, flightDate=None, *args, **kwargs):
        super(AoKaiSpider, self).__init__(*args, **kwargs)
        self.flightNo = flightNo
        self.flightDate = flightDate

    def parse(self, response):
        selector = scrapy.Selector(response)
        flightDate = datetime.datetime.strptime(self.flightDate, '%Y-%m-%d')
        flights = selector.css('.top_cx_col1 ')
        for flight in flights:
            item = AoKaiItems()
            airlineCorp = "奥凯航空"
            airline = flight.css(".d1::text").extract_first()
            expDeptTime = flight.css(".d5::text").extract_first()
            expArrTime = flight.css(".d5 ::text").extract()[1]
            actDeptTime = flight.css(".d6 ::text").extract_first()
            actDeptTimeStr = actDeptTime
            actArrTime = flight.css(".d6 ::text").extract()[1]
            status = flight.css(".d7 span::text").extract_first()

            expDeptTime = datetime.datetime(flightDate.year, flightDate.month, flightDate.day,
                                            int(expDeptTime.split(':')[0]),
                                            int(expDeptTime.split(':')[1]))
            expArrTime = datetime.datetime(flightDate.year, flightDate.month, flightDate.day,
                                           int(expArrTime.split(':')[0]),
                                           int(expArrTime.split(':')[1]))
            if expDeptTime > expArrTime:
                expArrTime = expArrTime + datetime.timedelta(days=1)
            if actDeptTime != '':
                actDeptTime = datetime.datetime(flightDate.year, flightDate.month, flightDate.day,
                                                int(actDeptTime.split(':')[0]),
                                                int(actDeptTime.split(':')[1]))
                actDeptTimeStr = actDeptTime.strftime("%Y-%m-%d %H:%M:%S")
            if actArrTime != '':
                actArrTime = datetime.datetime(flightDate.year, flightDate.month, flightDate.day,
                                               int(actArrTime.split(':')[0]),
                                               int(actArrTime.split(':')[1]))
                if actDeptTime > actArrTime:
                    actArrTime = actArrTime + datetime.timedelta(days=1)
                    actArrTime = actArrTime.strftime("%Y-%m-%d %H:%M:%S")

            item['airlineCorp'] = airlineCorp
            item['airline'] = airline
            item['expDeptTime'] = expDeptTime
            item['expArrTime'] = expArrTime
            item['actDeptTime'] = actDeptTimeStr
            item['actArrTime'] = actArrTime
            item['status'] = status
            yield item
        # next_page = selector.css('div.pages .nextprev:last-child::attr(href)').extract_first()
        # if next_page is not None:
        #     next_page = response.urljoin(next_page)
        #     yield scrapy.Request(next_page, callback=self.parse)
