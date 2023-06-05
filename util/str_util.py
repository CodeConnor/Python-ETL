# coding:utf8
'''
字符串处理的相关工具方法
'''


def check_null(data: str):
    '''
    检查字符串是否为无意义字符串，是则返回True，否则返回False
    无意义：内容为空字符串、None、null、undefined
    :param data: str，待检查字符串
    :return: True：无意义， False：有意义
    '''
    if not data:
        return True
    data = data.lower()  # 将字符串转换为小写，减少判断难度
    if data == '' or data == 'none' or data == 'null' or data == 'undefined':
        # 数据无意义则进入if选项
        return True
    return False


def check_str_null_and_transform_to_sql_null(data):
    '''
    检查字符串是否无意义，是则将无意义字符串转换为SQL中的NULL，否则返回原字符串
    :param data: 待检查字符串
    :return: "NULL" 或者 str
    '''
    if check_null(str(data)):
        return "NULL"
    else:
        return f"'{data}'"


def check_number_null_and_transform_to_sql_null(data):
    '''
    检查数字是否无意义，是则将无意义数字转换为SQL中的NULL，否则返回原数字内容
    :param data: 待检查数字
    :return: "NULL" 或者 data
    '''
    if data and not check_null(str(data)):
        return data
    else:
        return "NULL"


def clean_str(data):
    '''
    排除脏数据影响
    例如：可口可乐\，其中的斜杠会影响程序执行（转义）
    '''
    if check_null(data):
        # 无意义内容不影响，直接返回
        return data
    else:
        # 排除特殊符号影响
        data = data.replace("'", "")
        data = data.replace('"', "")
        data = data.replace("\\", "")
        data = data.replace("@", "")
        data = data.replace(";", "")
        data = data.replace(",", "")
        return data
