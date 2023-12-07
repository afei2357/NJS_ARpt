from PyQt6.QtCore import QThread
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtSql import QSqlDatabase, QSqlQueryModel, QSqlQuery
from reporter import *
import time, json
import pandas


class WorkerThread():
    def __init__(self):
        if not self.set_tb():
            self.ceate_table()
            self.set_tb()

    # signal = pyqtSignal()
    def insert_tb(self):
        self.query.exec('insert into ')
    def set_tb(self):
        print('set_tb')
        self.db = QSqlDatabase.addDatabase('QSQLITE')
        # 设置数据库名称
        self.db.setDatabaseName('./db/database.db')
        # 打开数据库
        self.db.open()
        # 判断是否打开
        if not self.db.open():
            return False

        # 声明数据库查询对象
        self.query = QSqlQuery()
        return True
        # self.db.close()

    def ceate_table(self):
        self.query.exec("create table patient_info(id int primary key,"
                        " sample_code vchar,"
                        "name vchar, "
                        "gender_desc vchar, "
                        "birthday vchar, "
                        "sample_date vchar,"
                        "risk vchar,"
                        "predict_pls vchar)")

if __name__ == "__main__":
    t = WorkerThread()
    t.ceate_table()