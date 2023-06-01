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

# 判断目标数据库中是否存在保存数据源的表，没有就创建
target_db_util.check_table_exists_and_create(
    conf.target_db_name,
    conf.target_barcode_table_name,
    conf.target_barcode_table_create_cols
)

last_update_time = None  # 记录元数据表的上次更新时间，初始为空
# 判断元数据库是否存在barcode元数据表
metadata_db_util.select_db(conf.metadata_db_name)
if not metadata_db_util.check_table_exists(conf.metadata_db_name, conf.metadata_barcode_monitor_table_name):
    # 不存在该表则创建
    metadata_db_util.check_table_exists_and_create(
        conf.metadata_db_name,
        conf.metadata_barcode_monitor_table_name,
        conf.metadata_barcode_monitor_table_create_cols
    )
else:
    # 筛选出上次的元数据更新时间，即最大的time_record
    # 但是不能用MAX()，因为使用MAX()如果查不到数据会返回((None),)，而不是真正的空()
    query_sql = f"SELECT time_record FROM {conf.metadata_barcode_monitor_table_name} " \
                f"ORDER BY time_record DESC LIMIT 1"
    result = metadata_db_util.query(query_sql)

    if len(result) != 0:
        # 如果能查到最大time_record，就取出元组中的字符 ==> ((timestamp, ), )
        last_update_time = str(result[0][0])

# 判断元数据上次更新时间是否存在
if last_update_time:
    # 存在则用该时间筛选数据源表
    barcode_query_sql = f"SELECT * FROM {conf.source_barcode_table_name} " \
          f"WHERE updateAt >= '{last_update_time}' ORDER BY updateAt"
else:
    # 不存在则检索整个数据源表
    barcode_query_sql = f"SELECT * FROM {conf.source_barcode_table_name} " \
                        f"ORDER BY updateAt"

# 执行查询
source_db_util.select_db(conf.source_db_name)
result = source_db_util.query(barcode_query_sql)

# TODO: 步骤三 -- 使用模型构建 INSERT 插入语句

