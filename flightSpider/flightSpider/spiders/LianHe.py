import json
import re
import time
from urllib import parse

import scrapy
from ..Item.LianHeItems import LianHeItems


class LianHeSpider(scrapy.Spider):
    name = "LianHe"

    def start_requests(self):
        flightNo = "5921"
        # flightTime -昨天  +明天  .今天
        url = "http://www.flycua.com/addservice/new-aoc!queryNewFlightStatus.shtml?qType=" \
              "0&flightTime=.&queryCxr=KN&queryFlightno=" + flightNo + "&_=" + str(int(round(time.time() * 1000)))
        yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        airlineCorp = '联合航空'
        item = LianHeItems()
        js = response.body.decode('utf-8')
        pattern = re.compile('\s*flightAoc.showData\((.*)\);$')
        match = pattern.match(js)
        if match:
            js = match.group(1)
        js = json.loads(js)
        flights = js[0]['actualFlightShowList']
        # flightInfoDetailEntity = flightInfoDetailEntity['flightInfoDetailEntity']
        for flight in flights:
            item['airlineCorp'] = airlineCorp
            item['airline'] = flight['flightno']
            item['expDeptTime'] = flight['std']
            item['expArrTime'] = flight['sta']
            item['actDeptTime'] = flight['atd']
            item['actArrTime'] = flight['ata']
            item['status'] = flight['status']
            yield item
        pass
