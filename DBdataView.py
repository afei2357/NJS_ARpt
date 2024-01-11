from NJS_ARpt_project.UI.Ui_MainWindow import Ui_MainWindow
from PyQt6.QtWidgets import *
import sys
import re
from PyQt6.QtWidgets import (QApplication, QHeaderView , QMessageBox)
from PyQt6.QtCore import Qt
from PyQt6.QtSql import QSqlDatabase, QSqlQueryModel, QSqlQuery


def createTableAndInit():
    # 添加数据库
    db = QSqlDatabase.addDatabase('QSQLITE')
    # 设置数据库名称
    db.setDatabaseName('./db/database.db')
    # 判断是否打开
    if not db.open():
        return False

    # 声明数据库查询对象
    query = QSqlQuery()
    # 创建表
    query.exec("create table student(id int primary key, name vchar, sex vchar, age int, deparment vchar)")

    # 添加记录
    query.exec("insert into student values(1,'张三1','男',20,'计算机')")
    query.exec("insert into student values(2,'李四1','男',19,'经管')")
    query.exec("insert into student values(3,'王五1','男',22,'机械')")
    db.close()
    return True


class DBdataView(QMainWindow,Ui_MainWindow):
    def __init__(self, parent=None):
        super(DBdataView, self).__init__(parent)
        self.setupUi(self)
        # 查询模型
        self.queryModel = None
        # 数据表
        # self.tableView = None
        # 总数页文本
        # self.totalPageLabel = None
        # 当前页文本
        # self.currentPageLabel = None
        # 转到页输入框
        # self.switchPageLineEdit = None
        # 前一页按钮
        # self.prevButton = None
        # 后一页按钮
        # self.nextButton = None
        # 转到页按钮
        # self.switchPageButton = None
        # 当前页
        self.currentPage = 0
        # 总页数
        self.totalPage = 0
        # 总记录数
        self.totalRecrodCount = 0
        # 每页显示记录数
        self.PageRecordCount = 20
        self.db = None
        print('----initInDataview -----'*20)
        self.initUI()

    def initUI(self):
        # 创建窗口
        # self.createWindow()
        # 设置表格
        self.setTableView()

        # # 信号槽连接
        self.prevButton.clicked.connect(self.onPrevButtonClick)
        self.nextButton.clicked.connect(self.onNextButtonClick)
        self.switchPageButton.clicked.connect(self.onSwitchPageButtonClick)


        # 设置表格属性
        # self.tableView = QTableView()
        # 表格宽度的自适应调整
        self.tableView.horizontalHeader().setStretchLastSection(True)
        self.tableView.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)

    def setTableView(self):
        print('*** step2 SetTableView')
        self.db = QSqlDatabase.addDatabase('QSQLITE')
        # 设置数据库名称
        self.db.setDatabaseName('./db/database.db')
        # 打开数据库
        self.db.open()
        # 声明查询模型
        self.queryModel = QSqlQueryModel(self)
        self.reset_table_view()
    def reset_table_view(self):
        # 设置当前页
        self.currentPage = 1
        # 得到总记录数
        self.totalRecrodCount = self.getTotalRecordCount()
        # 得到总页数
        self.totalPage = self.getPageCount()
        # 刷新状态
        self.updateStatus()
        # 设置总页数文本
        self.setTotalPageLabel()
        # 设置总记录数
        self.setTotalRecordLabel()
        # 记录查询
        self.recordQuery(0)
        # 设置模型
        self.tableView.setModel(self.queryModel)

        print('totalRecrodCount=' + str(self.totalRecrodCount))
        print('totalPage=' + str(self.totalPage))

        # 设置表格表头
        self.queryModel.setHeaderData(0, Qt.Orientation.Horizontal, "id")
        self.queryModel.setHeaderData(1, Qt.Orientation.Horizontal, "编号")
        self.queryModel.setHeaderData(2, Qt.Orientation.Horizontal, "姓名")
        self.queryModel.setHeaderData(3, Qt.Orientation.Horizontal, "性别")
        self.queryModel.setHeaderData(4, Qt.Orientation.Horizontal, "年龄")
        self.queryModel.setHeaderData(5, Qt.Orientation.Horizontal, "采样日期")
        self.queryModel.setHeaderData(6, Qt.Orientation.Horizontal, "风险区间")
        self.queryModel.setHeaderData(7, Qt.Orientation.Horizontal, "风险值")

    # 得到记录数
    def getTotalRecordCount(self):
        self.queryModel.setQuery("select * from patient_info")
        rowCount = self.queryModel.rowCount()
        print('rowCount==' + str(rowCount))
        return rowCount

    # 得到页数
    def getPageCount(self):
        print('in getPageCount1',self.totalRecrodCount ,self.PageRecordCount)
        print('in getPageCount2',self.totalRecrodCount /self.PageRecordCount)
        if self.totalRecrodCount % self.PageRecordCount == 0:
            return (self.totalRecrodCount / self.PageRecordCount)
        else:
            return (self.totalRecrodCount % self.PageRecordCount + 1)

    # 记录查询
    def recordQuery(self, limitIndex):
        szQuery = ("select * from patient_info limit %d,%d" % (limitIndex, self.PageRecordCount))
        print('query sql=' + szQuery)
        self.queryModel.setQuery(szQuery)

    # 刷新状态
    def updateStatus(self):
        szCurrentText = ("当前第%d页" % self.currentPage)
        self.currentPageLabel.setText(szCurrentText)
        print(' self.currentPage == self.totalPage')
        print( self.currentPage,  self.totalPage)
        # 设置按钮是否可用
        if self.currentPage == 1:
            self.prevButton.setEnabled(False)
            self.nextButton.setEnabled(True)
        elif self.currentPage == self.totalPage:
            self.prevButton.setEnabled(True)
            self.nextButton.setEnabled(False)
        else:
            self.prevButton.setEnabled(True)
            self.nextButton.setEnabled(True)

    # 设置总数页文本
    def setTotalPageLabel(self):
        szPageCountText = ("总共%d页" % self.totalPage)
        self.totalPageLabel.setText(szPageCountText)

    # 设置总记录数
    def setTotalRecordLabel(self):
        szTotalRecordText = ("共%d条" % self.totalRecrodCount)
        print('*** setTotalRecordLabel szTotalRecordText=' + szTotalRecordText)
        self.totalRecordLabel.setText(szTotalRecordText)

    # 前一页按钮按下
    def onPrevButtonClick(self):
        print('*** onPrevButtonClick ');
        limitIndex = (self.currentPage - 2) * self.PageRecordCount
        self.recordQuery(limitIndex)
        self.currentPage -= 1
        self.updateStatus()

    # 后一页按钮按下
    def onNextButtonClick(self):
        print('*** onNextButtonClick ');
        limitIndex = self.currentPage * self.PageRecordCount
        self.recordQuery(limitIndex)
        self.currentPage += 1
        self.updateStatus()
        print('next click ----------',self.currentPage ,self.totalPage)

    # 转到页按钮按下
    def onSwitchPageButtonClick(self):
        # 得到输入字符串
        szText = self.switchPageLineEdit.text()
        print('szText')
        print(szText)
        # 数字正则表达式
        pattern = re.compile(r'^[-+]?[0-9]+\.[0-9]+$')
        match = pattern.match(szText)

        # 判断是否为数字
        if match:
            QMessageBox.information(self, "提示", "请输入数字")
            return

        # 是否为空
        if szText == '':
            QMessageBox.information(self, "提示", "请输入跳转页面")
            return

        # 得到页数
        pageIndex = int(szText)
        # 判断是否有指定页
        if pageIndex > self.totalPage or pageIndex < 1:
            QMessageBox.information(self, "提示", "没有指定的页面，请重新输入")
            return

        # 得到查询起始行号
        limitIndex = (pageIndex - 1) * self.PageRecordCount

        # 记录查询
        self.recordQuery(limitIndex);
        # 设置当前页
        self.currentPage = pageIndex
        # 刷新状态
        self.updateStatus();


if __name__ == '__main__':
    app = QApplication(sys.argv)

    # createTableAndInit()
        # 创建窗口
    example = DBdataView()
    # 显示窗口
    example.show()

    sys.exit(app.exec())