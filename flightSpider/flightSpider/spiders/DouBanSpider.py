import scrapy

from ..Item.MovieItems import MovieItem


class DouBanSpider(scrapy.Spider):
    name = 'douban'
    allowed_domain = ['movie.douban.com']
    start_urls = [
        'https://movie.douban.com/top250'
    ]

    def parse(self, response):
        selector = scrapy.Selector(response)
        # 解析出各个电影
        movies = selector.xpath('//div[@class="item"]')
        # 存放电影信息
        item = MovieItem()

        for movie in movies:
            # 电影各种语言名字的列表
            titles = movie.xpath('.//span[@class="title"]/text()').extract()
            name = ''
            for title in titles:
                name += title.strip()
            item['name'] = name

            # 电影信息列表
            infos = movie.xpath('.//div[@class="bd"]/p/text()').extract()
            # 电影信息合成一个字符串
            fullInfo = ''
            for info in infos:
                fullInfo += info.strip()
            item['info'] = fullInfo

            # 提取评分信息
            # item['rating'] = movie.xpath('.//span[@class="rating_num"]/text()').extract()[0].strip()
            # 提取评价人数
            # item['num'] = movie.xpath('.//div[@class="star"]/span[last()]/text()').extract()[0].strip()[:-3]
            quote = movie.xpath('.//span[@class="inq"]/text()').extract()
            if quote:
                quote = quote[0].strip()
            item['quote'] = quote
            yield item
        next_page = response.css('span.next a::attr(href)').extract_first()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)
