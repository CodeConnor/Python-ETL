# coding:utf8
'''
用于采集后台日志文件（backend_logs）的业务逻辑
'''
from util.logging_util import Logging
from util.mysql_util import MySQLUtil
from config import project_config as conf

logger = Logging().init_logger()
logger.info("程序启动，开始采集后台日志文件（backend_logs）......")

# 建立数据库连接
metedata_db_util = MySQLUtil()
target_db_util = MySQLUtil(
    host=conf.target_host,
    port=conf.target_port,
    user=conf.target_user,
    password=conf.target_password
)

