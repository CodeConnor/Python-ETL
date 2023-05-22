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

# 业务数据源数据库配置

# 目标数据库配置

# ============================= mysql 配置 end =========================================

