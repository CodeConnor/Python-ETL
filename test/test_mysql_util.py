# 创建测试文件测试util中的工具类
# 导入需要测试的util工具类
from util.mysql_util import MySQLUtil
# 导入TestCase包
from unittest import TestCase

class TestMySQLUtil(TestCase):  # 继承至TestCase
    # 初始化测试类
    def setUp(self) -> None:
        # 创建对象
        self.db_util = MySQLUtil()

    # 定义测试方法测试sql语句
    def test_query(self):
        # 调用对象中的execute方法
        self.db_util.execute('show databases;')