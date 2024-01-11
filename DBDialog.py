from PyQt6.QtWidgets import *
import re
from PyQt6.QtWidgets import (QTableView , QHeaderView , QMessageBox)
from PyQt6.QtCore import Qt
from PyQt6.QtSql import QSqlDatabase, QSqlQueryModel, QSqlQuery
from NJS_ARpt_project.UI import Ui_DataView


class testDialog(QDialog, Ui_DataView):
    def __init__(self):
        super().__init__(parent=None)
        self.setWindowsTitle('显示数据库')
        # self.table  = QTableView()



class DatabaseDialog(QDialog, Ui_DataView):
# class ARptWindow(QMainWindow,DBdataView):
    def __init__(self, parent=None):
        super(DatabaseDialog, self).__init__(parent)
        # self.setupUi(self)
        # 查询模型
        self.queryModel = None
        # 当前页
        self.currentPage = 0
        # 总页数
        self.totalPage = 0
        # 总记录数
        self.totalRecrodCount = 0
        # 每页显示记录数
        self.PageRecordCount = 20
        self.db = None
        # self.initUI()
        print('dialog')

    # 数据库相关
    def initUI(self):
        # 创建窗口
        # self.createWindow()


        print('initUI')
        # # # 信号槽连接
        # self.prevButton.clicked.connect(self.onPrevButtonClick)
        # self.nextButton.clicked.connect(self.onNextButtonClick)
        # self.switchPageButton.clicked.connect(self.onSwitchPageButtonClick)


        # 设置表格属性
        self.tableView = QTableView()
        # 设置表格
        # self.setTableView()
        # # 表格宽度的自适应调整
        self.tableView.horizontalHeader().setStretchLastSection(True)
        self.tableView.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)

    def setTableView(self):
        # print('*** step2 SetTableView')
        self.db = QSqlDatabase.addDatabase('QSQLITE')
        # 设置数据库名称
        self.db.setDatabaseName('./db/database.db')
        # 打开数据库
        self.db.open()
        # 声明查询模型
        self.queryModel = QSqlQueryModel(self)
        self.dataModel = QSqlQueryModel(self)
    #     self.reset_table_view()
        self.ceate_table()
        # 设置当前页
        self.currentPage = 1


        # 得到总记录数
        self.totalRecrodCount = self.getTotalRecordCount()
        # 得到总页数
        self.totalPage = self.getPageCount()
        # print('----total page:')

        # 刷新状态


        # self.updateStatus()
        # 设置总页数文本
        # self.setTotalPageLabel()

        # 设置总记录数
        # self.setTotalRecordLabel()


        # 记录查询
        self.recordQuery(0)
        # 设置模型
        self.tableView.setModel(self.queryModel)

        # print('totalRecrodCount=' + str(self.totalRecrodCount))

        # print('totalPage=' + str(self.totalPage))
        # self.updateStatus()


        # 设置表格表头
        self.queryModel.setHeaderData(0, Qt.Orientation.Horizontal, "id")
        self.queryModel.setHeaderData(1, Qt.Orientation.Horizontal, "编号")
        self.queryModel.setHeaderData(2, Qt.Orientation.Horizontal, "姓名")
        self.queryModel.setHeaderData(3, Qt.Orientation.Horizontal, "性别")
        self.queryModel.setHeaderData(4, Qt.Orientation.Horizontal, "年龄")
        self.queryModel.setHeaderData(5, Qt.Orientation.Horizontal, "采样日期")
        self.queryModel.setHeaderData(6, Qt.Orientation.Horizontal, "风险区间")
        self.queryModel.setHeaderData(7, Qt.Orientation.Horizontal, "风险值")

    def ceate_table(self):
        self.query = QSqlQuery()
        self.query.exec("create table if not exists  patient_info(id integer primary key AUTOINCREMENT ,"
                        " sample_code vchar,"
                        "name vchar, "
                        "gender_desc vchar, "
                        "birthday vchar, "
                        "sampling_time vchar,"
                        "risk vchar,"
                        "predict_pls vchar)")

    # 得到记录数
    def getTotalRecordCount(self):
        self.queryModel.setQuery("select * from patient_info")

        rowCount = self.queryModel.rowCount()
        # print('rowCount==' + str(rowCount))
        return rowCount

    # 得到页数
    def getPageCount(self):
        # print('self.totalRecrodCount, self.PageRecordCount')
        # print(self.totalRecrodCount, self.PageRecordCount)
        if self.totalRecrodCount % self.PageRecordCount == 0:
            # 地板除
            return (self.totalRecrodCount // self.PageRecordCount)
        else:
            return (self.totalRecrodCount // self.PageRecordCount + 1)

    # 记录查询
    def recordQuery(self, limitIndex):
        szQuery = ("select * from patient_info limit %d,%d" % (limitIndex, self.PageRecordCount))
        # print('query sql=' + szQuery)
        self.queryModel.setQuery(szQuery)

    # 刷新状态
    def updateStatus(self):
        szCurrentText = ("当前第%d页" % self.currentPage)
        self.currentPageLabel.setText(szCurrentText)
        # print('self.currentPage == self.totalPage------------')
        # print(self.currentPage , self.totalPage)
        # 设置按钮是否可用
        if self.currentPage <= 1:
            self.prevButton.setEnabled(False)
        else:
            self.prevButton.setEnabled(True)
        if self.currentPage >= self.totalPage:
            self.nextButton.setEnabled(False)
        else:
            self.nextButton.setEnabled(True)

    # 设置总数页文本
    def setTotalPageLabel(self):
        szPageCountText = ("总共%d页" % self.totalPage)
        self.totalPageLabel.setText(szPageCountText)

    # 设置总记录数
    def setTotalRecordLabel(self):
        szTotalRecordText = ("共%d条" % self.totalRecrodCount)
        # print('*** setTotalRecordLabel szTotalRecordText=' + szTotalRecordText)
        self.totalRecordLabel.setText(szTotalRecordText)

    # 前一页按钮按下
    def onPrevButtonClick(self):
        # print('*** onPrevButtonClick ');
        limitIndex = (self.currentPage - 2) * self.PageRecordCount
        self.recordQuery(limitIndex)
        self.currentPage -= 1
        self.updateStatus()

    # 后一页按钮按下
    def onNextButtonClick(self):
        # print('*** onNextButtonClick ')
        limitIndex = self.currentPage * self.PageRecordCount
        self.recordQuery(limitIndex)
        self.currentPage += 1
        self.updateStatus()
        # print('next click ----------')

    # 转到页按钮按下
    def onSwitchPageButtonClick(self):
        # 得到输入字符串
        szText = self.switchPageLineEdit.text()
        # print('szText')
        # print(szText)
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
