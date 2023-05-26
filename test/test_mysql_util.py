# coding:utf8
'''
测试MySQL工具类的一系列功能
'''
# 创建测试文件测试util中的工具类
# 一起导入需要测试的util工具类与方法
from util.mysql_util import MySQLUtil, get_processed_files
# 导入TestCase包
from unittest import TestCase
from config import project_config as conf


class TestMySQLUtil(TestCase):  # 继承至TestCase
    # 初始化测试类
    def setUp(self) -> None:
        # 创建对象, 初始化测试库以及测试表
        self.db_util = MySQLUtil()
        self.db_test = 'db_for_unittest'
        self.tb_test = 'table_for_unittest'

    # 定义测试方法测试sql语句
    def test_query(self):
        '''
        测试MySQLUtil中的query方法
        测试需要独立，不使用已存在的表，解耦合
        以下一共测试了select_db, query, check_table_exists_and_create, check_table_exists, execute 5个方法
        :return:
        '''
        # 建立数据库
        self.db_util.execute(f'CREATE DATABASE IF NOT EXISTS {self.db_test} CHARACTER SET utf8')
        # 连接数据库
        self.db_util.select_db(self.db_test)
        # 建表
        self.db_util.check_table_exists_and_create(
            self.db_test,
            self.tb_test,
            'id INT PRIMARY KEY, name VARCHAR(255)')
        # 删除并重建表，排除表内数据影响
        self.db_util.execute(f'TRUNCATE {self.tb_test}')
        # 插入数据
        self.db_util.execute(f'INSERT INTO {self.tb_test} VALUES(1, "Tom"), (2, "Lihua")')
        # 测试query
        result = self.db_util.query(f'SELECT * FROM {self.tb_test} ORDER BY id')
        expected = ((1, 'Tom'), (2, 'Lihua'))
        self.assertEqual(expected, result)
        # 清理单元测试残留
        self.db_util.execute(f'DROP DATABASE {self.db_test}')
        self.db_util.close_conn()

    def test_execute_without_autocommit(self):
        '''
        测试方法同上，需要分别测试将autocommit设置为True和False的情况
        注意：如果autocommit为False时提交插入语句不会写入数据库，但会写入缓存，此时用select查询数据库会从缓存将未提交的数据查询出来
        为了避免这个情况，需要创建与数据库的新连接来执行select
        :return:
        '''
        # autocommit = True
        db_util1 = MySQLUtil()
        db_util1.conn.autocommit(True)
        # 建立数据库
        db_util1.execute(f'CREATE DATABASE IF NOT EXISTS {self.db_test} CHARACTER SET utf8')
        # 连接数据库
        db_util1.select_db(self.db_test)
        # 建表
        db_util1.check_table_exists_and_create(
            self.db_test,
            self.tb_test,
            'id INT PRIMARY KEY, name VARCHAR(255)')
        # 删除并重建表，排除表内数据影响
        db_util1.execute(f'TRUNCATE {self.tb_test}')
        # 插入数据, 测试execute_without_autocommit
        db_util1.execute_without_autocommit(f'INSERT INTO {self.tb_test} VALUES(1, "Tom")')
        # 验证结果
        result = db_util1.query(f'SELECT * FROM {self.tb_test} ORDER BY id')
        expected = ((1, 'Tom'),)
        self.assertEqual(expected, result)

        # autocommit = False
        db_util1.conn.autocommit(False)
        # 插入数据, 测试execute_without_autocommit
        db_util1.execute_without_autocommit(f'INSERT INTO {self.tb_test} VALUES(2, "Lihua")')
        db_util1.close_conn()
        # 使用新的连接对象验证结果
        db_util2 = MySQLUtil()
        db_util2.select_db(self.db_test)
        # 验证结果
        result = db_util2.query(f'SELECT * FROM {self.tb_test} ORDER BY id')
        expected = ((1, 'Tom'),)
        self.assertEqual(expected, result)

        # 清理单元测试残留
        db_util2.execute(f'DROP DATABASE {self.db_test}')
        db_util2.close_conn()

    def test_get_processed_files(self):
        '''
        测试该独立方法
        :return:
        '''
        # 建立测试数据库以及数据表
        self.db_util.execute(f'CREATE DATABASE IF NOT EXISTS {self.db_test} CHARACTER SET utf8')
        self.db_util.check_table_exists_and_create(
            self.db_test,
            self.tb_test,
            conf.metadata_file_monitor_table_create_cols
        )
        self.db_util.execute(f'TRUNCATE {self.tb_test}')  # 排除未通过测试时，表格有缓存导致插入重复数据的情况
        self.db_util.execute(
            f'INSERT INTO {self.tb_test} VALUES(NULL, "D:/test_file1", 1000, "2000-01-01 00:00:01"),(NULL, "D:/test_file2", 1200, "2000-01-01 00:59:01")')
        result = get_processed_files(
            self.db_util,
            self.db_test,
            self.tb_test,
        )
        # 将字符串类型的时间转换为datetime类型
        expected = ["D:/test_file1", "D:/test_file2"]
        self.assertEqual(expected, result)
        # 移除测试数据库
        self.db_util.execute(f'DROP DATABASE {self.db_test}')
        self.db_util.close_conn()
