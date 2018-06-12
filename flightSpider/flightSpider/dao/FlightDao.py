import pymysql
import logging

from flightSpider.flightSpider import settings


class FlightDao(object):
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
        self.cursor = self.connect.cursor(cursor=pymysql.cursors.DictCursor)

    def searchFlight(self, airline):
        try:
            sql = 'SELECT * FROM flightInfo WHERE airline = %s'
            self.cursor.execute(sql, airline)
            # 获取查询结果
            result = self.cursor.fetchall()

        except Exception as error:
            # 出现错误时打印错误日志
            logging.error(error)
            result = None
        return result
