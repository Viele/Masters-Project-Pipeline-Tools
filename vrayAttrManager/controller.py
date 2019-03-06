import pymel.core as pm
import vrayAttrManager.core as core
import vrayAttrManager.mainView as view
import vrayAttrManager.editWidget as editW
from PySide2 import QtWidgets, QtCore
import maya.OpenMayaUI as omui
from shiboken2 import wrapInstance

'''
Open with

import pymel.core as pm
import vrayAttrManager.controller as vrayAttrManagerCtrl
import vrayAttrManager.core as vrayAttrManagerCore

if __name__ == "__main__":
    try:
        vrayAttrManagerWindow.close()
    except:
        pass

    vrayAttrManagerWindow = vrayAttrManagerCtrl.Controller()
    vrayAttrManagerWindow.show()
    
'''


# wrapper to get mayas main window
def getMayaMainWindow():
    mayaPtr = omui.MQtUtil.mainWindow()
    return wrapInstance(long(mayaPtr), QtWidgets.QWidget)


class Controller(QtWidgets.QMainWindow, view.Ui_vrayAttrManager):

    objTypes = {'Mesh':'mesh', 'Transform':'transform', 'V-Ray material':'VRayMtl'}
    meshAttrs = {
        'Subdivision' : 'vray_subdivision', 
        'Subdivision and Displacement Quality':'vray_subquality', 
        'Displacement control': 'vray_displacement', 
        'OpenSubdiv':'vray_opensubdiv', 
        'Round edges':'vray_roundedges', 
        'User attributes':'vray_user_attributes', 
        'Object ID':'vray_objectID', 
        'Fog fade out radius':'vray_fogFadeOut'
    }
    transformAttrs = {
        'Skip rendering':'vray_skip_export',
        'Object ID':'vray_objectID',
        'User attributes':'vray_user_attributes'
    }
    vMaterialAttrs = {
        'Material ID':'vray_material_id',
        'V-Ray material override':'vray_specific_mtl',
        'Closed Volume Shading':'vray_closed_volume'
    }
    

    def __init__(self, parent = getMayaMainWindow()):
        super(Controller, self).__init__(parent)

        self.setupUi(self)

        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)

        self.core = core.Core()

        for k, v in self.objTypes.iteritems():
            self.objType_cbox.addItem(k)

        self.updateAttrCBox()

        self.createConnections()


    def createConnections(self):
        self.objType_cbox.currentIndexChanged.connect(self.updateAttrCBox)
        self.attr_add_btn.clicked.connect(self.prepareAttrAdd)
        self.attr_remove_btn.clicked.connect(self.prepareAttrRm)
        self.edit_refresh_btn.clicked.connect(self.updateAttrEditList)


    def updateAttrCBox(self):

        self.attrType_cbox.clear()

        for k, v in self.getAttrs().iteritems():
            self.attrType_cbox.addItem(k)
    

    def updateAttrEditList(self):

        self.edit_listWidget.clear()

        # get Targets
        targets = pm.selected()

        for t in targets:
            try:
                targets.extend(t.getShapes())
            except:
                pass

        # getAttrs
        attrDict = {}
        for t in targets:
            for attr in t.listAttr(st = 'vray*'):
                if attr.type() != 'string':
                    attrDict[attr.attrName()] = attr.get()

        for attr, value in attrDict.iteritems():
            listItem = QtWidgets.QListWidgetItem()
            editWidget = EditWidget(self.edit_listWidget, attr, value)
            listItem.setSizeHint(editWidget.sizeHint())
            self.edit_listWidget.addItem(listItem)
            self.edit_listWidget.setItemWidget(listItem, editWidget)



    def prepareAttrAdd(self):

        self.core.addAttrFromGroup(
            self.getTargets(self.objTypes[self.objType_cbox.currentText()]), 
            self.getAttrs()[self.attrType_cbox.currentText()]
            )

        self.updateAttrEditList()


    def prepareAttrRm(self):

        self.core.rmAttrFromGroup(
            self.getTargets(self.objTypes[self.objType_cbox.currentText()]), 
            self.getAttrs()[self.attrType_cbox.currentText()]
            )

        self.updateAttrEditList()


    def getTargets(self, objType):

        tempTargets = pm.selected()

         # get possible shapes
        for t in tempTargets:
            try:
                tempTargets.extend(t.getShapes())
            except:
                pass

        targets = []
        for t in tempTargets:
            if t.type() == objType:
                targets.append(t)

        return targets


    def getAttrs(self):
        if(self.objType_cbox.currentText() == 'Mesh'): 
            return self.meshAttrs
        if(self.objType_cbox.currentText() == 'Transform'): 
            return self.transformAttrs
        if(self.objType_cbox.currentText() == 'V-Ray material'): 
            return self.vMaterialAttrs



class EditWidget(QtWidgets.QWidget, editW.Ui_editWidget):

    def __init__(self, parent, attrName, value):
        super(EditWidget, self).__init__(parent)

        self.setupUi(self)

        self.attrName = attrName

        self.editWidget_label.setText(attrName)

        self.editWidget_spinBox.setValue(value)

        self.editWidget_spinBox.valueChanged.connect(self.prepareAttrEdit)


    def prepareAttrEdit(self):

        # get Targets
        targets = pm.selected()

        for t in targets:
            if t.hasAttr(self.attrName):
                getattr(t, self.attrName).set(self.sender().value())