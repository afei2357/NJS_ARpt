from PyQt6.QtCore import Qt
from PyQt6.QtSql import  QSqlQueryModel, QSqlQuery
import re
import sys,os
from PyQt6.QtWidgets import *


from PyQt6.QtWidgets import QDialog,QHeaderView,QMessageBox
# from UI.UI_acount_manager import Ui_Form
from UI.UI_acount_manager import Ui_Form as manager_Ui_form
from UI.Ui_create_acount import Ui_Form as add_Ui_Form

from PyQt6.QtWidgets import QFileDialog


import logging.config
import logging
# basedir = os.path.join( os.path.abspath(__file__) ,os.pardir,os.pardir)
# print(basedir)
# config_file = os.path.join(basedir,'config/logging.ini')
# logging.config.fileConfig(config_file)
config_path = './config/logging.ini'
logging.config.fileConfig(config_path)
logger = logging.getLogger('worker')






class Add_User_Form(QDialog,add_Ui_Form):
    def __init__(self,db, parent=None):
        super(Add_User_Form, self).__init__(parent)
        self.setupUi(self)
        self.db = db
        self.query = QSqlQuery(self.db)
        self.btn_add_ok.clicked.connect(self.add_user)
        self.btn_add_cancle.clicked.connect(self.cancle_user)


    def add_user(self):
        logging.info(self.input_password.text())
        if not self.input_username.text() or not self.input_password.text():
            QMessageBox.warning(self,'输入不全','用户名、密码不能为空')
        if self.input_password.text() != self.input_password2.text() :
            QMessageBox.warning(self, '确认密码有问题', '密码、确认密码必须相同')
        logging.info('self.input_password.text()')

        if self.check_password() :
            if self.radio_visitor.isChecked():
                role = 'visitor'
                logging.info(role)
                self.inser_user2db(role)
                logging.info(role)
            else:
                role = 'manager'
                logging.info(role)
                self.inser_user2db(role)
        # QMessageBox.information(self,'完成')
        self.close()

    def inser_user2db(self,role):
        # connect = sqlite3.connect('mydata.db')
        logging.info(role)

        # self.query.exec('command')
        # c = connect.cursor()
        # command = "insert into users(username,password,role) values(null,'%s','%s','%s')" % (self.input_username.text(), self.input_password.text(),role)
        command = "insert into users(username,password,role) values('%s','%s','%s')" % (self.input_username.text(), self.input_password.text(),role)
        logging.info(command)
        ok = self.query.exec(command)
        if not ok :
            logging.info(self.query.lastError().text())
        # connect.commit()
        # connect.close()


    def check_password(self):
        password = self.input_password.text()
        # 检查密码长度和包含数字和字母
        if len(password) < 6 or not (any(char.isdigit() for char in password) and any(char.isalpha() for char in password)):
            QMessageBox.warning(self, '确认密码有问题', '密码不小于6位数，且必须包含数字和字母')
            return False
        else:
            # QMessageBox.information(self, '密码确认成功', '密码符合要求')
            return True


    def cancle_user(self):
        print('cancle add ')
        self.close()

