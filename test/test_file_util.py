# coding:utf8
'''
单元测试：
测试file_util中的方法
'''
from unittest import TestCase
from util.file_util import get_dir_files_list


class TestFileUtil(TestCase):
    def setUp(self) -> None:
        pass

    def get_dir_files_list(self):
        '''
        请在工程根目录的test文件夹内建立:
        test_dir/
            inner1/
                3
                4
                inner2/
                    5
        1
        2
        的目录结构用于进行此方法的单元测试
        不递归结果应该是1和2
        递归结果应该是1,2,3,4,5
        '''
        pass