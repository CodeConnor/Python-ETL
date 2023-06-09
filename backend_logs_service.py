# coding:utf8
'''
用于采集后台日志文件（backend_logs）的业务逻辑
'''
from util.logging_util import Logging
from util.mysql_util import MySQLUtil, get_processed_files
from config import project_config as conf
from util import file_util as fu

logger = Logging().init_logger()
logger.info("程序启动，开始采集后台日志文件（backend_logs）......")

# 建立数据库连接
metadata_db_util = MySQLUtil()
target_db_util = MySQLUtil(
    host=conf.target_host,
    port=conf.target_port,
    user=conf.target_user,
    password=conf.target_password
)

# 读取元数据库
processed_log_files = get_processed_files(
    db_util=metadata_db_util,
    table_name=conf.metadata_backend_logs_monitor_table_name,
    create_cols=conf.metadata_backend_logs_monitor_table_create_cols
)

# 获取所有待处理的backend_logs文件
backend_log_files = fu.get_dir_files_list(
    path=conf.backend_logs_root_path
)

# 对比以上两列表区别，找出待处理backend_logs
logs_to_be_processed = fu.get_new_files_by_comparing_lists(backend_log_files, processed_log_files)
logger.info(f"通过对比元数据库，待处理文件如下：{logs_to_be_processed}")


