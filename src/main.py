import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem
from PySide6.QtCore import Qt, Slot

from sqlite_helper import SQLiteDB


class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.db_helper = SQLiteDB('kangxi.db')
        self.setWindowTitle("name")
        self.setGeometry(100, 100, 600, 1000)
        self.col_name = ["字", "拼音", "笔画", "URL", "ID"]
        self.tableWidget = QTableWidget(self)
        self.init_ui()
        self.remove_data = []

    def init_ui(self):
        # 创建一个QTableWidget控件
        self.tableWidget.setGeometry(50, 50, 500, 800)
        self.tableWidget.setColumnCount(len(self.col_name))
        self.tableWidget.setHorizontalHeaderLabels(self.col_name)

        self.addTableRow()

        # 连接点击事件槽函数
        self.tableWidget.cellDoubleClicked.connect(self.onCellClicked)

    def addTableRow(self):
        # 添加一行数据
        res = self.db_helper.query_data("select word, ping_yin, bi_hua, uri, id  from word where bi_hua=12;")
        for data in res:
            row_position = self.tableWidget.rowCount()
            self.tableWidget.insertRow(row_position)
            for index in range(len(data)):
                self.tableWidget.setItem(row_position, index, QTableWidgetItem(str(data[index])))

    @Slot(int, int)
    def onCellClicked(self, row, _):
        # 获取点击的行和列
        self.tableWidget.removeRow(row)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec_())
