import scrapy

from ..Item.ChengDuItems import ChengDuItems


class ChengDuSpider(scrapy.Spider):
    name = "ChengDu"

    def start_requests(self):
        url = "http://www.chengduair.cc/service_4.asp"
        formData = {
            "hbh": "2251",
            "hbtime": "2018/6/7",
            "subform.x": "35",
            "subform.y": "3"
        }
        yield scrapy.FormRequest(url=url, formdata=formData, callback=self.parse)

    def parse(self, response):
        selector = scrapy.Selector(response)
        text = selector.extract()
        flights = selector.css("table[bgcolor='#999999']>tr[align='center']")
        for flight in flights:
            item = ChengDuItems()
            airline = flight.css("td:nth-child(1)::text").extract_first(default='')
            expDeptTime = flight.css("td:nth-child(3)::text").extract_first(default='')
            expArrTime = flight.css("td:nth-child(6)::text").extract_first(default='')
            actDeptTime = flight.css("td:nth-child(5)::text").extract_first(default='')
            actArrTime = flight.css("td:nth-child(8)::text").extract_first(default='')
            status = flight.css("td:nth-child(9)::text").extract_first(default='')
            airlineCorp = '成都航空'

            item['airline'] = airline
            item['airlineCorp'] = airlineCorp
            item['status'] = status
            item['expDeptTime'] = expDeptTime
            item['expArrTime'] = expArrTime
            item['actDeptTime'] = actDeptTime
            item['actArrTime'] = actArrTime
            yield item
        pass
