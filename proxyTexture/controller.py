import pymel.core as pm
from PySide2 import QtWidgets, QtCore
import maya.OpenMayaUI as omui
from shiboken2 import wrapInstance
from maya.app.general.mayaMixin import MayaQWidgetDockableMixin

import proxyTexture.core as core
import proxyTexture.mainView as mainView

'''
Open with:
import proxyTexture.controller as proxyTextureCtrl
proxyTextureCtrl.open()
'''


# because maya is changing the colorspace when updating the file path
# some of them are wrong. run this to fix
# of course you need to set the suffixes depending on how your naming scheme works
def fixColorSpace():
    types = ['_ior', '_Normal', '_Glossiness']

    for f in pm.ls(type='file'):
        for t in types:
            if t in f.fileTextureName.get():
                f.colorSpace.set('Raw')


proxyTextureUI = None
def open(develop = False, dockable = False, envVar = ""):

    if develop:
        reload(core)
        reload(mainView)

    try:
        proxyTextureUI.close()
    except:
        pass

    proxyTextureUI = Controller(envVar)
    proxyTextureUI.show(dockable = dockable)

# wrapper to get mayas main window
def getMayaMainWindow():
    mayaPtr = omui.MQtUtil.mainWindow()
    return wrapInstance(long(mayaPtr), QtWidgets.QWidget)


class Controller(MayaQWidgetDockableMixin, QtWidgets.QMainWindow, mainView.Ui_proxyTextureWindow):

    def __init__(self, envVar, parent = getMayaMainWindow()):
        super(Controller, self).__init__(parent)

        self.envVar = envVar

        self.setupUi(self)

        self.core = core.Core()

        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)

        self.createConnections()

    def createConnections(self):
        self.size_comboBox.activated.connect(self.changeTextureSize)

    def changeTextureSize(self):
        size = self.size_comboBox.currentText()
        self.core.changeTextureSize(size, self.envVar)