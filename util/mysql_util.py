# 封装mysql中连接数据库、执行SQL语句等常用方法

import pymysql
from config import project_config as conf
from util.logging_util import Logging

# 获取logger对象
logger = Logging().init_logger()


class MySQLUtil(object):
    '''创建pymysql工具类'''

    def __init__(self,
                 host=conf.metadata_host,
                 port=conf.metadata_port,
                 user=conf.metadata_user,
                 password=conf.metadata_password,
                 charset=conf.mysql_charset,
                 autocommit=False
                 ):
        '''初始化MySQL配置信息为属性，默认连接元数据库，可通过传参连接其他数据库'''
        self.conn = pymysql.Connection(  # 创建pymysql对象，连接数据库
            host=host,  # 主机名，IP地址
            port=port,  # 端口号
            user=user,  # 用户
            password=password,  # 密码
            charset=charset,  # 设置字符集
            autocommit=autocommit  # SQL语句的自动提交，为False时，执行`self.conn.commit()`后，SQL语句才会提交到数据库中执行
        )
        # 输出info日志
        logger.info(f'{host}:{port}数据库连接构建完成...')

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
        return (table_name,) in result

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


def get_processed_files(db_util,
                        db_name=conf.metadata_db_name,
                        table_name=conf.metadata_file_monitor_table_name,
                        create_cols=conf.metadata_file_monitor_table_create_cols
                        ):
    '''
    该方法用于将已被处理的文件的元数据存入元数据库中，创建并获取元数据表中被处理文件的文件名列表
    :param db_util:被实例化的MySQLUtil对象
    :param db_name:元数据库名称
    :param table_name:存储元数据的数据表名称
    :param create_cols:建表所用的列信息
    :return:已处理文件的列表
    '''
    # 选择数据库，若无表，则建立元数据数据表
    db_util.select_db(db_name)
    db_util.check_table_exists_and_create(
        db_name,
        table_name,
        create_cols
    )
    # 元数据表查询结果转换为列表
    # 查询结果为列表嵌套元组即[(D:/test_file1,),(D:/test_file2,)]
    # 所以需要for循环将元组取出，并使用i[0]切片，获取文件名字符串到列表中
    processed_files = [i[0] for i in db_util.query(f'SELECT file_name FROM {table_name} ORDER BY id')]

    return processed_files

