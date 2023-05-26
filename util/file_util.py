# coding:utf8
'''
功能逻辑：
封装文件处理的相关方法，实现文件处理在其他代码中的复用
'''
import os


def get_dir_files_list(path, recursion=False):
    '''
    获取文件夹中的文件列表，可进行递归获取
    :param path: 需要进行文件判断的文件路径，默认当前目录
    :param recursion: 是否递归读取，默认不递归
    :return: list对象，其中储存文件路径
    '''
    files = []  # 存储读取到的文件列表
    dir_names = os.listdir(path=path)  # 获取路径中的所有文件夹和文件

    for dir_name in dir_names:
        absolute_path = f'{path}/{dir_name}'  # 获取目录及文件的绝对路径
        if os.path.isfile(absolute_path):  # 判断是否为文件
            files.append(absolute_path)  # 是文件即添加入列表中

        else:  # 不是文件
            if recursion:  # 判断是否递归
                recursion_files = get_dir_files_list(absolute_path, recursion=recursion)  # 递归获取文件
                files += recursion_files  # 添加递归获取到的文件列表到大列表中

    return files

def get_new_files_by_comparing_lists(JSON_list, processed_list):
    '''
    对比两个list，找出JSON文件列表中的待处理的文件
    :param JSON_list: JSON业务数据文件列表，包含待处理文件与已处理文件
    :param processed_list: 已处理文件列表
    :return: list，待处理文件列表
    '''
    new_files = []
    for file in JSON_list:
        if file not in processed_list:
            new_files.append(file)

    return new_files
