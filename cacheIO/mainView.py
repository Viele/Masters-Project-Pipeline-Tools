# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:/Masterprojekt/03_Production/Maya\scripts\cacheIO\mainView.ui'
#
# Created: Wed Jul 04 15:40:03 2018
#      by: pyside2-uic  running on PySide2 2.0.0~alpha0
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_cacheIO_mainWindow(object):
    def setupUi(self, cacheIO_mainWindow):
        cacheIO_mainWindow.setObjectName("cacheIO_mainWindow")
        cacheIO_mainWindow.resize(293, 368)
        self.centralwidget = QtWidgets.QWidget(cacheIO_mainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.cacheBrowser_layout = QtWidgets.QHBoxLayout()
        self.cacheBrowser_layout.setObjectName("cacheBrowser_layout")
        self.sceneLevel_list = QtWidgets.QListWidget(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sceneLevel_list.sizePolicy().hasHeightForWidth())
        self.sceneLevel_list.setSizePolicy(sizePolicy)
        self.sceneLevel_list.setMinimumSize(QtCore.QSize(60, 0))
        self.sceneLevel_list.setObjectName("sceneLevel_list")
        self.cacheBrowser_layout.addWidget(self.sceneLevel_list)
        self.shotLevel_list = QtWidgets.QListWidget(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.shotLevel_list.sizePolicy().hasHeightForWidth())
        self.shotLevel_list.setSizePolicy(sizePolicy)
        self.shotLevel_list.setMinimumSize(QtCore.QSize(60, 0))
        self.shotLevel_list.setObjectName("shotLevel_list")
        self.cacheBrowser_layout.addWidget(self.shotLevel_list)
        self.cacheLevel_list = QtWidgets.QListWidget(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(100)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cacheLevel_list.sizePolicy().hasHeightForWidth())
        self.cacheLevel_list.setSizePolicy(sizePolicy)
        self.cacheLevel_list.setObjectName("cacheLevel_list")
        self.cacheBrowser_layout.addWidget(self.cacheLevel_list)
        self.verticalLayout.addLayout(self.cacheBrowser_layout)
        self.export_grpBox = QtWidgets.QGroupBox(self.centralwidget)
        self.export_grpBox.setObjectName("export_grpBox")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.export_grpBox)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.export_name = QtWidgets.QLineEdit(self.export_grpBox)
        self.export_name.setObjectName("export_name")
        self.verticalLayout_2.addWidget(self.export_name)
        self.export_layout = QtWidgets.QHBoxLayout()
        self.export_layout.setObjectName("export_layout")
        self.dumbify_chkBox = QtWidgets.QCheckBox(self.export_grpBox)
        self.dumbify_chkBox.setChecked(True)
        self.dumbify_chkBox.setObjectName("dumbify_chkBox")
        self.export_layout.addWidget(self.dumbify_chkBox)
        self.history_chkBox = QtWidgets.QCheckBox(self.export_grpBox)
        self.history_chkBox.setObjectName("history_chkBox")
        self.export_layout.addWidget(self.history_chkBox)
        self.exportSel_btn = QtWidgets.QPushButton(self.export_grpBox)
        self.exportSel_btn.setObjectName("exportSel_btn")
        self.export_layout.addWidget(self.exportSel_btn)
        self.verticalLayout_2.addLayout(self.export_layout)
        self.verticalLayout.addWidget(self.export_grpBox)
        self.import_grpBox = QtWidgets.QGroupBox(self.centralwidget)
        self.import_grpBox.setObjectName("import_grpBox")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.import_grpBox)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.import_btn = QtWidgets.QPushButton(self.import_grpBox)
        self.import_btn.setObjectName("import_btn")
        self.verticalLayout_3.addWidget(self.import_btn)
        self.importAll_btn = QtWidgets.QPushButton(self.import_grpBox)
        self.importAll_btn.setObjectName("importAll_btn")
        self.verticalLayout_3.addWidget(self.importAll_btn)
        self.verticalLayout.addWidget(self.import_grpBox)
        cacheIO_mainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(cacheIO_mainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 293, 21))
        self.menubar.setObjectName("menubar")
        cacheIO_mainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(cacheIO_mainWindow)
        self.statusbar.setObjectName("statusbar")
        cacheIO_mainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(cacheIO_mainWindow)
        QtCore.QMetaObject.connectSlotsByName(cacheIO_mainWindow)

    def retranslateUi(self, cacheIO_mainWindow):
        cacheIO_mainWindow.setWindowTitle(QtWidgets.QApplication.translate("cacheIO_mainWindow", "cache IO", None, -1))
        self.export_grpBox.setTitle(QtWidgets.QApplication.translate("cacheIO_mainWindow", "Export", None, -1))
        self.export_name.setPlaceholderText(QtWidgets.QApplication.translate("cacheIO_mainWindow", "Name", None, -1))
        self.dumbify_chkBox.setToolTip(QtWidgets.QApplication.translate("cacheIO_mainWindow", "Export only clean geo", None, -1))
        self.dumbify_chkBox.setText(QtWidgets.QApplication.translate("cacheIO_mainWindow", "Dumbify", None, -1))
        self.history_chkBox.setText(QtWidgets.QApplication.translate("cacheIO_mainWindow", "History", None, -1))
        self.exportSel_btn.setText(QtWidgets.QApplication.translate("cacheIO_mainWindow", "Export Selected", None, -1))
        self.import_grpBox.setTitle(QtWidgets.QApplication.translate("cacheIO_mainWindow", "Import", None, -1))
        self.import_btn.setText(QtWidgets.QApplication.translate("cacheIO_mainWindow", "Import Selected", None, -1))
        self.importAll_btn.setText(QtWidgets.QApplication.translate("cacheIO_mainWindow", "Import All", None, -1))

