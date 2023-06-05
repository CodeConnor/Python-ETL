# coding:utf8
'''
构建商品数据（barcode data）模型
'''
from util import str_util

class BarcodeModel:
    def __init__(self, code=None, name=None, spec=None, trademark=None,
                 addr=None, units=None, factory_name=None, trade_price=None,
                 retail_price=None, update_at=None, wholeunit=None,
                 wholenum=None, img=None, src=None):
        self.code = code
        self.name = str_util.clean_str(name)
        self.spec = str_util.clean_str(spec)
        self.trademark = str_util.clean_str(trademark)
        self.addr = str_util.clean_str(addr)
        self.units = str_util.clean_str(units)
        self.factory_name = str_util.clean_str(factory_name)
        self.trade_price = trade_price
        self.retail_price = retail_price
        self.update_at = update_at
        self.wholeunit = str_util.clean_str(wholeunit)
        self.wholenum = wholenum
        self.img = img
        self.src = src

