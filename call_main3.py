import sys,os
import time

# from PyQt5.QtWidgets import QApplication, QMainWindow
from Ui_MainWindow import Ui_MainWindow
# from PyQt6.QtCore import *
# # from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from worker import WorkerThread
from DBdataView import DBdataView

from time import sleep


# class ARptWindow(QMainWindow, Ui_MainWindow,DBdataView):
class ARptWindow( DBdataView):
# class ARptWindow(QMainWindow,DBdataView):
    def __init__(self, parent=None):
        super(ARptWindow, self).__init__(parent)
        self.setupUi(self)
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




    def getfiles(self,value='A'):
        # dlg = QFileDialog()
        # dlg.setFileMode(QFileDialog.AnyFile)
        # dlg.setFilter(QDir.Files)
        #
        # options = QFileDialog.Options()
        # options |= QFileDialog.DontUseNativeDialog
        # options |= QFileDialog.DontUseCustomDirectoryIcons

    # def test(self):
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
        print('test--------')
        # self.label_2.setText('所输入文件：')
        # self.label_info.setVisible(True)
        # self.label_3.setText("信息表： "+os.path.basename(self.info_file)+' \n检测结果表： '+os.path.basename(self.value_file))
        self.label_info.setText(os.path.basename(self.info_file))
        self.label_value.setText(os.path.basename(self.value_file))
        self.label_info.setVisible(True)
        self.label_value.setVisible(True)
        print(self.info_file and self.value_file)
        print('self.info_file and self.value_file')
        print(self.info_file , self.value_file)

        if self.info_file and self.value_file:
            self.btnGenerateReport.setEnabled(True)
        # else:
        #     self.btnGenerateReport.setVisible(False)
        # for file in files:
        #     if not (file.endswith('xlsx') or file.endswith('json')):
        #         print('必须json或者xls文件')
        #         self.show_message()
        #         return
        #     if file.endswith('xlsx'):
        #         self.xlxs_file = file
        #     if file.endswith('json'):
        #         self.js_file = file

    def generate_report(self):
        self.thread = WorkerThread(self.info_file, self.value_file, self.reports_result)
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

    def finished_state(self):
        self.btnGenerateReport.setEnabled(True)

        self.lbl_report_status.setText("<font color=green size=2><b>报告已完成!</b></font>")
        # self.btnOpenFile.setEnabled(True)
        print('after time3')

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


if __name__ == '__main__':
    app = QApplication(sys.argv)
    myWin = ARptWindow()
    myWin.show()
    sys.exit(app.exec())