class Manager(QDialog,manager_Ui_form):
    def __init__(self,db, parent=None):
        super(Manager, self).__init__(parent)
        self.setupUi(self)
        logging.info('creat before')
        # logger.info('start Manager')
        # print('aaaaaa')
        self.db = db
        self.query = QSqlQuery(self.db)
        self.create_tb()

        logging.info('start DataViewCelled')

        # self.btnCall.clicked.connect(self.open_diallog)
        # 查询模型
        # self.queryModel = None
        self.queryModel = QSqlQueryModel(self)
        # 当前页
        self.currentPage = 0
        # 总页数
        self.totalPage = 0
        # 总记录数
        self.totalRecrodCount = 0
        # 每页显示记录数
        self.PageRecordCount = 10
        self.db = db
        self.initUI()


        self.btn_add_user.clicked.connect(self.show_add_user)
        self.btn_modify_user.clicked.connect(self.show_modify_user)
        self.btn_delete_user.clicked.connect(self.show_delete_user)

    # 数据库相关
    def initUI(self):
        # 创建窗口
        # self.createWindow()
        # 设置表格
        self.setTableView()
        # # 信号槽连接：上一页、下一页、跳转页
        self.prevButton.clicked.connect(self.onPrevButtonClick)
        self.nextButton.clicked.connect(self.onNextButtonClick)
        self.switchPageButton.clicked.connect(self.onSwitchPageButtonClick)
        # self.btnExportInfo.clicked.connect(self.exportInfo)

        # 设置表格属性
        # 表格宽度的自适应调整
        self.tableView.horizontalHeader().setStretchLastSection(True)
        self.tableView.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)



    def setTableView(self):
        logger.info('*** step2 SetTableView')

        # 声明查询模型
        self.queryModel = QSqlQueryModel(self)
        # self.dataModel = QSqlQueryModel(self)
        self.ceate_table()
        # 设置当前页
        self.currentPage = 1
        # 得到总记录数
        self.totalRecrodCount = self.getTotalRecordCount()
        # 得到总页数
        self.totalPage = self.getPageCount()
        # logger.info('----total page:')

        # 刷新状态
        # self.updateStatus()
        # 设置总页数文本
        self.setTotalPageLabel()
        # 设置总记录数
        self.setTotalRecordLabel()
        # 记录查询
        self.recordQuery(0)
        # 设置模型
        self.tableView.setModel(self.queryModel)

        # logger.info('totalRecrodCount=' + str(self.totalRecrodCount))
        # logger.info('totalPage=' + str(self.totalPage))
        self.updateStatus()

        # 设置表格表头
        self.queryModel.setHeaderData(0, Qt.Orientation.Horizontal, "id")
        self.queryModel.setHeaderData(1, Qt.Orientation.Horizontal, "姓名")
        self.queryModel.setHeaderData(2, Qt.Orientation.Horizontal, "密码")
        self.queryModel.setHeaderData(3, Qt.Orientation.Horizontal, "角色")

    # 先判断表格是否存在，否则创建表格
    def ceate_table(self):
        self.query = QSqlQuery()
        logger.info('create db ')
        # # patient_results 只用于保存输入的详细信息
        # self.query.exec("create table if not exists  patient_results (id integer primary key AUTOINCREMENT ,"
        #                 "sample_code vchar,"
        #                 "results vchar)")
        # users 用于保存输入结果信息和展示给用户看
        self.query.exec("create table if not exists  users(id integer primary key AUTOINCREMENT ,"
                        "username vchar, "
                        "password vchar, "
                        "role vchar)")

    # 得到记录数
    def getTotalRecordCount(self):
        self.queryModel.setQuery("select * from users")

        rowCount = self.queryModel.rowCount()
        # logger.info('rowCount==' + str(rowCount))
        return rowCount

    # 得到页数
    def getPageCount(self):
        # logger.info('self.totalRecrodCount, self.PageRecordCount')
        # logger.info(self.totalRecrodCount, self.PageRecordCount)
        if self.totalRecrodCount % self.PageRecordCount == 0:
            # 地板除
            return (self.totalRecrodCount // self.PageRecordCount)
        else:
            return (self.totalRecrodCount // self.PageRecordCount + 1)

    # 记录查询
    def recordQuery(self, limitIndex):
        szQuery = ("select * from users limit %d,%d" % (limitIndex, self.PageRecordCount))
        # logger.info('query sql=' + szQuery)
        self.queryModel.setQuery(szQuery)

    # 刷新状态
    def updateStatus(self):
        szCurrentText = ("当前第%d页" % self.currentPage)
        self.currentPageLabel.setText(szCurrentText)
        # logger.info('self.currentPage == self.totalPage------------')
        # logger.info(self.currentPage , self.totalPage)
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
        # logger.info('*** setTotalRecordLabel szTotalRecordText=' + szTotalRecordText)
        self.totalRecordLabel.setText(szTotalRecordText)

    # 前一页按钮按下
    def onPrevButtonClick(self):
        # logger.info('*** onPrevButtonClick ');
        limitIndex = (self.currentPage - 2) * self.PageRecordCount
        self.recordQuery(limitIndex)
        self.currentPage -= 1
        self.updateStatus()

    # 后一页按钮按下
    def onNextButtonClick(self):
        # logger.info('*** onNextButtonClick ')
        limitIndex = self.currentPage * self.PageRecordCount
        self.recordQuery(limitIndex)
        self.currentPage += 1
        self.updateStatus()
        # logger.info('next click ----------')

    # 转到页按钮按下
    def onSwitchPageButtonClick(self):
        # 得到输入字符串
        szText = self.switchPageLineEdit.text()
        # logger.info('szText')
        # logger.info(szText)
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



    def show_add_user(self):
        form_add = Add_User_Form(self.db)
        form_add.exec()
        logging.info('exec before')


    def show_modify_user(self):
        pass

    def show_delete_user(self):
        pass
    def create_tb(self):
        create_tb_shell = ' create table if not exists  users(id integer primary key AUTOINCREMENT ,  "username" vchar,"password" vchar,"role" vchar);'
        logging.info('berore before')
        self.query.exec(create_tb_shell)
        logging.info('create')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    myWin = Manager()
    myWin.show()
    sys.exit(app.exec())
