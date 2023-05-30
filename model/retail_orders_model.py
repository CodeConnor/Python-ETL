# coding:utf8
'''
通过模型(将数据封装到类里面,一个字段,作为类的一个成员变量)来进行数据处理
零售订单模型, 负责构建:
- 纯订单相关的数据模型(1对1的class模型)
- 订单和商品相关的数据模型(1对多的class模型)
'''
import json
from util import time_util, str_util
from config import project_config as conf


class OrdersModel:
    '''构建纯订单模型（不包含商品信息）'''

    def __init__(self, data: str):
        '''
        从传入的字符串数据构建订单model
        :param data: str，从JSON数据文件中读取的字符串信息
        '''
        data = json.loads(data)  # 将字符串转换为Python对象，根据字符串格式不同，所转换的Python对象的就不同，这里的字符串被转换为了字典
        # 成员变量（公共属性）
        self.discount_rate = data['discountRate']  # 折扣率
        self.store_shop_no = data['storeShopNo']  # 店铺店号（无用列）
        self.day_order_seq = data['dayOrderSeq']  # 本单为当日第几单
        self.store_district = data['storeDistrict']  # 店铺所在行政区
        self.is_signed = data['isSigned']  # 是否签约店铺（签约第三方支付体系）
        self.store_province = data['storeProvince']  # 店铺所在省份
        self.origin = data['origin']  # 原始信息（无用）
        self.store_gps_longitude = data['storeGPSLongitude']  # 店铺GPS经度
        self.discount = data['discount']  # 折扣金额
        self.store_id = data['storeID']  # 店铺ID
        self.product_count = data['productCount']  # 本单售卖商品数量
        self.operator_name = data['operatorName']  # 操作员姓名
        self.operator = data['operator']  # 操作员ID
        self.store_status = data['storeStatus']  # 店铺状态
        self.store_own_user_tel = data['storeOwnUserTel']  # 店铺店主电话
        self.pay_type = data['payType']  # 支付类型
        self.discount_type = data['discountType']  # 折扣类型
        self.store_name = data['storeName']  # 店铺名称
        self.store_own_user_name = data['storeOwnUserName']  # 店铺店主名称
        self.date_ts = data['dateTS']  # 订单时间
        self.small_change = data['smallChange']  # 找零金额
        self.store_gps_name = data['storeGPSName']  # 店铺GPS名称
        self.erase = data['erase']  # 是否抹零
        self.store_gps_address = data['storeGPSAddress']  # 店铺GPS地址
        self.order_id = data['orderID']  # 订单ID
        self.money_before_whole_discount = data['moneyBeforeWholeDiscount']  # 折扣前金额
        self.store_category = data['storeCategory']  # 店铺类别
        self.receivable = data['receivable']  # 应收金额
        self.face_id = data['faceID']  # 面部识别ID
        self.store_own_user_id = data['storeOwnUserId']  # 店铺店主ID
        self.payment_channel = data['paymentChannel']  # 付款通道
        self.payment_scenarios = data['paymentScenarios']  # 付款情况（无用）
        self.store_address = data['storeAddress']  # 店铺地址
        self.total_no_discount = data['totalNoDiscount']  # 整体价格（无折扣）
        self.payed_total = data['payedTotal']  # 已付款金额
        self.store_gps_latitude = data['storeGPSLatitude']  # 店铺GPS纬度
        self.store_create_date_ts = data['storeCreateDateTS']  # 店铺创建时间
        self.store_city = data['storeCity']  # 店铺所在城市
        self.member_id = data['memberID']  # 会员ID

    def check_and_transform_area(self):
        '''
        检查数据中省市区字段是否无意义，若无意义则将对应字符串替换为“未知”
        :return:
        '''
        if str_util.check_null(self.store_province):
            self.store_province = '未知省份'
        if str_util.check_null(self.store_city):
            self.store_city = '未知城市'
        if str_util.check_null(self.store_district):
            self.store_district = '未知行政区'

    def to_csv(self, sep=','):
        '''
        该方法用于将类中存储的数据转换为csv结构的字符串，以参数（sep）传入的符号作为分隔符
        :param sep: csv中的分隔符
        :return: str，csv格式的字符串
        '''
        self.check_and_transform_area()  # 将无意义省市区字符串替换掉
        csv_line = \
            f"{self.order_id}{sep}" \
            f"{self.store_id}{sep}" \
            f"{self.store_name}{sep}" \
            f"{self.store_status}{sep}" \
            f"{self.store_own_user_id}{sep}" \
            f"{self.store_own_user_name}{sep}" \
            f"{self.store_own_user_tel}{sep}" \
            f"{self.store_category}{sep}" \
            f"{self.store_address}{sep}" \
            f"{self.store_shop_no}{sep}" \
            f"{self.store_province}{sep}" \
            f"{self.store_city}{sep}" \
            f"{self.store_district}{sep}" \
            f"{self.store_gps_name}{sep}" \
            f"{self.store_gps_address}{sep}" \
            f"{self.store_gps_longitude}{sep}" \
            f"{self.store_gps_latitude}{sep}" \
            f"{self.is_signed}{sep}" \
            f"{self.operator}{sep}" \
            f"{self.operator_name}{sep}" \
            f"{self.face_id}{sep}" \
            f"{self.member_id}{sep}" \
            f"{time_util.ts13_to_date_str(self.store_create_date_ts)}{sep}" \
            f"{self.origin}{sep}" \
            f"{self.day_order_seq}{sep}" \
            f"{self.discount_rate}{sep}" \
            f"{self.discount_type}{sep}" \
            f"{self.discount}{sep}" \
            f"{self.money_before_whole_discount}{sep}" \
            f"{self.receivable}{sep}" \
            f"{self.erase}{sep}" \
            f"{self.small_change}{sep}" \
            f"{self.total_no_discount}{sep}" \
            f"{self.payed_total}{sep}" \
            f"{self.pay_type}{sep}" \
            f"{self.payment_channel}{sep}" \
            f"{self.payment_scenarios}{sep}" \
            f"{self.product_count}{sep}" \
            f"{time_util.ts13_to_date_str(self.date_ts)}"

        return csv_line

    def generate_insert_sql(self):
        '''
        将模型转换为一条INSERT SQL语句
        :return: SQL语句
        '''
        sql = f"INSERT IGNORE INTO {conf.target_orders_table_name}(" \
              f"order_id,store_id,store_name,store_status,store_own_user_id," \
              f"store_own_user_name,store_own_user_tel,store_category," \
              f"store_address,store_shop_no,store_province,store_city," \
              f"store_district,store_gps_name,store_gps_address," \
              f"store_gps_longitude,store_gps_latitude,is_signed," \
              f"operator,operator_name,face_id,member_id,store_create_date_ts," \
              f"origin,day_order_seq,discount_rate,discount_type,discount," \
              f"money_before_whole_discount,receivable,erase,small_change," \
              f"total_no_discount,pay_total,pay_type,payment_channel," \
              f"payment_scenarios,product_count,date_ts" \
              f") VALUES(" \
              f"'{self.order_id}', " \
              f"{self.store_id}, " \
              f"{str_util.check_str_null_and_transform_to_sql_null(self.store_name)}, " \
              f"{str_util.check_str_null_and_transform_to_sql_null(self.store_status)}, " \
              f"{self.store_own_user_id}, " \
              f"{str_util.check_str_null_and_transform_to_sql_null(self.store_own_user_name)}, " \
              f"{str_util.check_str_null_and_transform_to_sql_null(self.store_own_user_tel)}, " \
              f"{str_util.check_str_null_and_transform_to_sql_null(self.store_category)}, " \
              f"{str_util.check_str_null_and_transform_to_sql_null(self.store_address)}, " \
              f"{str_util.check_str_null_and_transform_to_sql_null(self.store_shop_no)}, " \
              f"{str_util.check_str_null_and_transform_to_sql_null(self.store_province)}, " \
              f"{str_util.check_str_null_and_transform_to_sql_null(self.store_city)}, " \
              f"{str_util.check_str_null_and_transform_to_sql_null(self.store_district)}, " \
              f"{str_util.check_str_null_and_transform_to_sql_null(self.store_gps_name)}, " \
              f"{str_util.check_str_null_and_transform_to_sql_null(self.store_gps_address)}, " \
              f"{str_util.check_str_null_and_transform_to_sql_null(self.store_gps_longitude)}, " \
              f"{str_util.check_str_null_and_transform_to_sql_null(self.store_gps_latitude)}, " \
              f"{self.is_signed}, " \
              f"{str_util.check_str_null_and_transform_to_sql_null(self.operator)}, " \
              f"{str_util.check_str_null_and_transform_to_sql_null(self.operator_name)}, " \
              f"{str_util.check_str_null_and_transform_to_sql_null(self.face_id)}, " \
              f"{str_util.check_str_null_and_transform_to_sql_null(self.member_id)}, " \
              f"'{time_util.ts13_to_date_str(self.store_create_date_ts)}', " \
              f"{str_util.check_str_null_and_transform_to_sql_null(self.origin)}, " \
              f"{self.day_order_seq}, " \
              f"{self.discount_rate}, " \
              f"{self.discount_type}, " \
              f"{self.discount}, " \
              f"{self.money_before_whole_discount}, " \
              f"{self.receivable}, " \
              f"{self.erase}, " \
              f"{self.small_change}, " \
              f"{self.total_no_discount}, " \
              f"{self.payed_total}, " \
              f"{str_util.check_str_null_and_transform_to_sql_null(self.pay_type)}, " \
              f"{self.payment_channel}, " \
              f"{str_util.check_str_null_and_transform_to_sql_null(self.payment_scenarios)}, " \
              f"{self.product_count}, " \
              f"'{time_util.ts13_to_date_str(self.date_ts)}')"

        return sql


