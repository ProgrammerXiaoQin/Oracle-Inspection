from rich.console import Console
from rich.table import Table
from rich.text import Text
from mkdir import LogWriter

class RichTablePrinter:
    def __init__(self):
        self.console = Console(record=True)

    def print_table(self,filename,title: tuple, rows: list):
        # 创建表格实例
        table = Table(show_header=True, header_style="bold magenta")

        # 添加标题列
        for column_title in title:
            table.add_column(column_title, style="")

        # 遍历每一行并添加到表格
        for row in rows:
            row_cells = []

            # 遍历每一列，并将以 "<>" 开头的字符串标记为红色
            for cell in row:
                if isinstance(cell,str) and cell.startswith("<>"):
                    row_cells.append(Text(cell[2:], style="red"))
                else:
                    row_cells.append(cell)
            table.add_row(*row_cells)

        # 输出表格
        self.console.print(table,overflow="fold")

        log_writer = LogWriter()
        log_writer.create_folder_and_append_file(filename,self.console.export_html())
#示例用法:
# rp = RichTablePrinter()
# rp.print_table(("Column1", "Column2"), [("<>Value1", "Value2"), ("Value3", "Value4")],"192.168.1.1")







