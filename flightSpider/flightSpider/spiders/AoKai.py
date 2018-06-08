import scrapy

from ..Item.AoKaiItems import AoKaiItems


class AoKaiSpider(scrapy.Spider):
    name = 'AoKai'
    start_urls = [
        'http://okair.feeyo.com/flightDynamic/index.php?fnum='
    ]

    def parse(self, response):
        selector = scrapy.Selector(response)
        flights = selector.css('.top_cx_col1 ')
        for flight in flights:
            item = AoKaiItems()
            airlineCorp = "奥凯航空"
            item['airlineCorp'] = airlineCorp
            airline = flight.css(".d1::text").extract_first()
            item['airline'] = airline
            expDeptTime = flight.css(".d5::text").extract_first()
            item['expDeptTime'] = expDeptTime
            expArrTime = flight.css(".d5 ::text").extract()[1]
            item['expArrTime'] = expArrTime
            actDeptTime = flight.css(".d6 ::text").extract_first()
            item['actDeptTime'] = actDeptTime
            actArrTime = flight.css(".d6 ::text").extract()[1]
            item['actArrTime'] = actArrTime
            status = flight.css(".d7 span::text").extract_first()
            item['status'] = status
            yield item
        next_page = selector.css('div.pages .nextprev:last-child::attr(href)').extract_first()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)