class OrdersDetailModel:
    '''订单详情模型，包含订单ID + 商品详情数据'''

    def __init__(self, data: str):
        '''
        从传入的字符串数据构建订单详情model
        :param data: str，从JSON数据文件中读取的字符串信息
        '''
        data = json.loads(data)  # 将字符串转换为json对象
        self.order_id = data['orderID']  # 订单ID
        self.product = []


if __name__ == '__main__':
    data = {"discountRate": 1, "storeShopNo": "None", "dayOrderSeq": 37, "storeDistrict": "芙蓉区", "isSigned": 0,
            "storeProvince": "湖南省", "origin": 0, "storeGPSLongitude": "undefined", "discount": 0, "storeID": 1766,
            "productCount": 1, "operatorName": "OperatorName", "operator": "NameStr", "storeStatus": "open",
            "storeOwnUserTel": 12345678910, "payType": "cash", "discountType": 2, "storeName": "亿户超市郭一一食品店",
            "storeOwnUserName": "OwnUserNameStr", "dateTS": 1542436490000, "smallChange": 0, "storeGPSName": "None",
            "erase": 0, "product": [
            {"count": 1, "name": "南京特醇", "unitID": 8, "barcode": "6901028300056", "pricePer": 12, "retailPrice": 12,
             "tradePrice": 11, "categoryID": 1}], "storeGPSAddress": "None", "orderID": "154243648991517662217",
            "moneyBeforeWholeDiscount": 12, "storeCategory": "normal", "receivable": 12, "faceID": "",
            "storeOwnUserId": 1694, "paymentChannel": 0, "paymentScenarios": "OTHER", "storeAddress": "StoreAddress",
            "totalNoDiscount": 12, "payedTotal": 12, "storeGPSLatitude": "undefined",
            "storeCreateDateTS": 1540793134000, "storeCity": "长沙市", "memberID": "0"}
    data = json.dumps(data)
    model = OrdersModel(data)
    print(model.generate_insert_sql())

    data_detail = '{"discountRate": 1, "storeShopNo": "None", "dayOrderSeq": 28, "storeDistrict": "天心区", "isSigned": 0, "storeProvince": "湖南省", "origin": 0, "storeGPSLongitude": "112.96973", "discount": 0, "storeID": 1732, "productCount": 2, "operatorName": "OperatorName", "operator": "NameStr", "storeStatus": "open", "storeOwnUserTel": 12345678910, "payType": "cash", "discountType": 2, "storeName": "佳时利超市", "storeOwnUserName": "OwnUserNameStr", "dateTS": 1542436491000, "smallChange": 0, "storeGPSName": "None", "erase": 0, "product": [{"count": 1, "name": "维他命水柠檬味500ml", "unitID": 2, "barcode": "6921168550128", "pricePer": 5, "retailPrice": 5, "tradePrice": 0, "categoryID": 11}, {"count": 1, "name": "欢乐家生榨椰子汁5L", "unitID": 2, "barcode": "6924254686299", "pricePer": 13.5, "retailPrice": 13.5, "tradePrice": 0, "categoryID": 11}], "storeGPSAddress": "None", "orderID": "154243649043817324304", "moneyBeforeWholeDiscount": 18.5, "storeCategory": "normal", "receivable": 18.5, "faceID": "", "storeOwnUserId": 1656, "paymentChannel": 0, "paymentScenarios": "OTHER", "storeAddress": "StoreAddress", "totalNoDiscount": 18.5, "payedTotal": 18.5, "storeGPSLatitude": "28.083906", "storeCreateDateTS": 1540619466000, "storeCity": "长沙市", "memberID": "0"}'
