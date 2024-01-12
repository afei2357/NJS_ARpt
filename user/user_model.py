from PyQt6.QtCore import Qt

from PyQt6.QtSql import  QSqlQueryModel, QSqlQuery,QSqlTableModel,QSqlRecord

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


    def add_user(self, data):
        """Add a contact to the database."""
        rows = self.queryModel.rowCount()
        self.queryModel.insertRows(rows, 1)
        for column, field in enumerate(data):
            print('rows,columns,field--------')
            print(rows,column,field)
            self.queryModel.setData(self.queryModel.index(rows, column + 1), field)
        self.queryModel.submitAll()
        self.queryModel.select()

    def edit_user(self, data):
        """Add a contact to the database."""
        # rows = self.queryModel.rowCount()
        # id = data['id']
        print('in edit users 1')
        print(data)
        # 下面3个代码也可以，只是不那么优雅
        # self.queryModel.setData(self.queryModel.index(int(data['row']),  1), data['username'])
        # self.queryModel.setData(self.queryModel.index(data['row'],  2), data['password'])
        # self.queryModel.setData(self.queryModel.index(data['row'],  3), data['role'])
        # 使用如下来替代：
        row = data['row']
        record = self.queryModel.record(row)
        record.setValue('username', data['username'])
        record.setValue('password', data['password'])
        record.setValue('role', data['role'])
        self.queryModel.setRecord(row,record)

        self.queryModel.submitAll()
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
