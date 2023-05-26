# coding:utf8
# 功能逻辑：采集JSON数据（订单数据）到MySQL和CSV中
from util.logging_util import Logging
from util import file_util as fu
from config import project_config as conf
from util.mysql_util import MySQLUtil, get_processed_files

# 获取logger对象，用于后续输出日志
logger = Logging().init_logger()
logger.info('程序启动，开始读取JSON数据......')

# 获取JSON数据路径下的文件列表
files = fu.get_dir_files_list(conf.json_root_path)
logger.info(f'读取JSON数据路径，所获文件如下：{files}')

# 将已处理JSON数据文件信息存入元数据库
db_util = MySQLUtil()
processed_files = get_processed_files(db_util)
logger.info(f'读取元数据库，所获已处理文件如下：{processed_files}')

# 通过对比JSON文件列表与已处理文件列表，找出待处理文件
files_to_be_processed = fu.get_new_files_by_comparing_lists(files, processed_files)
logger.info(f'通过对比元数据库，待处理文件如下：{files_to_be_processed}')