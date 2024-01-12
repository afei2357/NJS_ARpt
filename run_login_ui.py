import sys,os

if not os.path.exists('./logs/'):
    os.makedirs('./logs/')

from UI.Ui_MainWindow import Ui_MainWindow
from PyQt6.QtSql import  QSqlQueryModel, QSqlQuery,QSqlTableModel,QSqlRecord
from PyQt6.QtWidgets import *
from PyQt6.QtSql import QSqlDatabase
from DataViewCelled import DataViewCelled
import logging.config

from PyQt6 import QtCore, QtGui, QtWidgets
if not os.path.exists('./logs/'):
    os.makedirs('./logs/')

from UI.Ui_login import Ui_Form
from user.user_model import User


config_path = './config/logging.ini'
logging.config.fileConfig(config_path)
if not os.path.exists(config_path):
    QMessageBox.warning('文件错误', '配置文件不存在，请检查,本软件自动退出')
    # return

main_logger = logging.getLogger('main')
main_logger.info('start ui ')


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


        self.db = QSqlDatabase.addDatabase('QSQLITE')
        if not os.path.exists('./db'):
            os.makedirs('./db')

        # 设置数据库名称
        self.db.setDatabaseName('./db/database.db')
        # 打开数据库
        self.db.open()
        self.table_dialog = DataViewCelled(self.db)
        self.query = QSqlQuery(self.db)
        self.create_tb()

    def create_tb(self):
        create_tb_shell = ' create table if not exists  users(id integer primary key AUTOINCREMENT ,  "username" vchar,"password_hash" vchar,"role" vchar);'
        logging.info('berore before')
        self.query.exec(create_tb_shell)
        logging.info('create tb ')
        #

    def login_data(self):
        # self.table_dialog.exec()
        username = self.name.text()
        password = self.password.text()

        user = User(self.db)
        content = user.check_login(username,password)
        if content :
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
    stacked_widget.setWindowTitle( "泌尿系结石代谢评估及风险预测软件")
    stacked_widget.addWidget(main_window)
    # stacked_widget.setWindowTitle(0, "泌尿结石登录页面2")
    icon = QtGui.QIcon()
    icon.addPixmap(QtGui.QPixmap("images/logo.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
    stacked_widget.setWindowIcon(icon)

    stacked_widget.show()




    # myWin = Login()

    # myWin.show()
    sys.exit(app.exec())
