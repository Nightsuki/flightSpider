import datetime
import json
import re
import time
from urllib import parse

import scrapy
from scrapy import Request
from ..Item.GuoHangItems import GuoHangItems


class GuoHangSpider(scrapy.Spider):
    name = 'GuoHang'

    # start_urls = [
    #     'http://www.airchina.com.cn/www/FlightEsbServlet.do?callback=&depDate=2018-06-04&departAirport'
    #     '=&arrivedAirport=&companyCode=CA&flightNO=CA1832&requesttype=flight&language=CN&_=1528093713176']
    def __init__(self, flightNo=None, flightDate=None, *args, **kwargs):
        super(GuoHangSpider, self).__init__(*args, **kwargs)
        self.flightNo = flightNo
        self.flightDate = flightDate

    def start_requests(self):
        url = 'http://www.airchina.com.cn/www/FlightEsbServlet.do?callback=&depDate=' + self.flightDate + '&departAirport' \
                                                                                                          '=&arrivedAirport=&companyCode=CA&flightNO=' + self.flightNo + '&requesttype=flight&language=CN&_=' + str(
            int(round(time.time() * 1000)))
        headers = {
            'User-Agent': 'Mozilla/5.0(Macintosh;U;IntelMacOSX10_6_8;en-us)AppleWebKit/534.50(KHTML,likeGecko)Version/5.1Safari/534.50'
        }
        yield Request(url, headers=headers, callback=self.parse)

    def parse(self, response):
        airlineCorp = '中国国际航空'
        item = GuoHangItems()
        js = response.body.decode('utf-8')
        pattern = re.compile(r'^\(\'(.*)\'\)\;$')

        match = pattern.match(js)
        if match:
            js = match.group(1)
        js = parse.unquote(js).replace("+", " ")
        js = json.loads(js)
        flightInfoDetailEntity = js[0]['flightInfoDetailEntity'][0]
        # flightInfoDetailEntity = flightInfoDetailEntity['flightInfoDetailEntity']
        flightLegInfoEntity = flightInfoDetailEntity['flightLegInfoEntity'][0]
        print(flightLegInfoEntity)

        airlineCorp = airlineCorp
        airline = flightLegInfoEntity['flightNumber']
        expDeptTime = datetime.datetime.strptime(flightLegInfoEntity['scheduledDepartureDateTime'],
                                                 '%Y-%m-%d %H:%M').strftime("%Y-%m-%d %H:%M:%S")
        expArrTime = datetime.datetime.strptime(flightLegInfoEntity['scheduledArrivalDateTime'],
                                                '%Y-%m-%d %H:%M').strftime("%Y-%m-%d %H:%M:%S")

        actDeptTime = flightLegInfoEntity['actualDepartureDateTime']
        if actDeptTime != '--':
            actDeptTime = datetime.datetime.strptime(actDeptTime, '%Y-%m-%d %H:%M').strftime("%Y-%m-%d %H:%M:%S")

        actArrTime = flightLegInfoEntity['actualArrivalDateTime']
        if actArrTime != '--':
            actArrTime = datetime.datetime.strptime(actArrTime, '%Y-%m-%d %H:%M').strftime("%Y-%m-%d %H:%M:%S")
        status = flightLegInfoEntity['status']

        item['airline'] = airline
        item['expDeptTime'] = expDeptTime
        item['airlineCorp'] = airlineCorp
        item['expArrTime'] = expArrTime
        item['status'] = status
        item['actDeptTime'] = actDeptTime
        item['actArrTime'] = actArrTime
        yield item
