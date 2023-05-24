# 封装mysql中连接数据库、执行SQL语句等常用方法

import pymysql
from config import project_config as conf
from util.logging_util import Logging

# 获取logger对象
logger = Logging().init_logger()


class MySQLUtil(object):
    '''创建pymysql工具类'''

    def __init__(self):
        '''初始化MySQL配置信息为属性'''
        self.conn = pymysql.Connection(  # 创建pymysql对象，连接数据库
            host=conf.metadata_host,  # 主机名，IP地址
            port=conf.metadata_port,  # 端口号
            user=conf.metadata_user,  # 用户
            password=conf.metadata_password,  # 密码
            charset=conf.mysql_charset,  # 设置字符集
            autocommit=False  # SQL语句的自动提交，为False时，执行`self.conn.commit()`后，SQL语句才会提交到数据库中执行
        )
        # 输出info日志
        logger.info(f'{conf.metadata_host}:{conf.metadata_port}数据库连接构建完成...')

    def close_conn(self):
        '''关闭数据库连接'''
        if self.conn:  # 如果数据库连接正常
            self.conn.close()

    def query(self, sql):
        '''
        执行SQL中的查询语句，并返回查询结果
        :param sql: 被执行的SQL语句
        :return: 查询结果
        '''
        # 获取可执行sql的游标cursor
        cursor = self.conn.cursor()
        cursor.execute(sql)
        # 通过游标获取执行结果
        result = cursor.fetchall()
        # 关闭游标
        cursor.close()
        # 输出info日志
        logger.info(f'{sql}被执行，返回{len(result)}条数据')
        return result

    def select_db(self, db):
        '''选择数据库，实现SQL中USE功能'''
        self.conn.select_db(db)

    def execute(self, sql):
        '''
        执行无返回值SQL语句（CREATE,UPDATE,INSERT），100%提交
        :param sql: 被执行的SQL
        :return: None
        '''
        cursor = self.conn.cursor()  # 创建游标
        cursor.execute(sql)
        # 判断自动提交是否生效，若不生效就手动提交
        if not self.conn.get_autocommit():
            self.conn.commit()
            # 输出debug日志
            logger.debug(f'{sql}被执行，已提交')
        cursor.close()  # 关闭游标

    # 封装方法，执行无返回值sql语句，不自动提交
    def execute_without_autocommit(self, sql):
        '''
        执行无返回值SQL语句，不自动提交
        :param sql: 被执行的SQL
        :return: None
        '''
        cursor = self.conn.cursor()
        cursor.execute(sql)  # 因为还未提交SQL语句，所以不要关闭游标
        logger.debug(f'{sql}被执行，未提交')

    def check_table_exists(self, db_name, table_name):
        '''
        检查数据库中表是否存在
        :param db_name: 被检查的数据库
        :param table_name: 被检查的数据表名
        :return:True存在，False不存在
        '''
        self.select_db(db_name)  # 切换数据库
        result = self.query('SHOW TABLES')  # 执行查询语句
        # 因为数据库返回的结果为嵌套的元组：((table1, ), (teble2, ))，所以需要用元组来检查结果
        return (table_name, ) in result

    def check_table_exists_and_create(self, db_name, table_name, create_cols):
        '''
        检查数据库中表是否存在，若不存在则创建它
        :param db_name: 被检查的数据库
        :param table_name: 被检查与被创建的表名
        :param create_cols: 创建表的列信息
        :return:
        '''
        # 调用自身方法查询表格是否存在
        if not self.check_table_exists(db_name, table_name):  # 进入if说明不存在该表
            create_sql = f'CREATE TABLE {table_name}({create_cols})'
            self.execute(create_sql)
