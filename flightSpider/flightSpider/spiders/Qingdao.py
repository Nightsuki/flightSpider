import datetime

import scrapy

from ..Item.QingdaoItems import QingdaoItems


class QingDaoSpider(scrapy.Spider):
    name = 'QingDao'

    def __init__(self, flightNo=None, flightDate=None, *args, **kwargs):
        super(QingDaoSpider, self).__init__(*args, **kwargs)
        self.flightNo = flightNo
        self.flightDate = flightDate

    def start_requests(self):
        url = 'http://www.qdairlines.com/queryFlightStatus.do'
        # alllines = ['QW6001', 'QW6002', 'QW6003', 'QW6004', 'QW6007', 'QW6008', 'QW6011', 'QW6012', 'QW6021', 'QW9775',
        #             'QW9779', 'QW9785', 'QW9786', 'QW9789', 'QW9793', 'QW9794', 'QW9795', 'QW9796', 'QW9799', 'QW9800',
        #             'QW9803', 'QW9804', 'QW9805', 'QW9807', 'QW9808', 'QW9811', 'QW9815', 'QW9817', 'QW9819', 'QW9833',
        #             'QW9843', 'QW9844', 'QW9853', 'QW9865', 'QW9866', 'QW9877', 'QW9878', 'QW9881', 'QW9889', 'QW6005',
        #             'QW9771']
        # for airline in alllines:
        yield scrapy.FormRequest(
            url=url,
            formdata={"searchType": "1", "flightNo": self.flightNo, "flightDate": self.flightDate, "journeyType": "OW"},
            callback=self.parse
        )

    def parse(self, response):
        item = QingdaoItems()
        flightDate = datetime.datetime.strptime(self.flightDate, '%Y-%m-%d')
        selector = scrapy.Selector(response)
        flights = selector.xpath('//*[@id="content"]/div/div/div[4]/table/tbody/tr')
        for flight in flights:
            airlineCorp = flight.xpath('./td[1]/span[1]/text()').extract_first()
            airline = flight.xpath('./td[1]/span[2]/text()').extract_first()
            expDeptTime = flight.xpath('./td[2]/span[1]/text()').extract_first()
            expArrTime = flight.xpath('./td[2]/span[2]/text()').extract_first()
            actDeptTime = flight.xpath('./td[3]/span[1]/text()').extract_first()
            actDeptTimeStr = actDeptTime
            actArrTime = flight.xpath('./td[3]/span[2]/text()').extract_first()
            expDeptTime = datetime.datetime(flightDate.year, flightDate.month, flightDate.day,
                                            int(expDeptTime.split(':')[0]),
                                            int(expDeptTime.split(':')[1]))
            expArrTime = datetime.datetime(flightDate.year, flightDate.month, flightDate.day,
                                           int(expArrTime.split(':')[0]),
                                           int(expArrTime.split(':')[1]))
            if expDeptTime > expArrTime:
                expArrTime = expArrTime + datetime.timedelta(days=1)
            if actDeptTime != '-':
                actDeptTime = datetime.datetime(flightDate.year, flightDate.month, flightDate.day,
                                                int(actDeptTime.split(':')[0]),
                                                int(actDeptTime.split(':')[1]))
                actDeptTime = actDeptTime
                actDeptTimeStr = actDeptTime.strftime("%Y-%m-%d %H:%M:%S")
            if actArrTime != '-':
                actArrTime = datetime.datetime(flightDate.year, flightDate.month, flightDate.day,
                                               int(actArrTime.split(':')[0]),
                                               int(actArrTime.split(':')[1]))
                if actDeptTime > actArrTime:
                    actArrTime = actArrTime + datetime.timedelta(days=1)
                    actArrTime = actArrTime.strftime("%Y-%m-%d %H:%M:%S")
            status = flight.xpath('./td[4]/span/text()').extract_first().replace("\r", "").replace("\t", "").replace(
                "\n", "")
            item['airline'] = airline
            item['expDeptTime'] = expDeptTime.strftime("%Y-%m-%d %H:%M:%S")
            item['airlineCorp'] = airlineCorp
            item['expArrTime'] = expArrTime.strftime("%Y-%m-%d %H:%M:%S")
            item['status'] = status
            item['actDeptTime'] = actDeptTimeStr
            item['actArrTime'] = actArrTime
            yield item
