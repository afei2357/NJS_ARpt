import sys,os
import time
if not os.path.exists('./logs/'):
    os.makedirs('./logs/')

from Ui_MainWindow import Ui_MainWindow

from PyQt6.QtWidgets import *
from PyQt6.QtSql import QSqlDatabase
from DataViewCelled import DataViewCelled
import logging.config
from worker import WorkerThread

config_path = './config/logging.ini'
logging.config.fileConfig(config_path)
if not os.path.exists(config_path):
    QMessageBox.warning('文件错误', '配置文件不存在，请检查,本软件自动退出')
    # return

main_logger = logging.getLogger('main')
main_logger.info('start ui ')

class ARptWindow( QMainWindow,Ui_MainWindow):
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
        self.btnSavetReport.clicked.connect(self.getdir)
        self.btnReport.clicked.connect(self.open_folder)
        self.btnGenerateReport.clicked.connect(self.generate_report)

        self.lbl_report_status.setVisible(False)
        self.label_info.setVisible(False)
        self.label_value.setVisible(False)
        self.info_file=''
        self.value_file=''
        self.reports_result=''

        self.db = QSqlDatabase.addDatabase('QSQLITE')
        if not os.path.exists('./db'):
            os.makedirs('./db')

        # 设置数据库名称
        self.db.setDatabaseName('./db/database.db')
        # 打开数据库
        self.db.open()
        self.table_dialog = DataViewCelled(self.db)

        self.lbl_finish.setWordWrap(True)

        workdir = os.path.abspath(os.path.dirname(__file__))
        if not self.reports_result:
            self.reports_result = os.path.join(workdir,'reports_result')

        if not os.path.exists(self.reports_result):
            os.makedirs(self.reports_result)

        if self.info_file and self.value_file:
            self.btnGenerateReport.setEnabled(True)
        else:
            self.btnGenerateReport.setEnabled(False)
        # btnTestReport 按钮仅用于方便测试，软件发布之后将其设置为不可见。
        self.btnTestReport.setVisible(False)
        self.btnTestReport.clicked.connect(self.test_generate_report_table)
        self.btnShowPatientInfo.clicked.connect(self.show_patient_info)
    def show_patient_info(self):
        self.table_dialog.exec()
    # 获取保存结果文件的目录路径
    def getdir(self):
        self.reports_result = QFileDialog.getExistingDirectory(self, caption='选择保存的文件夹', directory=os.path.abspath('.'))


    # 打开A表B表
    def getfiles(self,value='A'):
        file, _ = QFileDialog.getOpenFileName(self, caption='选择单个excel文件', directory=os.path.abspath('.'),
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
        main_logger.info(self.info_file )
        main_logger.info(self.value_file)

        if self.info_file and self.value_file:
            self.btnGenerateReport.setEnabled(True)

    def generate_report(self):
        self.thread = WorkerThread(self.info_file, self.value_file, self.reports_result,self.db)
        self.thread.started.connect(self.runing_state)
        self.thread.finished.connect(self.finished_state)
        self.lbl_finish.setText('准备生成报告，请稍后。。。')
        self.thread.signal.connect(self.finished_single_report_state)
        self.thread.signal.connect(self.table_dialog.setTableView )
        self.thread.info_signal.connect(self.thread_info_func)
        self.thread.start()
        main_logger.info(' self.thread.start' )

        # main_logger.info('generate_reporting ccc')

    def runing_state(self):
        self.btnGenerateReport.setEnabled(False)
        # self.btnOpenFile.setEnabled(False)
        # main_logger.info('in state')
        self.lbl_report_status.setVisible(True)
        self.lbl_report_status.setText("<font color=red size=2><b>报告正在生成，请稍后...</b></font>")
    # 如下函数仅用于方便测试
    def test_generate_report_table(self):
        self.info_file = 'D:/project/PycharmProjects/pyqt5/NJS_ARpt_project/input/表A.xlsx'
        self.value_file = 'D:/project/PycharmProjects/pyqt5/NJS_ARpt_project/input/尿结石表B：数据集.xlsx'
        self.reports_result = 'D:/project/PycharmProjects/pyqt5/NJS_ARpt_project/reports_result'
        self.generate_report()

    # 全部状态完成后提示
    def finished_state(self):
        self.btnGenerateReport.setEnabled(True)
        self.lbl_report_status.setText("<font color=green size=2><b>报告任务已结束!</b></font>")
        # QMessageBox.information(self,'任务信息','报告任务已经结束，请查看结果')
    # 单份报告的状态改变：
    def finished_single_report_state(self,content):
        self.lbl_finish.setText(content)
        # 自动调整label大小
        self.lbl_finish.adjustSize()

    # 在子线程出错时候，弹出提示信息
    def thread_info_func(self,content):
        QMessageBox.question(self,'错误', content)

    # 打开报告所在目录
    def open_folder(self):
        # main_logger.info('open1')
        path = os.path.abspath(self.reports_result)
        main_logger.info(path)

        if os.path.exists(path):
            os.startfile(path)
        else:
            main_logger.info(path)
            QMessageBox.warning(self,'路径错误','路径不存在，请检查')
        return
        # main_logger.info('open2')

    def show_message(self):
        reply = QMessageBox.information(self, '错误', '必须为xlsx或者json结尾的文件')
        # main_logger.info(reply)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    myWin = ARptWindow()
    myWin.show()
    sys.exit(app.exec())
