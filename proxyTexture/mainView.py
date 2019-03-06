# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\Masterprojekt\03_Production\Maya\scripts\proxyTexture\mainView.ui'
#
# Created: Wed Jul 18 22:46:57 2018
#      by: pyside2-uic  running on PySide2 2.0.0~alpha0
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_proxyTextureWindow(object):
    def setupUi(self, proxyTextureWindow):
        proxyTextureWindow.setObjectName("proxyTextureWindow")
        proxyTextureWindow.resize(248, 98)
        self.centralwidget = QtWidgets.QWidget(proxyTextureWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.size_label = QtWidgets.QLabel(self.centralwidget)
        self.size_label.setObjectName("size_label")
        self.verticalLayout.addWidget(self.size_label)
        self.size_comboBox = QtWidgets.QComboBox(self.centralwidget)
        self.size_comboBox.setObjectName("size_comboBox")
        self.size_comboBox.addItem("")
        self.size_comboBox.addItem("")
        self.size_comboBox.addItem("")
        self.verticalLayout.addWidget(self.size_comboBox)
        proxyTextureWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(proxyTextureWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 248, 21))
        self.menubar.setObjectName("menubar")
        proxyTextureWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(proxyTextureWindow)
        self.statusbar.setObjectName("statusbar")
        proxyTextureWindow.setStatusBar(self.statusbar)

        self.retranslateUi(proxyTextureWindow)
        QtCore.QMetaObject.connectSlotsByName(proxyTextureWindow)

    def retranslateUi(self, proxyTextureWindow):
        proxyTextureWindow.setWindowTitle(QtWidgets.QApplication.translate("proxyTextureWindow", "Proxy Texture", None, -1))
        self.size_label.setText(QtWidgets.QApplication.translate("proxyTextureWindow", "Texture Size", None, -1))
        self.size_comboBox.setItemText(0, QtWidgets.QApplication.translate("proxyTextureWindow", "original", None, -1))
        self.size_comboBox.setItemText(1, QtWidgets.QApplication.translate("proxyTextureWindow", "512", None, -1))
        self.size_comboBox.setItemText(2, QtWidgets.QApplication.translate("proxyTextureWindow", "256", None, -1))

