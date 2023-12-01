import sys,os
import time

# from PyQt5.QtWidgets import QApplication, QMainWindow
from Ui_MainWindow import Ui_MainWindow
from PyQt6.QtCore import *
# from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from worker import WorkerThread

from time import sleep


class ARptWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(ARptWindow, self).__init__(parent)
        self.setupUi(self)
        self.btnOpenFile.clicked.connect(self.getfiles)
        self.btnReport.clicked.connect(self.open_folder)
        self.label.setVisible(False)
        self.label_2.setVisible(False)
        self.label_3.setVisible(False)
        self.reports_result = './reports_result'
        if not os.path.exists(self.reports_result):
            os.makedirs(self.reports_result)

    def getfiles(self):
        # dlg = QFileDialog()
        # dlg.setFileMode(QFileDialog.AnyFile)
        # dlg.setFilter(QDir.Files)
        #
        # options = QFileDialog.Options()
        # options |= QFileDialog.DontUseNativeDialog
        # options |= QFileDialog.DontUseCustomDirectoryIcons

        # files, _ = QFileDialog.getOpenFileNames(self, "选取多个文件", ".",
        #                                         "All Files (*);;Text Files (*.txt)", options=options)
        files, _ = QFileDialog.getOpenFileNames(self, caption='选择多个文件', directory=os.path.abspath('.'),
                                                filter="All files(*);;Python files(*.py);;Image files (*.jpg *.png);;Image files2(*.ico *.gif)")

        for file in files:
            if not (file.endswith('xlsx') or file.endswith('json')):
                print('必须json或者xls文件')
                self.show_message()
                return
            if file.endswith('xlsx'):
                self.xlxs_file = file
            if file.endswith('json'):
                self.js_file = file
        # 开启新线程执行报告：
        self.thread = WorkerThread(self.xlxs_file,self.js_file,self.reports_result)
        self.thread.started.connect(self.runing_state)
        self.thread.finished.connect(self.finished_state)
        self.thread.start()
        # self.label.setText('报告正在生成，请稍后...')



        # time.sleep(2)
        # msgBox = QMessageBox()
        # # msgBox.information(self,'请稍等','正在生成报告，请等待',QMessageBox.Yes)
        # msgBox.setText('请稍等-------')
        # msgBox.setStandardButtons(QMessageBox.Ok)
        # msgBox.setDefaultButton(QMessageBox.Ok)
        # timer = QTimer()
        # timer.setSingleShot(True)
        # timer.timeout.connect(msgBox.close)
        # timer.start(500)
        # msgBox.exec_()

        # run_rpt(self.xlxs_file,self.js_file,self.reports_result)
        # sleep(2)


    def runing_state(self):
        # self.btnReport.setEnabled(False)
        self.btnOpenFile.setEnabled(False)
        print('in state')
    # def test(self):
        self.label.setText("<font color=red size=2><b>报告正在生成，请稍后...</b></font>")
        self.label_2.setText('所输入文件：')
        self.label.setVisible(True)
        self.label_3.setText(os.path.basename(self.xlxs_file)+' | '+os.path.basename(self.js_file))
        self.label_2.setVisible(True)
        self.label_3.setVisible(True)

    def finished_state(self):
        self.label.setText("<font color=green size=2><b>报告已完成!</b></font>")
        self.btnOpenFile.setEnabled(True)
        # self.btnReport.setEnabled(True)
        # QMessageBox.information(self, '请稍等', '报告已完成', QMessageBox.Yes)
        print('after time3')




    def open_folder(self):
        print('open1')
        path = os.path.abspath(self.reports_result)
        print(path)
        if os.path.exists(path):
            os.startfile(path)
        else:
            QMessageBox.information(self, '错误', '路径不存在，请检查', QMessageBox.Yes)
        print('open2')

    def generate_report(self):
        # run_rpt(self.xlxs_file,self.js_file,self.reports_result)
        print('ccc')

    def show_message(self):
        reply = QMessageBox.information(self, '错误', '必须为xlsx或者json结尾的文件', QMessageBox.Yes | QMessageBox.No)
        print(reply)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    myWin = ARptWindow()
    myWin.show()
    sys.exit(app.exec())
