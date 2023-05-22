# coding:utf8
# 功能逻辑：采集JSON数据（订单数据）到MySQL和CSV中
from util.logging_util import Logging
from util import file_util as fu
from config import project_config as conf

# 获取logger对象，用于后续输出日志
logger = Logging().init_logger()
logger.info('程序启动，开始读取JSON数据......')

# 获取JSON数据路径下的文件列表
files = fu.get_dir_files_list(conf.json_root_path)
logger.info(f'读取JSON数据路径，所获文件列表如下：{files}')
