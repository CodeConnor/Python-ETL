# 封装mysql中连接数据库、执行SQL语句等常用方法

import pymysql
from config import project_config as conf
from util.logging_util import Logging

# 获取logger对象
logger = Logging().init_logger()


# 创建pymysql工具类
class MySQLUtil(object):
    # 初始化MySQL配置信息为属性
    def __init__(self):
        # 创建pymysql对象，连接数据库
        self.conn = pymysql.Connection(
            host=conf.metadata_host,  # 主机名，IP地址
            port=conf.metadata_port,  # 端口号
            user=conf.metadata_user,  # 用户
            password=conf.metadata_password,  # 密码
            charset=conf.mysql_charset,  # 设置字符集
            autocommit=False  # SQL语句的自动提交，为False时，执行`self.conn.commit()`后才会SQL语句才会提交到数据库中执行
        )
        # 输出info日志
        logger.info(f'{conf.metadata_host}:{conf.metadata_port}数据库连接构建完成...')

    # 封装方法，关闭数据库连接的方法

    # 封装方法，执行查询SQL的方法，并返回查询结果
    def query(self, sql):
        # 获取可执行sql的游标cursor
        cursor = self.conn.cursor()
        cursor.execute(sql)

        # 通过游标获取执行结果

        # 关闭游标
        cursor.close()
        # 输出info日志

    # 封装方法，选择数据库，实现sql中的use功能

    # 封装方法，执行无返回值sql语句（CREATE,UPDATE,INSERT），100%提交

        # 输出debug日志

        # 判断自动提交是否生效，若不生效就手动提交

    # 封装方法，执行无返回值sql语句，不判断自动提交


