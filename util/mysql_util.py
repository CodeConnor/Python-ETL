# 封装mysql中连接数据库、执行SQL语句等常用方法

import pymysql
from config import project_config as conf


# 创建pymysql工具类
class MySQLUtil(object):
    # 初始化MySQL配置信息为属性
    def __init__(self):
        # 创建pymysql对象，连接数据库
        self.conn = pymysql.Connection(
            host=conf.metadata_host,            # 主机名，IP地址
            port=conf.metadata_port,            # 端口号
            user=conf.metadata_user,            # 用户
            password=conf.metadata_password,    # 密码
            charset=conf.mysql_charset,         # 设置字符集
            autocommit=False                    # sql语句的自动提交
        )

    # 封装方法执行SQL语句
    def execute(self, sql):
        # 获取可执行sql的游标cursor
        cursor = self.conn.cursor()
        # 执行传入游标中的SQL语句，此时代码还不会提交到数据库中执行，需要执行`self.conn.commit()`后才会执行（autocommit=False）
        cursor.execute(sql)
        # 关闭游标
        cursor.close()
