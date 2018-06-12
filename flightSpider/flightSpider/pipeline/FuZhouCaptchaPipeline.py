import scrapy
from scrapy.exceptions import DropItem
from scrapy.pipelines.images import ImagesPipeline
from scrapy.utils.project import get_project_settings
from ..spiders.FuZhou import FuZhouSpider


class FuZhouCaptchaPipeline(ImagesPipeline):
    img_store = get_project_settings().get('IMAGES_STORE')

    def get_media_requests(self, item, info):
        image_url = item['image_url']
        yield scrapy.Request(image_url)

    def item_completed(self, results, item, info):
        image_paths = [x['path'] for ok, x in results if ok]  # ok判断是否下载成功
        if not image_paths:
            raise DropItem("Item contains no images")

        url = "http://www.fuzhou-air.cn/frontend/passengerService/onlinecheckin/flightDynamic!getFlightDynamic.action"
        header = {
            'Referer': 'http://www.fuzhou-air.cn/frontend/passengerService/onlinecheckin/flightDynamic.action',
            'Connection': 'keep - alive',
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/66.0.3359.181 Safari/537.36') "
        }
        j_captcha_response = input()
        yield scrapy.FormRequest(
            url=url,
            formdata={"argDtoHnaFlight.fltid": item['flightNo'][2:], "argDtoHnaFlight.datopchn:": item['flightDate'],
                      "j_captcha_response": j_captcha_response},
            callback=FuZhouSpider.parse,
            headers=header,
        )
        return item
