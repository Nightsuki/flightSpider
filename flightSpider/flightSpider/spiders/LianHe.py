import datetime
import json
import re
import time
from urllib import parse

import scrapy
from ..Item.LianHeItems import LianHeItems


class LianHeSpider(scrapy.Spider):
    name = "LianHe"

    def __init__(self, flightNo=None, flightDate=None, *args, **kwargs):
        super(LianHeSpider, self).__init__(*args, **kwargs)
        self.flightNo = flightNo
        flightDate = datetime.datetime.strptime(flightDate, '%Y-%m-%d').date()
        today = datetime.date.today()
        yesterday = today + datetime.timedelta(days=-1)  # 减去一天
        tomorrow = today + datetime.timedelta(days=+1)  # 减去一天
        if flightDate == yesterday:
            self.flightDate = '-'
        elif flightDate == today:
            self.flightDate = '.'
        elif flightDate == tomorrow:
            self.flightDate = '+'
        else:
            self.flightDate = '.'

    def start_requests(self):
        # flightNo = "5921"
        # flightTime -昨天  +明天  .今天
        url = "http://www.flycua.com/addservice/new-aoc!queryNewFlightStatus.shtml?qType=" \
              "0&flightTime=" + self.flightDate + "&queryCxr=KN&queryFlightno=" + self.flightNo[2:] + "&_=" + str(
            int(round(time.time() * 1000)))
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
