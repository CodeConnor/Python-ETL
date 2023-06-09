# coding:utf8
'''构建后台日志文件的模型'''
from config import project_config as conf


class BackendLogsModel:
    def __init__(self, data: str):
        """
        初始化数据，构建model
        :param data: str，传入的log文件字符串
        """
        log_data = data.split("\t")
        self.log_time = log_data[0]
        self.log_level = log_data[1]
        self.backend_file_name = log_data[2]
        # 使用filter()函数结合isdigit()方法来过滤出字符串中的数字字符，并使用join()函数将其连接起来，最后再转换为int类型
        self.response_time = int(''.join(filter(str.isdigit, log_data[3])))
        self.caller_province = log_data[4]
        self.caller_city = log_data[5]
        self.log_info = log_data[6]

    def generate_insert_sql(self):
        """
        使用初始化后的数据生成sql
        :return: sql，目标数据库插入语句
        """
        sql = f"""
            INSERT IGNORE INTO {conf.target_backend_logs_table_name} 
            VALUES (
                {self.log_time},
                {self.log_level},
                {self.backend_file_name},
                {self.response_time},
                {self.caller_province},
                {self.caller_city},
                {self.log_info}
            )
        """
        return sql

    def to_csv(self, sep=","):
        """
        使用初始化后的数据生成csv
        :return: csv_line，生成的每行csv数据
        """
        csv_line = f"" \
                   f"{self.log_time}{sep}" \
                   f"{self.log_level}{sep}" \
                   f"{self.backend_file_name}{sep}" \
                   f"{self.response_time}{sep}" \
                   f"{self.caller_province}{sep}" \
                   f"{self.caller_city}{sep}" \
                   f"{self.log_info}"

        return csv_line


if __name__ == '__main__':
    log = "2023-06-08 18:21:52.491697	[INFO]	event.py	响应时间:866ms	广东省	珠海市	这里是日志信息......"
    model = BackendLogsModel(log)
    print(model.to_csv())
    print(model.generate_insert_sql())
    print(type(model.response_time))
