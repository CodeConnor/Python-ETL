# coding:utf8
'''
将MySQL中的条码库（商品信息）数据，采集到目标MySQL（target）中
'''
import sys
from util.logging_util import Logging
from util.mysql_util import MySQLUtil
from config import project_config as conf
from model.barcode_model import BarcodeModel

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
# pymysql的查询结果为((col1, col2, col3), (col1, col2, col3), (col1, col2, col3), )
# 每个小元组是整个结果的1行，每个小元组内的元素是结果中每个列的1个元素
# TODO: 步骤三 -- 构建模型
barcode_models = []
for single_line in result:
    # 每行结果中列的排列顺序与表格顺序相同（select *）
    code = single_line[0]
    name = single_line[1]
    spec = single_line[2]
    trademark = single_line[3]
    addr = single_line[4]
    units = single_line[5]
    factory_name = single_line[6]
    trade_price = single_line[7]
    retail_price = single_line[8]
    update_at = single_line[9]
    wholeunit = single_line[10]
    wholenum = single_line[11]
    img = single_line[12]
    src = single_line[13]

    model = BarcodeModel(
        code=code,
        name=name,
        spec=spec,
        trademark=trademark,
        addr=addr,
        units=units,
        factory_name=factory_name,
        trade_price=trade_price,
        retail_price=retail_price,
        update_at=update_at,
        wholeunit=wholeunit,
        wholenum=wholenum,
        img=img,
        src=src,
    )
    barcode_models.append(model)

# TODO: 步骤四 -- 写入目标数据库


