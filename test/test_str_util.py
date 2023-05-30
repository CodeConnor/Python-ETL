# coding:utf8
'''
字符串处理方法的单元测试
'''
from unittest import TestCase
from util import str_util

class TestStrUtil(TestCase):
    def setUp(self) -> None:
        pass

    def test_check_null(self):
        data = None
        result = str_util.check_null(data)
        self.assertTrue(result)

        data = 'NONE'
        result = str_util.check_null(data)
        self.assertTrue(result)

        data = 'none'
        result = str_util.check_null(data)
        self.assertTrue(result)

        data = 'null'
        result = str_util.check_null(data)
        self.assertTrue(result)

        data = 'undefined'
        result = str_util.check_null(data)
        self.assertTrue(result)

        data = ''
        result = str_util.check_null(data)
        self.assertTrue(result)

        data = '有意义数据'
        result = str_util.check_null(data)
        self.assertFalse(result)

    def test_check_str_null_and_transform_to_sql_null(self):
        data = None
        result = str_util.check_str_null_and_transform_to_sql_null(data)
        self.assertEqual("NULL", result)

        data = 'NONE'
        result = str_util.check_str_null_and_transform_to_sql_null(data)
        self.assertEqual("NULL", result)

        data = 'none'
        result = str_util.check_str_null_and_transform_to_sql_null(data)
        self.assertEqual("NULL", result)

        data = 'null'
        result = str_util.check_str_null_and_transform_to_sql_null(data)
        self.assertEqual("NULL", result)

        data = 'undefined'
        result = str_util.check_str_null_and_transform_to_sql_null(data)
        self.assertEqual("NULL", result)

        data = ''
        result = str_util.check_str_null_and_transform_to_sql_null(data)
        self.assertEqual("NULL", result)

        data = 111110000
        result = str_util.check_str_null_and_transform_to_sql_null(data)
        self.assertEqual(f"'{data}'", result)

        data = '有意义数据'
        result = str_util.check_str_null_and_transform_to_sql_null(data)
        self.assertEqual(f"'{data}'", result)