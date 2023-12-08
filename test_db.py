from PyQt6.QtCore import QThread
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtSql import QSqlDatabase, QSqlQueryModel, QSqlQuery
from reporter import *
import time, json
import pandas


class WorkerThread():
    def __init__(self):
        self.set_tb()
        self.ceate_table()

        # if not self.set_tb():
        #     self.set_tb()

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
        self.query.exec("create table if not exists  patient_info(id integer primary key AUTOINCREMENT ,"
                        " sample_code vchar,"
                        "name vchar, "
                        "gender_desc vchar, "
                        "birthday vchar, "
                        "sampling_time vchar,"
                        "risk vchar,"
                        "predict_pls vchar)")
        # self.query.exec('select * from patient_info')

        if self.query.lastError().isValid():
            print("Table create failed: ", self.query.lastError().text())
        else:
            print("Table created successfully")

        # print('insert --')
        self.db.close()

if __name__ == "__main__":
    t = WorkerThread()
    # t.ceate_table()
    # print(t.query.record())
    # print(t.query.result())
    print('finish')