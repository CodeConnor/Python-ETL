# coding:utf8
# 功能逻辑：采集JSON数据（订单数据）到MySQL和CSV中
from util.logging_util import Logging
from util import file_util as fu
from config import project_config as conf
from util.mysql_util import MySQLUtil, get_processed_files
from model.retail_orders_model import OrdersModel, OrdersDetailModel

# TODO: 步骤1--读取文件，获取待处理文件
# 构建数据库连接
metadata_db_util = MySQLUtil()  # 建立元数据库连接
# 建立目标数据库连接
target_db_util = MySQLUtil(
    host=conf.target_host,
    port=conf.target_port,
    user=conf.target_user,
    password=conf.target_password
)


# 获取logger对象，用于后续输出日志
logger = Logging().init_logger()
logger.info('程序启动，开始读取JSON数据......')

# 获取JSON数据路径下的文件列表
files = fu.get_dir_files_list(conf.json_root_path)
logger.info(f'读取JSON数据路径，所获文件如下：{files}')

# 将已处理JSON数据文件信息存入元数据库
processed_files = get_processed_files(metadata_db_util)
logger.info(f'读取元数据库，所获已处理文件如下：{processed_files}')

# 通过对比JSON文件列表与已处理文件列表，找出待处理文件
files_to_be_processed = fu.get_new_files_by_comparing_lists(files, processed_files)
logger.info(f'通过对比元数据库，待处理文件如下：{files_to_be_processed}')

# TODO: 步骤二--开始处理数据
global_count = 0  # 记录被处理数据的行数，全局记录
global_count_reserved = 0  # 记录过滤后保留的数据行数，全局记录
dict_processed_files = {}  # 记录被处理的文件与文件中被处理的数据条数
# 对待处理文件进行读取，按行读取，防止一次性读取文件中所有信息导致性能下降
for file in files_to_be_processed:
    order_model_list = []  # 存储所有订单模型对象
    order_detail_model_list = []  # 存储所有订单详情模型对象
    count_processed_lines = 0  # 记录单个文件被处理的数据行数

    for line in open(file, 'r', encoding='UTF-8'):
        line = line.replace('\n', '')  # line是文件中的1行数据，需要将换行符替换为空字符
        order_model = OrdersModel(line)  # 调用自定义类，将1行数据实例化为1个模型对象
        global_count += 1
        # 过滤数据
        # receivable表示本订单的实收金额
        # 若receivable的金额非常大，则说明订单异常，大于10000的数据都需要过滤掉（实际业务中过滤需求不同）
        if order_model.receivable <= 10000:
            order_model_list.append(order_model)
            order_detail_model = OrdersDetailModel(line)
            order_detail_model_list.append(order_detail_model)
            global_count_reserved += 1
            count_processed_lines += 1

    # 将订单模型的中的数据写出到CSV文件
    order_csv_write_f = open(  # 用于写出订单模型的文件对象，使用追加模式，防止写入多个文件内容时，将上一次写入内容覆盖
        conf.retail_output_csv_root_path + conf.retail_orders_output_csv_file_name, 'a', encoding='UTF-8'
    )

    order_detail_csv_write_f = open(  # 用于写出订单详情模型的文件对象
        conf.retail_output_csv_root_path + conf.retail_orders_detail_output_csv_file_name, 'a', encoding='UTF-8'
    )

    for model in order_model_list:
        # 写入订单模型信息
        order_csv_write_f.write(model.to_csv())  # 将模型中的数据转换为CSV格式的字符串再写入文件
        order_csv_write_f.write('\n')  # 写入换行符
    order_csv_write_f.close()

    for model in order_detail_model_list:
        # 写入订单详情模型信息
        for single_product_model in model.products_detail:  # 遍历模型存储的子模型（SingleProductSoldModel），使用子模型的to_csv方法
            order_detail_csv_write_f.write(single_product_model.to_csv())
            order_detail_csv_write_f.write('\n')
    order_detail_csv_write_f.close()

    # 以下方法效果相同，调用了OrdersDetailModel中的to_csv方法
    # for model in order_detail_model_list:
    #     order_detail_csv_write_f.write(model.to_csv())  # 注意:该方法中已经添加了换行符'\n'，所以之后无需重复添加
    # order_detail_csv_write_f.close()

    # 将数据写入到MySQL中
    # 判断待写入的表是否存在于MySQL中，不存在则创建
    # 判断订单表
    target_db_util.check_table_exists_and_create(
        conf.target_db_name,
        conf.target_orders_table_name,
        conf.target_orders_table_create_cols
    )

    # 判断订单详情表
    target_db_util.check_table_exists_and_create(
        conf.target_db_name,
        conf.target_orders_detail_table_name,
        conf.target_orders_detail_table_create_cols
    )

    # 将订单数据写入订单表
    for model in order_model_list:
        orders_sql = model.generate_insert_sql()
        target_db_util.select_db(conf.target_db_name)
        # 如果使用execute自动提交会导致执行1000条插入就要提交1000次，性能很低
        target_db_util.execute_without_autocommit(orders_sql)  # 先执行不提交，最后一次性提交，还能满足`事务处理`的要求

    # 将订单详情数据写入订单详情表
    for model in order_detail_model_list:
        orders_detail_sql = model.generate_insert_sql()
        target_db_util.select_db(conf.target_db_name)
        target_db_util.execute_without_autocommit(orders_detail_sql)

    dict_processed_files[file] = count_processed_lines  # 将被处理的文件名与数据行数记录到字典中

target_db_util.conn.commit()  # 一次性提交所有SQL
logger.info(f'CSV备份文件写出完成，写出路径：{conf.retail_output_csv_root_path}')
logger.info(f'json数据写入target数据库成功，共处理：{global_count}行，写入：{global_count_reserved}行，过滤：{global_count - global_count_reserved}行')

# 将已处理文件的记录存入元数据库中
for file_name in dict_processed_files.keys():  # 取出文件名
    lines_processed_file = dict_processed_files[file_name]  # 取出对应文件被处理行数
    insert_sql = f"INSERT IGNORE INTO {conf.metadata_file_monitor_table_name}(file_name, process_lines) " \
          f"VALUES ('{file_name}', {lines_processed_file})"  # 组成插入语句，只用插入两列
    metadata_db_util.execute(insert_sql)

# 关闭所有数据库连接
metadata_db_util.close_conn()
target_db_util.close_conn()
logger.info(f'读取JSON数据写入数据库完成，CSV文件备份完成，程序结束......')









