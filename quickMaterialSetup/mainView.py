# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\Masterprojekt\03_Production\Maya\scripts\quickMaterialSetup\mainView.ui'
#
# Created: Fri Nov 03 10:33:21 2017
#      by: pyside2-uic  running on PySide2 2.0.0~alpha0
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_QuickMaterialSetup(object):
    def setupUi(self, QuickMaterialSetup):
        QuickMaterialSetup.setObjectName("QuickMaterialSetup")
        QuickMaterialSetup.resize(348, 103)
        self.main_widget = QtWidgets.QWidget(QuickMaterialSetup)
        self.main_widget.setObjectName("main_widget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.main_widget)
        self.verticalLayout.setContentsMargins(-1, 5, -1, 1)
        self.verticalLayout.setObjectName("verticalLayout")
        self.browse_layout = QtWidgets.QHBoxLayout()
        self.browse_layout.setObjectName("browse_layout")
        self.browse_input = QtWidgets.QLineEdit(self.main_widget)
        self.browse_input.setObjectName("browse_input")
        self.browse_layout.addWidget(self.browse_input)
        self.browse_btn = QtWidgets.QPushButton(self.main_widget)
        self.browse_btn.setObjectName("browse_btn")
        self.browse_layout.addWidget(self.browse_btn)
        self.verticalLayout.addLayout(self.browse_layout)
        self.confirm_layout = QtWidgets.QHBoxLayout()
        self.confirm_layout.setObjectName("confirm_layout")
        self.confirm_create_btn = QtWidgets.QPushButton(self.main_widget)
        self.confirm_create_btn.setObjectName("confirm_create_btn")
        self.confirm_layout.addWidget(self.confirm_create_btn)
        self.confirm_assign_btn = QtWidgets.QPushButton(self.main_widget)
        self.confirm_assign_btn.setObjectName("confirm_assign_btn")
        self.confirm_layout.addWidget(self.confirm_assign_btn)
        self.verticalLayout.addLayout(self.confirm_layout)
        QuickMaterialSetup.setCentralWidget(self.main_widget)
        self.menubar = QtWidgets.QMenuBar(QuickMaterialSetup)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 348, 21))
        self.menubar.setObjectName("menubar")
        QuickMaterialSetup.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(QuickMaterialSetup)
        self.statusbar.setObjectName("statusbar")
        QuickMaterialSetup.setStatusBar(self.statusbar)

        self.retranslateUi(QuickMaterialSetup)
        QtCore.QMetaObject.connectSlotsByName(QuickMaterialSetup)

    def retranslateUi(self, QuickMaterialSetup):
        QuickMaterialSetup.setWindowTitle(QtWidgets.QApplication.translate("QuickMaterialSetup", "Quick Material Setup", None, -1))
        self.browse_btn.setText(QtWidgets.QApplication.translate("QuickMaterialSetup", "Browse", None, -1))
        self.confirm_create_btn.setText(QtWidgets.QApplication.translate("QuickMaterialSetup", "Create", None, -1))
        self.confirm_assign_btn.setText(QtWidgets.QApplication.translate("QuickMaterialSetup", "Create and Assign", None, -1))

