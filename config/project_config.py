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


# =========================== JSON订单数据采集csv配置项 start ================================
# JSON数据所在路径
json_root_path = 'D:/Python/pyetl-data/json/'

# 数据写出到CSV文件的目录路径
retail_output_csv_root_path = 'D:/Python/pyetl-data/output/csv/'
# 订单模型数据写出到CSV文件的文件名
retail_orders_output_csv_file_name = f'orders-{time.strftime("%Y%m%d-%H%M%S", time.localtime(time.time()))}.csv'
# 订单详情模型数据写出到CSV文件的文件名
retail_orders_detail_output_csv_file_name = f'orders-detail-{time.strftime("%Y%m%d-%H%M%S", time.localtime(time.time()))}.csv'
# =========================== JSON订单数据采集配置项 end ==================================

# =========================== barcode数据采集csv配置项 start ================================
# barcode数据写出到CSV文件的目录路径
barcode_output_csv_root_path = 'D:/Python/pyetl-data/output/csv/'
# 订单模型数据写出到CSV文件的文件名
barcode_output_csv_file_name = f'barcode-{time.strftime("%Y%m%d-%H%M%S", time.localtime(time.time()))}.csv'

# =========================== JSON订单数据采集配置项 end ==================================


# ============================= mysql 配置 start =======================================
# ################### 元数据管理库配置 ############################
metadata_host = 'localhost'
metadata_port = 3306
metadata_user = 'root'
metadata_password = '123456'
mysql_charset = 'utf8'

metadata_db_name = 'metadata'  # 元数据库名称
# 文件监控表（文件元数据表），记录哪些文件已被处理
metadata_file_monitor_table_name = 'file_monitor'
# 元数据表建表语句
metadata_file_monitor_table_create_cols = '''
    id INT AUTO_INCREMENT PRIMARY KEY,
    file_name VARCHAR(50) UNIQUE NOT NULL COMMENT '被处理文件文件名',
    process_lines INT COMMENT '被处理文件数据条数',
    process_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '文件处理时间'
'''

# 记录barcode数据表的update_at字段的元数据表
metadata_barcode_monitor_table_name = 'barcode_monitor'
metadata_barcode_monitor_table_create_cols = "" \
                                             "id INT PRIMARY KEY AUTO_INCREMENT COMMENT '自增ID', " \
                                             "time_record TIMESTAMP NOT NULL COMMENT '本次采集记录的最大时间', " \
                                             "gather_line_count INT NULL COMMENT '本次采集条数'"

# 记录backend_logs数据的元数据表
metadata_backend_logs_monitor_table_name = "backend_logs_monitor"
metadata_backend_logs_monitor_table_create_cols = "" \
                                                  "id INT PRIMARY KEY AUTO_INCREMENT COMMENT '自增ID'," \
                                                  "file_name VARCHAR(50) UNIQUE NOT NULL COMMENT '被处理文件文件名'," \
                                                  "process_lines INT COMMENT '被处理文件数据条数'," \
                                                  "process_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '文件处理时间'"

# #################### 目标数据库配置 ######################
target_host = 'localhost'
target_port = 3306
target_user = 'root'
target_password = '123456'
target_db_name = 'retail'  # 目标数据库
target_orders_table_name = 'orders'  # 订单信息表(不含商品详情信息)
# 订单信息表建表
target_orders_table_create_cols = \
    f"order_id VARCHAR(255) PRIMARY KEY, " \
    f"store_id INT COMMENT '店铺ID', " \
    f"store_name VARCHAR(30) COMMENT '店铺名称', " \
    f"store_status VARCHAR(10) COMMENT '店铺状态(open,close)', " \
    f"store_own_user_id INT COMMENT '店主id', " \
    f"store_own_user_name VARCHAR(50) COMMENT '店主名称', " \
    f"store_own_user_tel VARCHAR(15) COMMENT '店主手机号', " \
    f"store_category VARCHAR(10) COMMENT '店铺类型(normal,test)', " \
    f"store_address VARCHAR(255) COMMENT '店铺地址', " \
    f"store_shop_no VARCHAR(255) COMMENT '店铺第三方支付id号', " \
    f"store_province VARCHAR(10) COMMENT '店铺所在省', " \
    f"store_city VARCHAR(10) COMMENT '店铺所在市', " \
    f"store_district VARCHAR(10) COMMENT '店铺所在行政区', " \
    f"store_gps_name VARCHAR(255) COMMENT '店铺gps名称', " \
    f"store_gps_address VARCHAR(255) COMMENT '店铺gps地址', " \
    f"store_gps_longitude VARCHAR(255) COMMENT '店铺gps经度', " \
    f"store_gps_latitude VARCHAR(255) COMMENT '店铺gps纬度', " \
    f"is_signed TINYINT COMMENT '是否第三方支付签约(0,1)', " \
    f"operator VARCHAR(10) COMMENT '操作员', " \
    f"operator_name VARCHAR(50) COMMENT '操作员名称', " \
    f"face_id VARCHAR(255) COMMENT '顾客面部识别ID', " \
    f"member_id VARCHAR(255) COMMENT '顾客会员ID', " \
    f"store_create_date_ts TIMESTAMP COMMENT '店铺创建时间', " \
    f"origin VARCHAR(255) COMMENT '原始信息(无用)', " \
    f"day_order_seq INT COMMENT '本订单是当日第几单', " \
    f"discount_rate DECIMAL(10, 5) COMMENT '折扣率', " \
    f"discount_type TINYINT COMMENT '折扣类型', " \
    f"discount DECIMAL(10, 5) COMMENT '折扣金额', " \
    f"money_before_whole_discount DECIMAL(10, 5) COMMENT '折扣前总金额', " \
    f"receivable DECIMAL(10, 5) COMMENT '应收金额', " \
    f"erase DECIMAL(10, 5) COMMENT '抹零金额', " \
    f"small_change DECIMAL(10, 5) COMMENT '找零金额', " \
    f"total_no_discount DECIMAL(10, 5) COMMENT '总价格(无折扣)', " \
    f"pay_total DECIMAL(10, 5) COMMENT '付款金额', " \
    f"pay_type VARCHAR(10) COMMENT '付款类型', " \
    f"payment_channel TINYINT COMMENT '付款通道', " \
    f"payment_scenarios VARCHAR(15) COMMENT '付款描述(无用)', " \
    f"product_count INT COMMENT '本单卖出多少商品', " \
    f"date_ts TIMESTAMP COMMENT '订单时间', " \
    f"INDEX (receivable), INDEX (date_ts)"

