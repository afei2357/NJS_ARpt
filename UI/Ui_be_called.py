# Form implementation generated from reading ui file 'Ui_be_called.ui'
#
# Created by: PyQt6 UI code generator 6.4.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_widget(object):
    def setupUi(self, widget):
        widget.setObjectName("widget")
        widget.resize(843, 655)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("../images/logo.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        widget.setWindowIcon(icon)
        self.verticalLayoutWidget_2 = QtWidgets.QWidget(widget)
        self.verticalLayoutWidget_2.setGeometry(QtCore.QRect(20, 60, 811, 491))
        self.verticalLayoutWidget_2.setObjectName("verticalLayoutWidget_2")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_2)
        self.verticalLayout_2.setSizeConstraint(QtWidgets.QLayout.SizeConstraint.SetMinAndMaxSize)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setSpacing(9)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.operatorLayout = QtWidgets.QHBoxLayout()
        self.operatorLayout.setObjectName("operatorLayout")
        self.prevButton = QtWidgets.QPushButton(self.verticalLayoutWidget_2)
        self.prevButton.setObjectName("prevButton")
        self.operatorLayout.addWidget(self.prevButton)
        self.nextButton = QtWidgets.QPushButton(self.verticalLayoutWidget_2)
        self.nextButton.setObjectName("nextButton")
        self.operatorLayout.addWidget(self.nextButton)
        self.switchPage = QtWidgets.QLabel(self.verticalLayoutWidget_2)
        self.switchPage.setObjectName("switchPage")
        self.operatorLayout.addWidget(self.switchPage)
        self.switchPageLineEdit = QtWidgets.QLineEdit(self.verticalLayoutWidget_2)
        self.switchPageLineEdit.setMaximumSize(QtCore.QSize(50, 16777215))
        self.switchPageLineEdit.setObjectName("switchPageLineEdit")
        self.operatorLayout.addWidget(self.switchPageLineEdit)
        self.page = QtWidgets.QLabel(self.verticalLayoutWidget_2)
        self.page.setMaximumSize(QtCore.QSize(30, 16777215))
        self.page.setObjectName("page")
        self.operatorLayout.addWidget(self.page)
        self.switchPageButton = QtWidgets.QPushButton(self.verticalLayoutWidget_2)
        self.switchPageButton.setObjectName("switchPageButton")
        self.operatorLayout.addWidget(self.switchPageButton)
        self.verticalLayout_2.addLayout(self.operatorLayout)
        self.tableView = QtWidgets.QTableView(self.verticalLayoutWidget_2)
        self.tableView.setObjectName("tableView")
        self.verticalLayout_2.addWidget(self.tableView)
        self.statusLayout = QtWidgets.QHBoxLayout()
        self.statusLayout.setObjectName("statusLayout")
        self.totalPageLabel = QtWidgets.QLabel(self.verticalLayoutWidget_2)
        self.totalPageLabel.setMaximumSize(QtCore.QSize(70, 16777215))
        self.totalPageLabel.setObjectName("totalPageLabel")
        self.statusLayout.addWidget(self.totalPageLabel)
        self.currentPageLabel = QtWidgets.QLabel(self.verticalLayoutWidget_2)
        self.currentPageLabel.setMaximumSize(QtCore.QSize(70, 70))
        self.currentPageLabel.setObjectName("currentPageLabel")
        self.statusLayout.addWidget(self.currentPageLabel)
        self.totalRecordLabel = QtWidgets.QLabel(self.verticalLayoutWidget_2)
        self.totalRecordLabel.setMaximumSize(QtCore.QSize(70, 16777215))
        self.totalRecordLabel.setObjectName("totalRecordLabel")
        self.statusLayout.addWidget(self.totalRecordLabel)
        self.verticalLayout_2.addLayout(self.statusLayout)
        self.btnExportInfo = QtWidgets.QPushButton(widget)
        self.btnExportInfo.setGeometry(QtCore.QRect(680, 590, 151, 31))
        self.btnExportInfo.setObjectName("btnExportInfo")

        self.retranslateUi(widget)
        QtCore.QMetaObject.connectSlotsByName(widget)

    def retranslateUi(self, widget):
        _translate = QtCore.QCoreApplication.translate
        widget.setWindowTitle(_translate("widget", "数据库"))
        self.prevButton.setText(_translate("widget", "前一页"))
        self.nextButton.setText(_translate("widget", "后一页"))
        self.switchPage.setText(_translate("widget", "跳转到"))
        self.page.setText(_translate("widget", "页"))
        self.switchPageButton.setText(_translate("widget", "go"))
        self.totalPageLabel.setText(_translate("widget", "TextLabel"))
        self.currentPageLabel.setText(_translate("widget", "TextLabel"))
        self.totalRecordLabel.setText(_translate("widget", "TextLabel"))
        self.btnExportInfo.setText(_translate("widget", "导出为excel"))