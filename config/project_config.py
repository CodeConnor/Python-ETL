'''
整个项目的配置项都设置在这个文件中
'''
import time


# =========================== 程序运行日志配置项 start ====================================
# 日志输出根目录
log_root_path = 'D:/Python/PycharmProjects/Python-ETL/log/'
# 日志输出文件名(每小时生成1个log)
log_name = f'pyetl-{time.strftime("%Y%m%d-%H", time.localtime(time.time()))}.log'
# =========================== 程序运行日志配置项 end ======================================


# =========================== JSON订单数据采集配置项 start ================================
# JSON数据所在路径
json_root_path = 'D:/Python/pyetl-data/json'
# =========================== JSON订单数据采集配置项 end ==================================


# ============================= mysql 配置 start =======================================
# 元数据管理库配置
metadata_host = 'localhost'
metadata_port = 3306
metadata_user = 'root'
metadata_password = '123456'
mysql_charset = 'utf8'

metadata_db_name = 'metadata'  # 元数据库名称
metadata_file_monitor_table_name = 'file_monitor'  # 元数据表名称
# 元数据表建表语句
metadata_file_monitor_table_create_cols = '''
    id INT AUTO_INCREMENT PRIMARY KEY,
    file_name VARCHAR(50) UNIQUE NOT NULL COMMENT '被处理文件文件名',
    process_lines INT COMMENT '被处理文件数据条数',
    process_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '文件处理时间'
'''

# 业务数据源数据库配置

# 目标数据库配置

# ============================= mysql 配置 end =========================================

