from scrapy.cmdline import execute

import sys
import os

# execute(["scrapy", "crawl", "Qingdao"])
flightNo = 'GY7107'
flightDate = "2018-06-11"
execute(["scrapy", "crawl", "GuiZhou", '-a', 'flightNo=' + flightNo,'flightDate='+flightDate])
