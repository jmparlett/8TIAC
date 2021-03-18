# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'design.ui'
#
# Created by: PyQt5 UI code generator 5.15.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1029, 830)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_7 = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_7.setObjectName("gridLayout_7")
        self.section2 = QtWidgets.QGridLayout()
        self.section2.setObjectName("section2")
        self.aluDataTableLable = QtWidgets.QLabel(self.centralwidget)
        self.aluDataTableLable.setObjectName("aluDataTableLable")
        self.section2.addWidget(self.aluDataTableLable, 1, 0, 1, 1)
        self.aluDataTable = QtWidgets.QTableWidget(self.centralwidget)
        self.aluDataTable.setObjectName("aluDataTable")
        self.aluDataTable.setColumnCount(0)
        self.aluDataTable.setRowCount(0)
        self.section2.addWidget(self.aluDataTable, 2, 0, 1, 1)
        self.gridLayout_7.addLayout(self.section2, 0, 0, 1, 1)
        self.section1 = QtWidgets.QVBoxLayout()
        self.section1.setObjectName("section1")
        self.marLable = QtWidgets.QLabel(self.centralwidget)
        self.marLable.setEnabled(True)
        self.marLable.setObjectName("marLable")
        self.section1.addWidget(self.marLable)
        self.marContents = QtWidgets.QLabel(self.centralwidget)
        self.marContents.setObjectName("marContents")
        self.section1.addWidget(self.marContents)
        self.memoryTableLable = QtWidgets.QLabel(self.centralwidget)
        self.memoryTableLable.setObjectName("memoryTableLable")
        self.section1.addWidget(self.memoryTableLable)
        self.memoryTable = QtWidgets.QTableWidget(self.centralwidget)
        self.memoryTable.setObjectName("memoryTable")
        self.memoryTable.setColumnCount(3)
        self.memoryTable.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.memoryTable.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.memoryTable.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.memoryTable.setHorizontalHeaderItem(2, item)
        self.section1.addWidget(self.memoryTable)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.section1.addItem(spacerItem)
        self.registerTableLable = QtWidgets.QLabel(self.centralwidget)
        self.registerTableLable.setObjectName("registerTableLable")
        self.section1.addWidget(self.registerTableLable)
        self.regTable = QtWidgets.QTableWidget(self.centralwidget)
        self.regTable.setObjectName("regTable")
        self.regTable.setColumnCount(3)
        self.regTable.setRowCount(4)
        item = QtWidgets.QTableWidgetItem()
        self.regTable.setVerticalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.regTable.setVerticalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.regTable.setVerticalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.regTable.setVerticalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.regTable.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.regTable.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.regTable.setHorizontalHeaderItem(2, item)
        self.section1.addWidget(self.regTable)
        self.gridLayout_7.addLayout(self.section1, 0, 1, 2, 1)
        self.gridLayout_2 = QtWidgets.QGridLayout()
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setObjectName("label")
        self.gridLayout_2.addWidget(self.label, 0, 0, 1, 1)
        self.tableWidget_2 = QtWidgets.QTableWidget(self.centralwidget)
        self.tableWidget_2.setObjectName("tableWidget_2")
        self.tableWidget_2.setColumnCount(0)
        self.tableWidget_2.setRowCount(0)
        self.gridLayout_2.addWidget(self.tableWidget_2, 1, 0, 1, 1)
        self.gridLayout_7.addLayout(self.gridLayout_2, 1, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.aluDataTableLable.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-size:14pt; font-weight:600;\">ALU (Arithmetic Logic Unit)</span></p></body></html>"))
        self.marLable.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-size:14pt; font-weight:600;\">MAR (Memory Address Register)</span></p></body></html>"))
        self.marContents.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-size:12pt; font-weight:600;\">[TextLabel]</span></p></body></html>"))
        self.memoryTableLable.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-size:14pt; font-weight:600;\">Memory Contents</span></p></body></html>"))
        item = self.memoryTable.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "S bit"))
        item = self.memoryTable.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "E bit"))
        item = self.memoryTable.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "byteValue"))
        self.registerTableLable.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-size:14pt; font-weight:600;\">Register Contents</span></p></body></html>"))
        item = self.regTable.verticalHeaderItem(0)
        item.setText(_translate("MainWindow", "R0"))
        item = self.regTable.verticalHeaderItem(1)
        item.setText(_translate("MainWindow", "R1"))
        item = self.regTable.verticalHeaderItem(2)
        item.setText(_translate("MainWindow", "R2"))
        item = self.regTable.verticalHeaderItem(3)
        item.setText(_translate("MainWindow", "R3"))
        item = self.regTable.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "S bit"))
        item = self.regTable.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "E bit"))
        item = self.regTable.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "byteValue"))
        self.label.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-size:14pt; font-weight:600;\">CLU (Central Logic Unit)</span></p></body></html>"))
