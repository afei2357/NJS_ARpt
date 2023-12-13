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
# from Ui_ARpt_MainWindow import Ui_MainWindow
from test_data_view import mainCelled

from time import sleep


# class ARptWindow(QMainWindow, Ui_MainWindow,DBdataView):
class ARptWindow( QMainWindow,Ui_MainWindow):
# class ARptWindow(QMainWindow,DBdataView):
    def __init__(self, parent=None):
        super(ARptWindow, self).__init__(parent)
        self.setupUi(self)
        # self.setWindowIcon(QIcon)
        # self.verticalLayout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        # self.container = QWidget()
        # self.container.setLayout(self.verticalLayout)
        # self.setCentralWidget(self.container)
        # self.centralwidget.setLayout(self.verticalLayout)
        self.btnOpenInfo.clicked.connect(lambda : self.getfiles('A'))
        self.btnOpenValue.clicked.connect(lambda : self.getfiles('B'))
        self.btnReport.clicked.connect(self.open_folder)
        self.btnGenerateReport.clicked.connect(self.generate_report)

        self.lbl_report_status.setVisible(False)
        self.label_info.setVisible(False)
        self.label_value.setVisible(False)
        self.info_file=''
        self.value_file=''

        self.db = QSqlDatabase.addDatabase('QSQLITE')
        if not os.path.exists('./db'):
            os.makedirs('./db')
        # 设置数据库名称
        self.db.setDatabaseName('./db/database.db')
        # 打开数据库
        self.db.open()
        self.table_dialog = mainCelled(self.db)

        self.lbl_finish.setWordWrap(True)

        workdir = os.path.abspath(os.path.dirname(__file__))
        self.reports_result = os.path.join(workdir,'reports_result')

        if not os.path.exists(self.reports_result):
            os.makedirs(self.reports_result)

        if self.info_file and self.value_file:
            self.btnGenerateReport.setEnabled(True)
        else:
            self.btnGenerateReport.setEnabled(False)

        self.btnTestReport.clicked.connect(self.test_generate_report_table)
        self.btnShowPatientInfo.clicked.connect(self.show_patient_info)
    def show_patient_info(self):
        self.table_dialog.exec()

    def getfiles(self,value='A'):
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
        # print(self.info_file and self.value_file)
        # print('self.info_file and self.value_file')
        # print(self.info_file , self.value_file)

        if self.info_file and self.value_file:
            self.btnGenerateReport.setEnabled(True)

    def generate_report(self):
        self.thread = WorkerThread(self.info_file, self.value_file, self.reports_result,self.db)
        self.thread.started.connect(self.runing_state)
        self.thread.finished.connect(self.finished_state)
        self.lbl_finish.setText('准备生成报告，请稍后。。。')
        self.thread.signal.connect(self.finished_single_report_state)
        self.thread.signal.connect(self.table_dialog.setTableView )
        self.thread.start()
        # print('generate_reporting ccc')

    def runing_state(self):
        self.btnGenerateReport.setEnabled(False)
        # self.btnOpenFile.setEnabled(False)
        # print('in state')
        self.lbl_report_status.setVisible(True)
        self.lbl_report_status.setText("<font color=red size=2><b>报告正在生成，请稍后...</b></font>")
    def test_generate_report_table(self):
        self.info_file = 'D:/project/PycharmProjects/pyqt5/NJS_ARpt_project/input/表A.xlsx'
        self.value_file = 'D:/project/PycharmProjects/pyqt5/NJS_ARpt_project/input/尿结石表B：数据集.xlsx'
        self.reports_result = 'D:/project/PycharmProjects/pyqt5/NJS_ARpt_project/reports_result'
        self.generate_report()

    # 全部状态完成后提示
    def finished_state(self):
        self.btnGenerateReport.setEnabled(True)
        self.lbl_report_status.setText("<font color=green size=2><b>报告已全部完成!</b></font>")

    # 单份报告的状态改变：
    def finished_single_report_state(self,content):
        self.lbl_finish.setText(content)
        # 自动调整label大小
        self.lbl_finish.adjustSize()

        # self.btnOpenFile.setEnabled(True)
        # self.updateStatus()
        # print('after time3')
        # self.tableView.reset()
    # 打开报告所在目录
    def open_folder(self):
        # print('open1')
        path = os.path.abspath(self.reports_result)
        # print('path')
        # print(path)
        if os.path.exists(path):
            os.startfile(path)
        else:
            QMessageBox.information(self, '错误', '路径不存在，请检查', QMessageBox.Yes)
        # print('open2')

    def show_message(self):
        reply = QMessageBox.information(self, '错误', '必须为xlsx或者json结尾的文件', QMessageBox.Yes | QMessageBox.No)
        # print(reply)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    myWin = ARptWindow()
    myWin.show()
    sys.exit(app.exec())
