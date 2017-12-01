# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'memo.ui'
#
# Created: Tue Nov 28 18:21:10 2017
#      by: pyside-uic 0.2.15 running on PySide 1.2.2
#
# WARNING! All changes made in this file will be lost!
from PySide import QtCore, QtGui

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtGui.QWidget(MainWindow)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_2 = QtGui.QGridLayout(self.centralwidget)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setSizeConstraint(QtGui.QLayout.SetMaximumSize)
        self.gridLayout.setObjectName("gridLayout")
        self.pushButtonAdd = QtGui.QPushButton(self.centralwidget)
        self.pushButtonAdd.setObjectName("pushButtonAdd")
        self.gridLayout.addWidget(self.pushButtonAdd, 3, 0, 3, 2)
        self.lineEditPath = QtGui.QLineEdit(self.centralwidget)
        self.lineEditPath.setObjectName("lineEditPath")
        self.gridLayout.addWidget(self.lineEditPath, 0, 1, 1, 1)
        self.labelPath = QtGui.QLabel(self.centralwidget)
        self.labelPath.setAlignment(QtCore.Qt.AlignCenter)
        self.labelPath.setObjectName("labelPath")
        self.gridLayout.addWidget(self.labelPath, 0, 0, 1, 1)
        self.labelSearch = QtGui.QLabel(self.centralwidget)
        self.labelSearch.setAlignment(QtCore.Qt.AlignCenter)
        self.labelSearch.setObjectName("labelSearch")
        self.gridLayout.addWidget(self.labelSearch, 1, 0, 1, 1)
        self.lineEditSearch = QtGui.QLineEdit(self.centralwidget)
        self.lineEditSearch.setObjectName("lineEditSearch")
        self.gridLayout.addWidget(self.lineEditSearch, 1, 1, 1, 1)
        self.tableWidget = QtGui.QTableWidget(self.centralwidget)
        self.tableWidget.setRowCount(1)
        self.tableWidget.setColumnCount(4)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(4)
        self.tableWidget.setRowCount(1)
        self.tableWidget.horizontalHeader().setHighlightSections(True)
        self.tableWidget.verticalHeader().setVisible(True)
        self.gridLayout.addWidget(self.tableWidget, 2, 0, 1, 3)
        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 37))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "Memo", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButtonAdd.setText(QtGui.QApplication.translate("MainWindow", "Add New Alias", None, QtGui.QApplication.UnicodeUTF8))
        self.labelPath.setText(QtGui.QApplication.translate("MainWindow", "Collection Path", None, QtGui.QApplication.UnicodeUTF8))
        self.labelSearch.setText(QtGui.QApplication.translate("MainWindow", "Filter", None, QtGui.QApplication.UnicodeUTF8))
        self.tableWidget.setSortingEnabled(True)

