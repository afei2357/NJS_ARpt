import os,sys
if not os.path.exists('./logs/'):
    os.makedirs('./logs/')

from UI.Ui_login import Ui_Form

# 账号 管理员-录入者-查询者
from PyQt6.QtWidgets import *
import logging.config

config_path = './config/logging.ini'
logging.config.fileConfig(config_path)

from call_main6 import ARptWindow


class Login( QMainWindow,Ui_Form):
    def __init__(self, stacked_widget,parent=None):
        super(Login, self).__init__(parent)
        # 保存主界面的StackedWidget
        self.stacked_widget = stacked_widget

        self.setupUi(self)
        self.setGeometry(100, 100, 400, 300)

        self.btnLogin.clicked.connect(self.login_data)
        self.btnCancle.clicked.connect(self.cancle_login)

        # self.lbl_report_status.setVisible(False)
        # self.label_info.setVisible(False)
        # # self.label_value.setVisible(False)
        # self.info_file=''
        # self.value_file=''
        # self.reports_result=''
        #
        # self.db = QSqlDatabase.addDatabase('QSQLITE')
        # if not os.path.exists('./db'):
        #     os.makedirs('./db')

        # 设置数据库名称
        # self.db.setDatabaseName('./db/database.db')
        # # 打开数据库
        # self.db.open()
        # self.table_dialog = DataViewCelled(self.db)
        #
        # self.lbl_finish.setWordWrap(True)
        #
        # workdir = os.path.abspath(os.path.dirname(__file__))
        # if not self.reports_result:
        #     self.reports_result = os.path.join(workdir,'reports_result')
        #
        # if not os.path.exists(self.reports_result):
        #     os.makedirs(self.reports_result)
        #
        # if self.info_file and self.value_file:
        #     self.btnGenerateReport.setEnabled(True)
        # else:
        #     self.btnGenerateReport.setEnabled(False)
        # # btnTestReport 按钮仅用于方便测试，软件发布之后将其设置为不可见。
        # self.btnTestReport.setVisible(False)
        # self.btnTestReport.clicked.connect(self.test_generate_report_table)
        # self.btnShowPatientInfo.clicked.connect(self.show_patient_info)
    def login_data(self):
        # self.table_dialog.exec()
        # 这里可以添加实际的验证逻辑，例如从数据库中验证用户名和密码
        # 简单示例：如果用户名是'admin'且密码是'password'，则登录成功
        if self.name.text() == 'a' and self.password.text() == 'a':
            # QMessageBox.information(self, '登录成功', '欢迎进入主界面！')
            # 在这里切换到主界面并关闭登录窗口
            self.stacked_widget.setCurrentIndex(1)  # 切换到主界面
            self.stacked_widget.setFixedSize(745, 800)
            self.close()  # 关闭登录窗口
        else:
            QMessageBox.warning(self, '登录失败', '用户名或密码错误，请重试。')

    # 获取保存结果文件的目录路径
    def cancle_login(self):
        # self.reports_result = QFileDialog.getExistingDirectory(self, caption='选择保存的文件夹', directory=os.path.abspath('.'))
        # reply = QMessageBox.information(self, '错误', '必须为xlsx或者json结尾的文件')
        QApplication.quit()

    def show_message(self):
        reply = QMessageBox.information(self, '错误', '必须为xlsx或者json结尾的文件')
        # main_logger.info(reply)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    # 创建一个 QStackedWidget 用于管理不同的界面
    stacked_widget = QStackedWidget()
    # 添加登录窗口和主界面到 stacked_widget
    login_window = Login(stacked_widget)
    main_window = ARptWindow()
    stacked_widget.addWidget(login_window)
    stacked_widget.addWidget(main_window)

    stacked_widget.show()




    # myWin = Login()

    # myWin.show()
    sys.exit(app.exec())
