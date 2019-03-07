import pymel.core as pm

from PySide2 import QtWidgets, QtCore
import maya.OpenMayaUI as omui
from shiboken2 import wrapInstance

import sceneChecker.core as core
import sceneChecker.mainView as view

'''
Open with

import sceneChecker.controller as sceneChkCtrl
reload(sceneChkCtrl)
sceneChkCtrl.open()
    
'''







tmpWindow = None
def open(develop = False):

    if develop:
        reload(core)
        reload(view)

    try:
        tmpWindow.close()
    except:
        pass

    tmpWindow = Controller()
    tmpWindow.show()


# wrapper to get mayas main window
def getMayaMainWindow():
    mayaPtr = omui.MQtUtil.mainWindow()
    return wrapInstance(long(mayaPtr), QtWidgets.QWidget)



'''
The controller is the bridge between ui and functionality
'''
class Controller(QtWidgets.QMainWindow, view.Ui_sceneChecker):

    def __init__(self, parent = getMayaMainWindow()):
        super(Controller, self).__init__(parent)

        self.setupUi(self)

        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)

        self.core = core.Core()

        self.createConnections()


    # linking buttons to functions
    def createConnections(self):
        self.checkScene_btn.clicked.connect(self.checkScene)
        self.openSubdiv_select_btn.clicked.connect(self.selectOpenSubdiv)
        self.shadowCasting_select_btn.clicked.connect(self.selectNoShadow)

    def checkScene(self):
        # proxy textures
        proxyTexturesResult = self.core.checkProxyTextures()
        if proxyTexturesResult:
            self.proxyTexture_message.setText('Full resolution active.')
            self.proxyTexture_message.setStyleSheet('QLabel { color : lime; }')
        else:
            self.proxyTexture_message.setText('Proxy Textures found!')
            self.proxyTexture_message.setStyleSheet('QLabel { color : red; }')

        # open subdiv
        noSubdivCount = self.core.checkOpenSubdiv()
        self.openSubdiv_count.setText(str(noSubdivCount))

        # shadow objects
        noShadowCount = self.core.checkShadowCasting()
        self.shadowCasting_count.setText(str(noShadowCount))
        

        # aovs
        aovCount = self.core.checkAOVs()
        self.renderElements_count.setText(str(aovCount))
        if aovCount == 0:
            self.renderElements_count.setStyleSheet('QLabel { color : red; }')
        elif aovCount < 7:
            self.renderElements_count.setStyleSheet('QLabel { color : yellow; }')
        else:
            self.renderElements_count.setStyleSheet('QLabel { color : lime; }')

        # render settings
        try:
            self.core.checkRenderSettings()
            self.renderSettings_message.setText('Render Settings are correct')
            self.renderSettings_message.setStyleSheet('QLabel { color : lime; }')
        except Exception as e:
            self.renderSettings_message.setText(e.message)
            self.renderSettings_message.setStyleSheet('QLabel { color : red; }')

    def selectOpenSubdiv(self):
        pm.select(self.core.noSubdivObjects)

    def selectNoShadow(self):
        pm.select(self.core.noShadowObjects)


