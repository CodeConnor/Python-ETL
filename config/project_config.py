'''
整个项目的配置项都设置在这个文件中
'''
import time


# ============================= mysql 配置 ==================================
metadata_host = 'localhost'
metadata_port = 3306
metadata_user = 'root'
metadata_password = '123456'
# ===========================================================================

# =========================== 程序运行日志配置项 ================================
# 日志输出根目录
file_path = 'D:\Python\PycharmProjects\Python-ETL\log'
# 日志输出文件名(每小时生成1个log)
log_time = time.strftime("%Y%m%d-%H", time.localtime(time.time()))
file_name = f'pyetl-{log_time}.log'
# ============================================================================
