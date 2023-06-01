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
# 连接数据源source数据库
source_db_util = MySQLUtil(
    host=conf.source_host,
    port=conf.source_port,
    user=conf.source_user,
    password=conf.source_password
)

# TODO：步骤2 -- 从数据源中读取数据
# 判断需要采集的数据表是否存在
if not source_db_util.check_table_exists(conf.source_db_name, conf.source_barcode_table_name):
    logger.error(f'数据源库：{conf.source_db_name}中不存在数据源表：{conf.source_barcode_table_name}，'
                 f'无法采集，程序终止，请核实原因...')
    sys.exit(1)  # 发生异常，终止程序
