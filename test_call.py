import sys,os,re
from PyQt6.QtWidgets import *
from Ui_test_call import Ui_MainWindow
# from Ui_be_called import Ui_Form
from test_data_view import mainCelled

# class ARptWindow(QMainWindow, Ui_MainWindow,DBdataView):
class mainWindow( QMainWindow,Ui_MainWindow):
    def __init__(self, parent=None):
        super(mainWindow, self).__init__(parent)
        self.setupUi(self)
        self.btnCall.clicked.connect(self.open_diallog)

    def open_diallog(self):
        dialog = mainCelled()
        dialog.exec()



if __name__ == '__main__':
    app = QApplication(sys.argv)
    myWin = mainWindow()
    myWin.show()
    sys.exit(app.exec())

