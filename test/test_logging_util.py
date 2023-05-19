# coding:utf8
# 导入单元测试包和需要测试的文件
from unittest import TestCase
from util.logging_util import Logging

# 必须定义的测试类
class TestLoggingUtil(TestCase):
    def setUp(self) -> None:
        self.logging_util = Logging()

    def test_logging(self):
        self.logging_util.init_logger()

