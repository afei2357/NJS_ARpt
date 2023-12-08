import sys,os,re
import time

# from PyQt5.QtWidgets import QApplication, QMainWindow
from Ui_MainWindow import Ui_MainWindow
# from PyQt6.QtCore import *
# # from PyQt6.QtGui import *
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import *
from worker import WorkerThread
# from DBdataView import DBdataView
from PyQt6.QtSql import QSqlDatabase, QSqlQueryModel, QSqlQuery

from time import sleep


# class ARptWindow(QMainWindow, Ui_MainWindow,DBdataView):
class ARptWindow( QMainWindow,Ui_MainWindow):
# class ARptWindow(QMainWindow,DBdataView):
    def __init__(self, parent=None):
        super(ARptWindow, self).__init__(parent)
        self.setupUi(self)
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

        self.btnOpenInfo.clicked.connect(lambda : self.getfiles('A'))
        self.btnOpenValue.clicked.connect(lambda : self.getfiles('B'))
        self.btnReport.clicked.connect(self.open_folder)
        self.btnGenerateReport.clicked.connect(self.generate_report)

        self.lbl_report_status.setVisible(False)
        self.label_info.setVisible(False)
        self.label_value.setVisible(False)
        self.info_file=''
        self.value_file=''
        workdir = os.path.abspath(os.path.dirname(__file__))
        self.reports_result = os.path.join(workdir,'reports_result')
        print('self.reports_result ')
        print(self.reports_result )
        if not os.path.exists(self.reports_result):
            os.makedirs(self.reports_result)

        if self.info_file and self.value_file:
            self.btnGenerateReport.setEnabled(True)
        else:
            self.btnGenerateReport.setEnabled(False)
        # self.init_dataview()
        self.initUI()
        self.btnTestReport.clicked.connect(self.test_generate_report_table)
        self.btnShowPatientInfo.clicked.connect(self.show_patient_info)

    def show_patient_info(self):
        self.finished_state()
        print('show_patient_info ')
        # pass

    def getfiles(self,value='A'):
        # dlg = QFileDialog()
        # dlg.setFileMode(QFileDialog.AnyFile)
        # dlg.setFilter(QDir.Files)
        #
        # options = QFileDialog.Options()
        # options |= QFileDialog.DontUseNativeDialog
        # options |= QFileDialog.DontUseCustomDirectoryIcons
        # files, _ = QFileDialog.getOpenFileNames(self, "选取多个文件", ".",
                                                # "All Files (*);;Text Files (*.txt)")
        # files, _ = QFileDialog.getOpenFileNames(self, caption="选取多个文件", directory=".",
        #                                         filter="All Files (*);;Text Files (*.txt)")
        # files, _ = QFileDialog.getOpenFileName(self, caption='选择多个文件', directory=os.path.abspath('.'),
        #                                                  filter="All files(*);;Python files(*.py);;Image files (*.jpg *.png);;Image files2(*.ico *.gif)")
        file, _ = QFileDialog.getOpenFileName(self, caption='选择多个文件', directory=os.path.abspath('.'),
                                                         filter="Excel  (*.xlsx *.xls)")
        if not file:
            return
        if value=='A':
            self.info_file = file
        else :
            self.value_file = file

        self.label_info.setText(os.path.basename(self.info_file))
        self.label_value.setText(os.path.basename(self.value_file))
        self.label_info.setVisible(True)
        self.label_value.setVisible(True)
        print(self.info_file and self.value_file)
        print('self.info_file and self.value_file')
        print(self.info_file , self.value_file)

        if self.info_file and self.value_file:
            self.btnGenerateReport.setEnabled(True)

    def generate_report(self):
        self.thread = WorkerThread(self.info_file, self.value_file, self.reports_result,self.db)
        self.thread.started.connect(self.runing_state)
        self.thread.finished.connect(self.finished_state)
        self.thread.start()
        print('generate_reporting ccc')

    def runing_state(self):
        self.btnGenerateReport.setEnabled(False)
        # self.btnOpenFile.setEnabled(False)
        print('in state')
        self.lbl_report_status.setVisible(True)
        self.lbl_report_status.setText("<font color=red size=2><b>报告正在生成，请稍后...</b></font>")
    def test_generate_report_table(self):
        self.info_file = 'D:/project/PycharmProjects/pyqt5/NJS_ARpt_project/input/表A.xlsx'
        self.value_file = 'D:/project/PycharmProjects/pyqt5/NJS_ARpt_project/input/尿结石表B：数据集.xlsx'
        self.reports_result = 'D:/project/PycharmProjects/pyqt5/NJS_ARpt_project/reports_result'
        self.generate_report()
        # pass
    def finished_state(self):
        self.btnGenerateReport.setEnabled(True)
        self.lbl_report_status.setText("<font color=green size=2><b>报告已完成!</b></font>")
        # self.btnOpenFile.setEnabled(True)
        self.updateStatus()
        print('after time3')

        self.tableView.reset()


    def open_folder(self):
        print('open1')
        path = os.path.abspath(self.reports_result)
        print('path')
        print(path)
        if os.path.exists(path):
            os.startfile(path)
        else:
            QMessageBox.information(self, '错误', '路径不存在，请检查', QMessageBox.Yes)
        print('open2')

    def show_message(self):
        reply = QMessageBox.information(self, '错误', '必须为xlsx或者json结尾的文件', QMessageBox.Yes | QMessageBox.No)
        print(reply)


    # 数据库相关
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
        self.dataModel = QSqlQueryModel(self)
    #     self.reset_table_view()
    # def reset_table_view(self):
        self.ceate_table()
        # 设置当前页
        self.currentPage = 1
        # 得到总记录数
        self.totalRecrodCount = self.getTotalRecordCount()
        # 得到总页数
        self.totalPage = self.getPageCount()
        # print('----total page:')

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
        print('rowCount==' + str(rowCount))
        return rowCount

    # 得到页数
    def getPageCount(self):
        print('self.totalRecrodCount, self.PageRecordCount')
        print(self.totalRecrodCount, self.PageRecordCount)
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
        print('self.currentPage ,self.totalPage，self.totalRecrodCount')
        print(self.currentPage ,self.totalPage,self.totalRecrodCount)
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
        print('*** onNextButtonClick ')
        limitIndex = self.currentPage * self.PageRecordCount
        self.recordQuery(limitIndex)
        self.currentPage += 1
        self.updateStatus()
        print('next click ----------')

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
    myWin = ARptWindow()
    myWin.show()
    sys.exit(app.exec())