target_orders_detail_table_name = 'orders_detail'  # 订单详情表(含商品详情信息)
# 订单详情表建表
target_orders_detail_table_create_cols = \
    f"order_id VARCHAR(255) COMMENT '订单ID', " \
    f"barcode VARCHAR(255) COMMENT '商品条码', " \
    f"name VARCHAR(255) COMMENT '商品名称', " \
    f"count INT COMMENT '本单此商品卖出数量', " \
    f"price_per DECIMAL(10, 5) COMMENT '实际售卖单价', " \
    f"retail_price DECIMAL(10, 5) COMMENT '零售建议价', " \
    f"trade_price DECIMAL(10, 5) COMMENT '贸易价格(进货价)', " \
    f"category_id INT COMMENT '商品类别ID', " \
    f"unit_id INT COMMENT '商品单位ID(包、袋、箱、等)', " \
    f"PRIMARY KEY (order_id, barcode)"

# #################采集barcode数据，写入MySQL的表名与建表#####################
target_barcode_table_name = "barcode"  # barcode数据表（商品数据表）
# barcode数据表建表
target_barcode_table_create_cols = """
`code` varchar(50) PRIMARY KEY COMMENT '商品条码',
`name` varchar(200) DEFAULT '' COMMENT '商品名称',
`spec` varchar(200) DEFAULT '' COMMENT '商品规格',
`trademark` varchar(100) DEFAULT '' COMMENT '商品商标',
`addr` varchar(200) DEFAULT '' COMMENT '商品产地',
`units` varchar(50) DEFAULT '' COMMENT '商品单位(个、杯、箱、等)',
`factory_name` varchar(200) DEFAULT '' COMMENT '生产厂家',
`trade_price` DECIMAL(50, 5) DEFAULT 0.0 COMMENT '贸易价格(指导进价)',
`retail_price` DECIMAL(50, 5) DEFAULT 0.0 COMMENT '零售价格(建议卖价)',
`update_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
`wholeunit` varchar(50) DEFAULT NULL COMMENT '大包装单位',
`wholenum` int(11) DEFAULT NULL COMMENT '大包装内装数量',
`img` varchar(500) DEFAULT NULL COMMENT '商品图片',
`src` varchar(20) DEFAULT NULL COMMENT '源信息', 
INDEX (update_at)
"""

# ################## 采集后台日志数据，写入目标数据库 ################
# backend_logs所在目录
backend_logs_root_path = "D:/Python/pyetl-data/backend_logs/"

target_backend_logs_table_name = "backend_logs"  # 后台日志表
target_backend_logs_table_create_cols = "" \
                                        "id INT PRIMARY KEY AUTO_INCREMENT COMMENT '自增ID'" \
                                        "log_time TIMESTAMP(6) COMMENT '日志时间, 精确到6位毫秒'," \
                                        "log_level VARCHAR(10) COMMENT '日志等级'," \
                                        "log_module VARCHAR(255) COMMENT '代码模块'," \
                                        "response_time INT COMMENT '接口响应时间'," \
                                        "caller_province VARCHAR(20) COMMENT '调用者省份'," \
                                        "caller_city VARCHAR(20) COMMENT '调用者城市'," \
                                        "log_info VARCHAR(255) COMMENT '日志信息'"

# backend_logs数据写出到CSV文件的目录路径
backend_logs_output_csv_root_path = 'D:/Python/pyetl-data/output/csv/'
# 订单模型数据写出到CSV文件的文件名
backend_logs_output_csv_file_name = f'backend_logs-{time.strftime("%Y%m%d-%H%M%S", time.localtime(time.time()))}.csv'

# ###################### 业务数据源数据库配置 ###########################
source_host = 'localhost'
source_port = 3306
source_user = 'root'
source_password = '123456'
source_db_name = 'source_data'
source_barcode_table_name = 'sys_barcode'

# ============================= mysql 配置 end =========================================
