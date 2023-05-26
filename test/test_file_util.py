# coding:utf8
'''
单元测试：
测试file_util中的方法
'''
from unittest import TestCase
from util import file_util as fu
import os


class TestFileUtil(TestCase):
    def setUp(self) -> None:
        self.test_path = os.getcwd()  # 获取当前路径

    def test_get_dir_files_list(self):
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
        test_dir_path = self.test_path + '/test_dir'  # 获取测试文件夹所在路径
        # 不递归
        result = []  # 用于存放测试结果文件列表
        for i in fu.get_dir_files_list(test_dir_path):  # 不递归获取测试中所有文件名
            result .append(os.path.basename(i))  # 只添加文件名
        result.sort()  # 对结果排序，防止乱序时通不过测试
        self.assertEqual(['1', '2'], result)

        # 递归
        result = []  # 用于存放测试结果文件列表
        for i in fu.get_dir_files_list(test_dir_path, recursion=True):  # 递归获取测试中所有文件名
            result.append(os.path.basename(i))  # 只添加文件名
        result.sort()  # 对结果排序，防止乱序通不过测试
        self.assertEqual(['1', '2', '3', '4', '5'], result)

        '''
        推导式写法
        # 不递归
        result1 = [os.path.basename(i) for i in fu.get_dir_files_list(test_dir_path)]
        self.assertEqual(['1', '2'], result1)

        # 递归
        result2 = [os.path.basename(i) for i in fu.get_dir_files_list(test_dir_path, recursion=True)]
        self.assertEqual(['1', '2', '3', '4', '5'], result2)
        '''

    def test_get_new_files_by_comparing_lists(self):
        '''建立两个列表进行独立测试'''
        big_list = ['D:/a.json', 'D:/b.json', 'D:/c.json', 'D:/d.json']
        small_list = ['D:/a.json', 'D:/b.json']
        result = fu.get_new_files_by_comparing_lists(big_list, small_list)
        self.assertEqual(['D:/c.json', 'D:/d.json'], result)
