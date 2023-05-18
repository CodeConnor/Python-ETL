import pymysql
from config import project_config as conf


# 创建pymysql工具类，保存mysql中常用操作的方法
class MySQLUtil(object):
    # 初始化MySQL配置信息为属性
    def __init__(self,
                 host=conf.metadata_host,
                 port=conf.metadata_port,
                 user=conf.metadata_user,
                 password=conf.metadata_password
                 ):
        # 创建pymysql对象，连接数据库
        self.conn = pymysql.connect(
            host=host,
            port=port,
            user=user,
            password=password
        )

    # 封装方法执行SQL语句
    def execute(self, sql):
        # 获取可执行sql的游标cursor
        cursor = self.conn.cursor()
        # 执行传入游标中的SQL语句
        cursor.execute(sql)
        # 关闭游标
        cursor.close()
