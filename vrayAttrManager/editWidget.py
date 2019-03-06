# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\Masterprojekt\03_Production\Maya\scripts\vrayAttrManager\editWidget.ui'
#
# Created: Wed Jan 17 12:42:30 2018
#      by: pyside2-uic  running on PySide2 2.0.0~alpha0
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_editWidget(object):
    def setupUi(self, editWidget):
        editWidget.setObjectName("editWidget")
        editWidget.resize(251, 38)
        self.horizontalLayout = QtWidgets.QHBoxLayout(editWidget)
        self.horizontalLayout.setSpacing(3)
        self.horizontalLayout.setContentsMargins(3, 3, 3, 3)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.editWidget_label = QtWidgets.QLabel(editWidget)
        self.editWidget_label.setObjectName("editWidget_label")
        self.horizontalLayout.addWidget(self.editWidget_label)
        self.editWidget_spinBox = QtWidgets.QSpinBox(editWidget)
        self.editWidget_spinBox.setObjectName("editWidget_spinBox")
        self.horizontalLayout.addWidget(self.editWidget_spinBox)

        self.retranslateUi(editWidget)
        QtCore.QMetaObject.connectSlotsByName(editWidget)

    def retranslateUi(self, editWidget):
        editWidget.setWindowTitle(QtWidgets.QApplication.translate("editWidget", "Form", None, -1))
        self.editWidget_label.setText(QtWidgets.QApplication.translate("editWidget", "TextLabel", None, -1))

