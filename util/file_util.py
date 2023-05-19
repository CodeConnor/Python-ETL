# coding:utf8
'''
功能逻辑：
封装文件处理的相关方法，实现文件处理在其他代码中的复用
'''
import os
from config import project_config as conf


def get_dir_files_list(path='./', recursion=False):
    '''
    获取文件夹中的文件列表，可进行递归获取
    :param path: 需要进行文件判断的文件路径，默认当前目录
    :param recursion: 是否递归读取，默认不递归
    :return: list对象，其中储存文件路径
    '''
    file_list = []
