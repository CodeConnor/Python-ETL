# coding:utf8
'''
时间工具的单元测试
'''
from unittest import TestCase
from util import time_util as tu

class TestTimeUtil(TestCase):
    def setUp(self) -> None:
        pass

    def test_ts10_to_date_str(self):
        # 不传参的测试
        timestamp_s = 1685342666
        result = tu.ts10_to_date_str(timestamp_s)
        self.assertEqual('2023-05-29 14:44:26', result)

        # 传参测试
        result = tu.ts10_to_date_str(timestamp_s, '%Y%m%d%H%M%S')
        self.assertEqual('20230529144426', result)


    def test_ts13_to_date_str(self):
        timestamp_ms = 1685342930765
        result = tu.ts13_to_date_str(timestamp_ms)
        self.assertEqual('2023-05-29 14:48:50', result)

        result = tu.ts13_to_date_str(timestamp_ms, '%Y%m%d%H%M%S')
        self.assertEqual('20230529144850', result)