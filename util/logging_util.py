# coding:utf8
# 封装将日志输出到文件中的方法
import logging
from config import project_config as conf


class Logging:
    # 初始化日志等级、logger对象
    def __init__(self, level=20):
        self.logger = logging.getLogger()
        self.logger.setLevel(level)

    # 获取日志对象
    def init_logger(self):
        # 实例化得到logger对象
        logger = Logging().logger

        # 获取Handle,并设置属性
        file_handle = logging.FileHandler(
            filename=conf.file_path + conf.file_name,
            mode='a',
            encoding='UTF-8'
        )

        # 设置日志输出格式
        fmt = logging.Formatter('%(asctime)s - [%(levelname)s] - %(filename)s[%(lineno)d]: %(message)s')

        # 将输出格式应用到handle中
        file_handle.setFormatter(fmt)

        # 将handle实例传入logger对象
        logger.addHandler(file_handle)

        return logger


