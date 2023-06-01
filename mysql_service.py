# coding:utf8
'''
将MySQL中的条码库（商品信息）数据，采集到目标MySQL（target）中
'''
import sys
from util.logging_util import Logging
from util.mysql_util import MySQLUtil
from config import project_config as conf

# 构建日志对象
logger = Logging().init_logger()
logger.info('采集MySQL数据（商品信息数据）程序启动......')

# TODO：步骤1 -- 构建数据库连接
metadata_db_util = MySQLUtil()
target_db_util = MySQLUtil(
    host=conf.target_host,
    port=conf.target_port,
    user=conf.target_user,
    password=conf.target_password,
)
source_db_util = MySQLUtil(

)

# TODO：步骤2 -- 从数据源中读取数据