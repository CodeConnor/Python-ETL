# coding:utf8
# 导入单元测试包和需要测试的文件
import logging
from unittest import TestCase
from util.logging_util import Logging


# 必须定义的测试类
class TestLoggingUtil(TestCase):
    # 初始化需要测试的类
    def setUp(self) -> None:
        self.logging_util = Logging()

    # 定义测试方法
    def test_init_logging(self):
        logger = self.logging_util.init_logger()
        self.assertIsInstance(logger, logging.RootLogger)