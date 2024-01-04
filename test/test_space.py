import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt


class GUi(QMainWindow):

    def __init__(self):
        super().__init__()
        self.inirUI()

    def inirUI(self):
        # self.win=QWidget()
        self.resize(400, 300)
        self.setWindowTitle('')

        # label_1 = QLabel('第一个标签', self)
        # label_2 = QLabel('第二个标签', self)
        button_1 = QPushButton('按钮', self)
        # button_2 = QPushButton('按钮', self)
        # button_3 = QPushButton('第三个按钮')

        # 网格布局
        hbox_layout = QHBoxLayout()
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)  # 水平
        self.horizontalSpacer_1 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)  # 水平
        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)  # 垂直

        # 添加窗口部件
        # hbox_layout.addItem(self.horizontalSpacer_1)
        # hbox_layout.addWidget(button_1)
        # hbox_layout.addItem(self.horizontalSpacer)
        # hbox_layout.addWidget(button_2)

        # 创建窗口对象
        layout_widget = QWidget()
        # 设置窗口布局层
        layout_widget.setLayout(hbox_layout)
        self.setCentralWidget(layout_widget)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = GUi()
    win.show()
    sys.exit(app.exec_())