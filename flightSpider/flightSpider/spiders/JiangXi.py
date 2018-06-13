import scrapy

from ..Item.JiangXiItems import JiangXiItems


class JiangXiSpider(scrapy.Spider):
    name = 'JiangXi'

    def __init__(self, flightNo=None, flightDate=None, *args, **kwargs):
        super(JiangXiSpider, self).__init__(*args, **kwargs)
        self.flightNo = flightNo
        self.flightDate = flightDate

    def start_requests(self):
        url = 'http://www.airjiangxi.com/jiangxiair/flight-dynamic/flightSearch.action?flightTabs=1&flightNo=' + self.flightNo + '&depDate=' + self.flightDate
        yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        selector = scrapy.Selector(response)
        flights = selector.css("table:nth-child(n+1)")
        for flight in flights:
            item = JiangXiItems()
            # print(flight.xpath("//text()").extract()[0])
            # text = flight.xpath("./td[2]/text()").extract_first()
            airline = flight.xpath("//td[1]/text()").extract_first()
            expDeptTime = flight.xpath("//td[3]/text()").extract_first()
            expArrTime = flight.xpath("//td[7]/text()").extract_first()
            actDeptTime = flight.xpath("//td[5]/text()").extract_first()
            actArrTime = flight.xpath("//td[9]/text()").extract_first()
            status = flight.xpath("//td[11]/text()").extract_first()
            airlineCorp = '江西航空'
            item['airline'] = airline
            item['airlineCorp'] = airlineCorp
            item['status'] = status
            item['expDeptTime'] = expDeptTime
            item['expArrTime'] = expArrTime
            item['actDeptTime'] = actDeptTime
            item['actArrTime'] = actArrTime
            yield item
        pass
