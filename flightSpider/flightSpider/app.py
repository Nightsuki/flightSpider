import logging
import os

from flask import Flask, jsonify, abort, signals
from scrapy.crawler import Crawler, CrawlerProcess

from scrapy.utils.project import get_project_settings

from flightSpider.flightSpider.dao.FlightDao import FlightDao
from flightSpider.flightSpider.spiders.GuiZhou import GuiZhou

app = Flask(__name__)

spiders = {
    "CA": "GuoHang",
    "GY": "GuiZhou",
    "SC": "ShanDong",
    "BK": "AoKai"
}


@app.route('/flight/<string:flightDate>/<string:flightNo>', methods=['GET'])
def getFlightInfo(flightNo, flightDate):
    # spider = GuiZhou()
    # settings = get_project_settings()
    # crawler = Crawler(settings)
    # crawler.configure()
    # crawler.crawl(spider, flightNo)
    try:
        print('scrapy crawl ' + spiders[flightNo[0:2]] + ' -a flightNo=' + flightNo + ' -a flightDate=' + flightDate)
        os.system(
            'scrapy crawl ' + spiders[flightNo[0:2]] + ' -a flightNo=' + flightNo + ' -a flightDate=' + flightDate)
        dao = FlightDao()
        result = dao.searchFlight(flightNo)
        return jsonify({'flight': result})
    except Exception as error:
        # 出现错误时打印错误日志
        logging.error(error)
        result = error
        return jsonify({'error': result})
    # if len(result) == 0:
    #     abort(404)


if __name__ == '__main__':
    app.run(debug=True)
