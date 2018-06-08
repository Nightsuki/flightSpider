import scrapy

from ..Item.QingdaoItems import QingdaoItems


class QingDaoSpider(scrapy.Spider):
    name = 'Qingdao'

    def start_requests(self):
        url = 'http://www.qdairlines.com/queryFlightStatus.do'
        alllines = ['QW6001', 'QW6002', 'QW6003', 'QW6004', 'QW6007', 'QW6008', 'QW6011', 'QW6012', 'QW6021', 'QW9775',
                    'QW9779', 'QW9785', 'QW9786', 'QW9789', 'QW9793', 'QW9794', 'QW9795', 'QW9796', 'QW9799', 'QW9800',
                    'QW9803', 'QW9804', 'QW9805', 'QW9807', 'QW9808', 'QW9811', 'QW9815', 'QW9817', 'QW9819', 'QW9833',
                    'QW9843', 'QW9844', 'QW9853', 'QW9865', 'QW9866', 'QW9877', 'QW9878', 'QW9881', 'QW9889', 'QW6005',
                    'QW9771']
        for airline in alllines:
            yield scrapy.FormRequest(
                url=url,
                formdata={"searchType": "1", "flightNo": airline, "flightDate": "2018-06-04", "journeyType": "OW"},
                callback=self.parse
            )

    def parse(self, response):
        item = QingdaoItems()
        selector = scrapy.Selector(response)
        airlineCorp = selector.xpath('//*[@id="content"]/div/div/div[4]/table/tbody/tr/td[1]/span[1]/text()').extract()[
            0]
        item['airlineCorp'] = airlineCorp
        airline = selector.xpath('//*[@id="content"]/div/div/div[4]/table/tbody/tr/td[1]/span[2]/text()').extract()[0]
        item['airline'] = airline
        expDeptTime = selector.xpath('//*[@id="content"]/div/div/div[4]/table/tbody/tr/td[2]/span[1]/text()').extract()[
            0]
        item['expDeptTime'] = expDeptTime
        expArrTime = selector.xpath('//*[@id="content"]/div/div/div[4]/table/tbody/tr/td[2]/span[2]/text()').extract()[
            0]
        item['expArrTime'] = expArrTime
        actDeptTime = selector.xpath('//*[@id="content"]/div/div/div[4]/table/tbody/tr/td[3]/span[1]/text()').extract()[
            0]
        item['actDeptTime'] = actDeptTime
        actArrTime = selector.xpath('//*[@id="content"]/div/div/div[4]/table/tbody/tr/td[3]/span[1]/text()').extract()[
            0]
        item['actArrTime'] = actArrTime
        status = selector.xpath('//*[@id="content"]/div/div/div[4]/table/tbody/tr/td[4]/span/text()').extract()[
            0].replace("\r", "").replace("\t", "").replace("\n", "")
        item['status'] = status
        yield item
        print(airlineCorp)

        pass
