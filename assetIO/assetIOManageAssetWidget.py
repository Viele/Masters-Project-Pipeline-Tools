# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\Masterprojekt\03_Production\Maya\scripts\assetIO\assetIOManageAssetWidget.ui'
#
# Created: Tue Jan 23 13:28:02 2018
#      by: pyside2-uic  running on PySide2 2.0.0~alpha0
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_manage_widget(object):
    def setupUi(self, manage_widget):
        manage_widget.setObjectName("manage_widget")
        manage_widget.resize(358, 37)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(manage_widget.sizePolicy().hasHeightForWidth())
        manage_widget.setSizePolicy(sizePolicy)
        manage_widget.setMinimumSize(QtCore.QSize(0, 0))
        manage_widget.setMaximumSize(QtCore.QSize(16777215, 16777215))
        manage_widget.setStyleSheet("padding: 0px; margin: 0px;")
        self.manage_widget_layout = QtWidgets.QHBoxLayout(manage_widget)
        self.manage_widget_layout.setSpacing(6)
        self.manage_widget_layout.setContentsMargins(8, 2, 8, 2)
        self.manage_widget_layout.setObjectName("manage_widget_layout")
        self.manage_assetName = QtWidgets.QLabel(manage_widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.manage_assetName.sizePolicy().hasHeightForWidth())
        self.manage_assetName.setSizePolicy(sizePolicy)
        self.manage_assetName.setMinimumSize(QtCore.QSize(0, 20))
        self.manage_assetName.setMaximumSize(QtCore.QSize(16777215, 20))
        self.manage_assetName.setObjectName("manage_assetName")
        self.manage_widget_layout.addWidget(self.manage_assetName)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.manage_widget_layout.addItem(spacerItem)
        self.manage_instanceCount_label = QtWidgets.QLabel(manage_widget)
        self.manage_instanceCount_label.setObjectName("manage_instanceCount_label")
        self.manage_widget_layout.addWidget(self.manage_instanceCount_label)
        self.manage_instanceCount_display = QtWidgets.QLabel(manage_widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.manage_instanceCount_display.sizePolicy().hasHeightForWidth())
        self.manage_instanceCount_display.setSizePolicy(sizePolicy)
        self.manage_instanceCount_display.setObjectName("manage_instanceCount_display")
        self.manage_widget_layout.addWidget(self.manage_instanceCount_display)
        self.manage_reference_button = QtWidgets.QPushButton(manage_widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.manage_reference_button.sizePolicy().hasHeightForWidth())
        self.manage_reference_button.setSizePolicy(sizePolicy)
        self.manage_reference_button.setMinimumSize(QtCore.QSize(0, 20))
        self.manage_reference_button.setMaximumSize(QtCore.QSize(16777215, 20))
        self.manage_reference_button.setObjectName("manage_reference_button")
        self.manage_widget_layout.addWidget(self.manage_reference_button)
        self.manage_visibility_button = QtWidgets.QPushButton(manage_widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.manage_visibility_button.sizePolicy().hasHeightForWidth())
        self.manage_visibility_button.setSizePolicy(sizePolicy)
        self.manage_visibility_button.setMinimumSize(QtCore.QSize(20, 20))
        self.manage_visibility_button.setMaximumSize(QtCore.QSize(20, 20))
        self.manage_visibility_button.setCursor(QtCore.Qt.ArrowCursor)
        self.manage_visibility_button.setText("")
        self.manage_visibility_button.setIconSize(QtCore.QSize(20, 20))
        self.manage_visibility_button.setCheckable(True)
        self.manage_visibility_button.setChecked(False)
        self.manage_visibility_button.setFlat(True)
        self.manage_visibility_button.setObjectName("manage_visibility_button")
        self.manage_widget_layout.addWidget(self.manage_visibility_button)
        self.manage_annotationVisibility_button = QtWidgets.QPushButton(manage_widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.manage_annotationVisibility_button.sizePolicy().hasHeightForWidth())
        self.manage_annotationVisibility_button.setSizePolicy(sizePolicy)
        self.manage_annotationVisibility_button.setMinimumSize(QtCore.QSize(20, 20))
        self.manage_annotationVisibility_button.setMaximumSize(QtCore.QSize(20, 20))
        self.manage_annotationVisibility_button.setCursor(QtCore.Qt.ArrowCursor)
        self.manage_annotationVisibility_button.setText("")
        self.manage_annotationVisibility_button.setIconSize(QtCore.QSize(20, 20))
        self.manage_annotationVisibility_button.setCheckable(True)
        self.manage_annotationVisibility_button.setFlat(True)
        self.manage_annotationVisibility_button.setObjectName("manage_annotationVisibility_button")
        self.manage_widget_layout.addWidget(self.manage_annotationVisibility_button)
        self.manage_delete_button = QtWidgets.QPushButton(manage_widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.manage_delete_button.sizePolicy().hasHeightForWidth())
        self.manage_delete_button.setSizePolicy(sizePolicy)
        self.manage_delete_button.setMinimumSize(QtCore.QSize(20, 20))
        self.manage_delete_button.setMaximumSize(QtCore.QSize(20, 20))
        self.manage_delete_button.setText("")
        self.manage_delete_button.setIconSize(QtCore.QSize(20, 20))
        self.manage_delete_button.setFlat(True)
        self.manage_delete_button.setObjectName("manage_delete_button")
        self.manage_widget_layout.addWidget(self.manage_delete_button)

        self.retranslateUi(manage_widget)
        QtCore.QMetaObject.connectSlotsByName(manage_widget)

    def retranslateUi(self, manage_widget):
        manage_widget.setWindowTitle(QtWidgets.QApplication.translate("manage_widget", "Manage Asset Widget", None, -1))
        self.manage_assetName.setText(QtWidgets.QApplication.translate("manage_widget", "AssetName", None, -1))
        self.manage_instanceCount_label.setText(QtWidgets.QApplication.translate("manage_widget", "Reference Count", None, -1))
        self.manage_instanceCount_display.setText(QtWidgets.QApplication.translate("manage_widget", "0", None, -1))
        self.manage_reference_button.setText(QtWidgets.QApplication.translate("manage_widget", "Reference", None, -1))

