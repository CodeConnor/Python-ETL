# coding:utf8
'''此文件是和时间相关的工具代码集合'''
import time


def ts10_to_date_str(timestamp, format_string='%Y-%m-%d %H:%M:%S'):
    '''
    将10位秒级时间戳转换为给定的日期格式
    :param timestamp: 待转换的时间戳
    :param format_string: 转换后的日期格式，默认：2023-01-01 00:00:00
    :return: 转换完成后的日期字符串
    '''
    time_array = time.localtime(timestamp)  # 将时间戳转换为时间数组（中转格式），该格式仅支持秒级10位时间戳
    # 将数组格式转化为指定时间格式
    return time.strftime(format_string, time_array)


def ts13_to_date_str(timestamp, format_string='%Y-%m-%d %H:%M:%S'):
    '''
    将13位毫秒级时间戳转换为给定的日期格式
    :param timestamp: 待转换的时间戳
    :param format_string: 转换后的日期格式，默认：2023-01-01 00:00:00
    :return: 转换完成后的日期字符串
    '''
    timestamp_s = int(timestamp / 1000)  # 将13位时间戳转换为10位时间戳
    return ts10_to_date_str(timestamp_s, format_string=format_string)

