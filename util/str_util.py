# coding:utf8
'''
字符串处理的相关工具方法
'''

def check_null(data):
    '''
    检查字符串是否为无意义字符串，是则返回True，否则返回False
    无意义：内容为空字符串、None、null、undefined
    :param data: str，待检查字符串
    :return: True：无意义， False：有意义
    '''