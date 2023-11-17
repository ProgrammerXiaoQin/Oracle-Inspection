import os
from datetime import datetime

class LogWriter:
    def __init__(self):
        pass

    def create_folder_and_append_file(self, filename, date):
        # 获取当前日期和时间
        now = datetime.now()

        # 获取当前月份和日期
        current_month = now.strftime("%Y-%m")
        current_date = now.strftime("%Y-%m-%d")

        # 创建文件夹路径
        logs_folder_path = os.path.join(os.getcwd(), 'logs')
        month_folder_path = os.path.join(logs_folder_path, current_month)
        folder_path = os.path.join(month_folder_path, current_date)

        # 检查月份文件夹是否存在，如果不存在则创建
        if not os.path.exists(month_folder_path):
            os.makedirs(month_folder_path)

        # 检查日期文件夹是否存在，如果不存在则创建
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

        # 创建文件路径
        file_path = os.path.join(folder_path, f"{filename}.html")  # 使用 .html 扩展名

        # 打开文件以追加内容
        with open(file_path, 'a', encoding="utf-8") as file:
            # 写入内容
            file.write(f"\n{date}")


# 创建类的实例
# log_writer = LogWriter()

# 调用方法
# log_writer.create_folder_and_append_file("example", "2023-11-15")
