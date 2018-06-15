# coding=utf-8
import random
from ..settings import IPPOOL
from scrapy.downloadermiddlewares.httpproxy import HttpProxyMiddleware
import logging

class MyproxiesSpiderMiddleware(HttpProxyMiddleware):

    def __init__(self, ip=''):
        self.ip = ip

    def process_request(self, request, spider):
        thisip = random.choice(IPPOOL)
        logging.info(thisip)
        request.meta["proxy"] = "http://" + thisip["ipaddr"]
