from PyQt6.QtCore import Qt

from PyQt6.QtSql import  QSqlQueryModel, QSqlQuery,QSqlTableModel,QSqlRecord
from werkzeug.security import generate_password_hash, check_password_hash

import logging.config
import logging

config_path = './config/logging.ini'
logging.config.fileConfig(config_path)
logger = logging.getLogger('worker')



class User():
    def __init__(self,db):
        self.db = db
        self.queryModel = QSqlTableModel(None,db)
        self.queryModel.setTable('users')
        self.queryModel.select()
        # self.queryModel.setEditStrategy(QSqlTableModel.OnFieldChange)
        self.queryModel.setHeaderData(1, Qt.Orientation.Horizontal, "姓名")
        self.queryModel.setHeaderData(3, Qt.Orientation.Horizontal, "角色")
        self.queryModel.setHeaderData(2, Qt.Orientation.Horizontal, "密码")

    def set_password(self, password):
        '''设置用户密码，保存为 Hash 值'''
        self.password_hash = generate_password_hash(password)
        return self.password_hash
    def check_login(self,username,password):
        logger.info(username)
        self.queryModel.setFilter("username ='" + username + "'")
        if self.queryModel.rowCount() == 0:
            logger.info(username)
            return False
        else:
            record = self.queryModel.record(0)
            logger.info(record)
            logger.info(record.value('username'))
            password_hash = record.value('password_hash')
            logger.info(password_hash)
            if check_password_hash(password_hash,password):
                return True
            # else:
            #     logger.info(username)
                # return '密码不正确'

    def check_password(self, password):
        '''验证密码与保存的 Hash 值是否匹配'''
        return check_password_hash(self.password_hash, password)

    def add_user_old(self, data):
        """Add a contact to the database."""
        rows = self.queryModel.rowCount()
        self.queryModel.insertRows(rows, 1)
        for column, field in enumerate(data):
            print('rows,columns,field--------')
            print(rows,column,field)
            self.queryModel.setData(self.queryModel.index(rows, column + 1), field)
        self.queryModel.submitAll()
        self.queryModel.select()

    def add_user(self, data):
        """Add a contact to the database."""
        row = self.queryModel.rowCount()
        self.queryModel.insertRows(row, 1)
        logger.info(data)
        password_hash = self.set_password(data['password'])
        self.queryModel.setData(self.queryModel.index(row,  1), data['username'])
        self.queryModel.setData(self.queryModel.index(row,  2), password_hash)
        self.queryModel.setData(self.queryModel.index(row,  3), data['role'])
        logger.info(data)

        self.queryModel.submitAll()
        logger.info(self.queryModel)
        self.queryModel.select()
        logger.info(data)

    def get_data(self,row):
        record = self.queryModel.record(row)
        username = record.value('username')
        password_hash = record.value('password_hash')
        role = record.value('role')
        data = {"username":username,'password_hash':password_hash,'role':role,"id":id,'row':row }
        return data

    def edit_user(self, data):
        """Add a contact to the database."""
        # rows = self.queryModel.rowCount()
        # id = data['id']
        logger.info('edit ')
        # 下面3个代码也可以，只是不那么优雅
        # self.queryModel.setData(self.queryModel.index(int(data['row']),  1), data['username'])
        # self.queryModel.setData(self.queryModel.index(data['row'],  2), data['password'])
        # self.queryModel.setData(self.queryModel.index(data['row'],  3), data['role'])
        # 使用如下来替代：
        row = data['row']
        record = self.queryModel.record(row)
        logger.info('edit ')
        record.setValue('username', data['username'])
        logger.info('edit ')
        password_hash = self.set_password(data['password'])
        logger.info('edit ')
        record.setValue('password_hash', password_hash)
        logger.info('edit ')
        record.setValue('role', data['role'])
        logger.info('edit ')
        self.queryModel.setRecord(row,record)
        logger.info('edit ')

        self.queryModel.submitAll()
        logger.info('edit ')
        self.queryModel.select()



    def delete_user(self, row):
        """Remove a contact from the database."""
        print('delete user ---')
        self.queryModel.removeRow(row)
        self.queryModel.submitAll()
        self.queryModel.select()

    def query_user(self,condition):
        self.queryModel.setFilter(condition)
        self.queryModel.select()
