# coding=utf-8

import scrapy
import re

from ..Item.TuniuItem import TuniuItem

Pnum = re.compile("([0-9]*)")


class TuNiuSpider(scrapy.Spider):
    name = 'tuniu'
    allowed_domain = 'tuniu.com'
    start_urls = [
        'http://s.tuniu.com/search_complex/pkg-sz-0-%E4%B8%8A%E6%B5%B7/'
    ]

    def parse(self, response):
        next_page = response.css("a.page-next::attr(href)").extract_first()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse_item)

    def parse_item(self, response):
        selector = scrapy.Selector(response)
        lines = selector.css('div.theinfo')

        for line in lines:
            url = line.css('a.clearfix::attr(href)').extract()[0]
            yield scrapy.Request(response.urljoin(url), callback=self.parse_detail)

    def parse_detail(self, response):
        selector = scrapy.Selector(response)
        item = TuniuItem()
        c = re.compile(r'<h1 class="resource-title"><strong>(.*?)</strong>')
        title = c.search(response.text).group(1)
        item['title'] = title
        price = selector.css('span.price-number::text').extract_first()
        item['price'] = price
        Nums = selector.css(r'a.resource-people-number::text').extract()
        if len(Nums) > 0:
            item['personNum'] = Nums[0]
            item['recommendNum'] = Nums[1]
        # recommendNum = selector.css(r'a.resource-people-number::text').extract()[1]
        yield item
