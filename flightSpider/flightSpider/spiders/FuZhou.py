# coding=utf-8
import re
from urllib import request
from urllib.parse import urljoin
# from PIL import Image
import scrapy
# from pytesseract import pytesseract

from ..Item.FuZhouCaptchaItem import FuZhouCaptchaItem
from ..Item.FuZhouItems import FuZhouItems


def convert_Image(img, standard=127.5):
    image = img.convert('L')
    pixels = image.load()
    for x in range(image.width):
        for y in range(image.height):
            if pixels[x, y] > standard:
                pixels[x, y] = 255
            else:
                pixels[x, y] = 0
    return image

#
# def change_Image_to_text(img):
#     testdata_dir_config = '--tessdata-dir "C:\\Program Files (x86)\\Tesseract-OCR\\tessdata"'
#     textCode = pytesseract.image_to_string(img, lang='eng', config=testdata_dir_config)
#     # 去掉非法字符，只保留字母数字
#     textCode = re.sub("\W", "", textCode)
#     return textCode


class FuZhouSpider(scrapy.Spider):
    name = "FuZhou"

    def start_requests(self):
        url = "http://www.fuzhou-air.cn/frontend/passengerService/onlinecheckin/flightDynamic.action"
        flightNo = '6520'
        header = {
            'Connection': 'keep - alive',
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/66.0.3359.181 Safari/537.36') "
        }
        flightDate = '2018-06-06'
        yield scrapy.Request(url=url, meta={"flightNo": flightNo, "flightDate": flightDate}, callback=self.parse_flight,
                             headers=header)

    def parse_flight(self, response):
        url = "http://www.fuzhou-air.cn/frontend/passengerService/onlinecheckin/flightDynamic!getFlightDynamic.action"
        header = {
            'Referer': 'http://www.fuzhou-air.cn/frontend/passengerService/onlinecheckin/flightDynamic.action',
            'Connection': 'keep - alive',
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/66.0.3359.181 Safari/537.36') "
        }
        meta = response.meta
        selector = scrapy.Selector(response)
        captcha = selector.css("img[id='jcaptcha']::attr(src)").extract_first()
        localPath = '/capatcha/fuzhouCapatcha.jpg'
        image_item = FuZhouCaptchaItem()
        image_item['image_url'] = urljoin(response.url, captcha)
        image_item['flightNo'] = meta['flightNo'][2:]
        image_item['flightDate'] = meta['flightDate']
        yield image_item
        # request.urlretrieve(urljoin(response.url, captcha), localPath)
        # img = Image.open(localPath)
        # img = convert_Image(img)
        # imgry = img.convert('L')
        #
        # threshold = 140
        # table = []
        # for i in range(256):
        #     if i < threshold:
        #         table.append(0)
        #     else:
        #         table.append(1)
        # out = imgry.point(table, '1')
        # out.show()
        # img.show()
        # j_captcha_response = change_Image_to_text(img)
        # image = io.imread(urljoin(response.url, captcha))
        # io.imshow(image)
        # io.show()
        # img = Image.open(localPath)
        # img.show()
        # f = open(localPath, "rb")
        # j_captcha_response = self.get_captcha_by_tessractcor(localPath)

        # j_captcha_response = input()
        # yield scrapy.FormRequest(
        #     url=url,
        #     formdata={"argDtoHnaFlight.fltid": meta['flightNo'][2:], "argDtoHnaFlight.datopchn:": meta['flightDate'],
        #               "j_captcha_response": j_captcha_response},
        #     callback=self.parse,
        #     headers=header,
        # )
        # img = Image.open
        pass

    def parse(self, response):
        selector = scrapy.Selector(response)
        flights = selector.css("table:nth-child(n+1)")
        print(response.body.decode('utf-8'))
        for flight in flights:
            item = FuZhouItems()
            text = flight.xpath("./td[2]/text()").extract_first()
            airline = "".join(flight.xpath("./td[2]/text()").extract_first().split())
            expDeptTime = "".join(flight.xpath("./td[4]/text()").extract_first().split())
            expArrTime = "".join(flight.xpath("./td[6]/text()").extract_first().split())
            actDeptTime = "".join(flight.xpath("./td[5]/text()").extract_first().split())
            actArrTime = "".join(flight.xpath("./td[7]/text()").extract_first().split())
            status = "".join(flight.xpath("./td[8]/text()").extract_first().split())
            # # ARR 落地 NDR 落地 ATA 到达 CNL 取消 DEL 延误 DEP 起飞 RTR 返航 SCH 计划

            airlineCorp = '福州航空'
            # print(str(flight))

            item['airline'] = airline
            item['airlineCorp'] = airlineCorp
            item['status'] = status
            item['expDeptTime'] = expDeptTime
            item['expArrTime'] = expArrTime
            item['actDeptTime'] = actDeptTime
            item['actArrTime'] = actArrTime
            yield item

    # def get_captcha_by_tessractcor(self, captcha_data):
# img = Image.open(captcha_data)
# img = img.convert('L')
# captcha_solution = pytesseract.image_to_string(img)
# img.close()
# return captcha_solution
