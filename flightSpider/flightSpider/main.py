from scrapy.cmdline import execute

import sys
import os

# execute(["scrapy", "crawl", "Qingdao"])
# flightNo = 'NS3261'
# flightNo = 'ZH9511'

# execute(["scrapy", "crawl", "FeiChangZhun"])

flightNo = 'ZH9506'
flightDate = "2018-06-14"
execute(["scrapy", "crawl", "ShenZhen", '-a', 'flightNo=' + flightNo, '-a', 'flightDate=' + flightDate])
