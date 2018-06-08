# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from logging import log

import pymysql

from . import settings


# class flightSpiderPipeline(object):
#     def process_item(self, item, spider):
#         return item


class FlightSpiderPipeline(object):
    def __init__(self):
        # 连接数据库
        self.connect = pymysql.connect(
            host=settings.MYSQL_HOST,
            db=settings.MYSQL_DBNAME,
            user=settings.MYSQL_USER,
            passwd=settings.MYSQL_PASSWD,
            charset='utf8',
            use_unicode=True)

        # 通过cursor执行增删查改
        self.cursor = self.connect.cursor()

    def process_item(self, item, spider):
        try:
            # 插入数据
            self.cursor.execute(
                """insert into flightInfo(expectedDepartureTime, expectedArrivalTime, actualDepartureTime, actualArrivalTime ,status,airline,airlineCorp)
                value (%s, %s, %s, %s, %s,%s,%s)""",
                (item['expDeptTime'],
                 item['expArrTime'],
                 item['actDeptTime'],
                 item['actArrTime'],
                 item['status'],
                 item['airline'],
                 item['airlineCorp']
                 )
            )

            # 提交sql语句
            self.connect.commit()

        except Exception as error:
            # 出现错误时打印错误日志
            log(error.msg)
        return item
