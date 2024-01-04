from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *
from PyQt6.QtSql import QSqlDatabase, QSqlTableModel
import sys
import os

class QTableViewDemo(QMainWindow):

    def __init__(self, parent=None):
        super(QTableViewDemo, self).__init__(parent)
        self.setWindowTitle("QSqlTableModel案例")
        self.resize(500, 600)
        self.createTable()
        # self.createWindow()
        # self.onUpdate()
    def createTable(self):
        labelSort = QLabel('排序：')
        self.comboBoxSort= QComboBox()
        lst = ['a','b','c','d']
        self.comboBoxSort.addItems(lst)
        # self.comboBoxSort.addItems('bbb')
        # self.comboBoxSort.addItems('ccc')
        # self.comboBoxSort.addItems('ddd')
        # self.comboBoxSort.setCurrentText('fff')
        layoutSort = QHBoxLayout()
        layoutSort.addWidget(labelSort)
        layoutSort.addWidget(self.comboBoxSort)


        layoutOne = QHBoxLayout(self)
        layoutOne.addLayout(layoutSort)
        btn = QPushButton('test')
        layoutOne.addWidget(btn)

        # layout = QVBoxLayout(self)
        widget = QWidget()
        self.setCentralWidget(widget)
        widget.setLayout(layoutOne)




if __name__ == '__main__':
    app = QApplication(sys.argv)
    demo = QTableViewDemo()
    demo.show()
    sys.exit(app.exec())
