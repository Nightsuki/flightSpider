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

    def start_requests(self):
        url = 'http://www.airchina.com.cn/www/FlightEsbServlet.do?callback=&depDate=2018-06-04&departAirport' \
              '=&arrivedAirport=&companyCode=CA&flightNO=CA1832&requesttype=flight&language=CN&_=' + str(
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

        item['airlineCorp'] = airlineCorp
        # airline = selector.xpath('//*[@id="content"]/div/div/div[4]/table/tbody/tr/td[1]/span[2]/text()').extract()[0]
        item['airline'] = flightLegInfoEntity['flightNumber']
        item['expDeptTime'] = flightLegInfoEntity['scheduledDepartureDateTime']
        item['expArrTime'] = flightLegInfoEntity['scheduledArrivalDateTime']
        item['actDeptTime'] = flightLegInfoEntity['actualDepartureDateTime']
        item['actArrTime'] = flightLegInfoEntity['actualArrivalDateTime']
        item['status'] = flightLegInfoEntity['status']
        yield item

        pass
