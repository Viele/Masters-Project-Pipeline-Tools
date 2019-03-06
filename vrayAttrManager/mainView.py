# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\Masterprojekt\03_Production\Maya\scripts\vrayAttrManager\mainView.ui'
#
# Created: Wed Jan 17 11:14:05 2018
#      by: pyside2-uic  running on PySide2 2.0.0~alpha0
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_vrayAttrManager(object):
    def setupUi(self, vrayAttrManager):
        vrayAttrManager.setObjectName("vrayAttrManager")
        vrayAttrManager.resize(265, 277)
        self.vrayAttrManager_widget = QtWidgets.QWidget(vrayAttrManager)
        self.vrayAttrManager_widget.setObjectName("vrayAttrManager_widget")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.vrayAttrManager_widget)
        self.verticalLayout_3.setSpacing(3)
        self.verticalLayout_3.setContentsMargins(3, 3, 3, 3)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.create_grpBox = QtWidgets.QGroupBox(self.vrayAttrManager_widget)
        self.create_grpBox.setObjectName("create_grpBox")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.create_grpBox)
        self.verticalLayout_2.setSpacing(3)
        self.verticalLayout_2.setContentsMargins(3, 3, 3, 3)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.manage_layout = QtWidgets.QVBoxLayout()
        self.manage_layout.setObjectName("manage_layout")
        self.objType_cbox = QtWidgets.QComboBox(self.create_grpBox)
        self.objType_cbox.setObjectName("objType_cbox")
        self.manage_layout.addWidget(self.objType_cbox)
        self.attrType_cbox = QtWidgets.QComboBox(self.create_grpBox)
        self.attrType_cbox.setObjectName("attrType_cbox")
        self.manage_layout.addWidget(self.attrType_cbox)
        self.manage_btn_layout = QtWidgets.QHBoxLayout()
        self.manage_btn_layout.setObjectName("manage_btn_layout")
        self.attr_add_btn = QtWidgets.QPushButton(self.create_grpBox)
        self.attr_add_btn.setObjectName("attr_add_btn")
        self.manage_btn_layout.addWidget(self.attr_add_btn)
        self.attr_remove_btn = QtWidgets.QPushButton(self.create_grpBox)
        self.attr_remove_btn.setObjectName("attr_remove_btn")
        self.manage_btn_layout.addWidget(self.attr_remove_btn)
        self.manage_layout.addLayout(self.manage_btn_layout)
        self.verticalLayout_2.addLayout(self.manage_layout)
        self.verticalLayout_3.addWidget(self.create_grpBox)
        self.edit_grpBox = QtWidgets.QGroupBox(self.vrayAttrManager_widget)
        self.edit_grpBox.setObjectName("edit_grpBox")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.edit_grpBox)
        self.verticalLayout.setObjectName("verticalLayout")
        self.edit_refresh_btn = QtWidgets.QPushButton(self.edit_grpBox)
        self.edit_refresh_btn.setObjectName("edit_refresh_btn")
        self.verticalLayout.addWidget(self.edit_refresh_btn)
        self.edit_listWidget = QtWidgets.QListWidget(self.edit_grpBox)
        self.edit_listWidget.setObjectName("edit_listWidget")
        self.verticalLayout.addWidget(self.edit_listWidget)
        self.verticalLayout_3.addWidget(self.edit_grpBox)
        vrayAttrManager.setCentralWidget(self.vrayAttrManager_widget)
        self.menubar = QtWidgets.QMenuBar(vrayAttrManager)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 265, 21))
        self.menubar.setObjectName("menubar")
        vrayAttrManager.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(vrayAttrManager)
        self.statusbar.setObjectName("statusbar")
        vrayAttrManager.setStatusBar(self.statusbar)

        self.retranslateUi(vrayAttrManager)
        QtCore.QMetaObject.connectSlotsByName(vrayAttrManager)

    def retranslateUi(self, vrayAttrManager):
        vrayAttrManager.setWindowTitle(QtWidgets.QApplication.translate("vrayAttrManager", "Vray Attribute Manager", None, -1))
        self.create_grpBox.setTitle(QtWidgets.QApplication.translate("vrayAttrManager", "Create", None, -1))
        self.attr_add_btn.setText(QtWidgets.QApplication.translate("vrayAttrManager", "Add", None, -1))
        self.attr_remove_btn.setText(QtWidgets.QApplication.translate("vrayAttrManager", "Remove", None, -1))
        self.edit_grpBox.setTitle(QtWidgets.QApplication.translate("vrayAttrManager", "Edit", None, -1))
        self.edit_refresh_btn.setText(QtWidgets.QApplication.translate("vrayAttrManager", "Refresh", None, -1))

