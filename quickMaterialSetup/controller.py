import pymel.core as pm
import quickMaterialSetup.core as core
import quickMaterialSetup.mainView as view
from PySide2 import QtWidgets, QtCore
import maya.OpenMayaUI as omui
from shiboken2 import wrapInstance
import os

'''
Open with

import quickMaterialSetup.controller as qmsCtrl
qmsCtrl.open(envVar = <envVar>, develop = ?)
    
'''






'''
This tool makes creating and assigning VRAY materials that have been created in substance painter easier.
It provides a ui where you browse for a texture. Any texture of the set will do.
Then it gives you the option to create or create+assign
It automatically sets the correct colorspace for the textures
If the filename has two dots (eg.: texture.1001.png) it is detected as UDIM and set that way

Not that for this script to work correctly you need to have the correct naming. 
By default the vray export preset from Substance painter should do the trick, 
but just in case here is how it needs to be named

diffuse: *textureName*_Diffuse.*extension*
glossiness: *textureName*_Glossiness.*extension*
ior: *textureName*_ior.*extension*
normal: *textureName*_Normal.*extension*
reflection: *textureName*_Reflection.*extension*


other map types are not automatically generated, but it should be fairly easy to do
take a look at core.py for more info on how it works
'''
qmsWindow = None
def open(envVar = 'TH_PROJ', develop = False):

    if develop:
        reload(core)
        reload(view)

    try:
        qmsWindow.close()
    except:
        pass

    qmsWindow = Controller(envVar)
    qmsWindow.show()


# wrapper to get mayas main window
def getMayaMainWindow():
    mayaPtr = omui.MQtUtil.mainWindow()
    return wrapInstance(long(mayaPtr), QtWidgets.QWidget)



'''
The controller is the bridge between ui and functionality
'''
class Controller(QtWidgets.QMainWindow, view.Ui_QuickMaterialSetup):

    def __init__(self, envVar, parent = getMayaMainWindow()):
        super(Controller, self).__init__(parent)

        self.setupUi(self)

        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)

        self.core = core.Core(envVar)

        # on ui launch it saves the project you are in
        # when you hit browse it auto directs you to sourceimages
        self.resourcePath = os.path.join(pm.system.workspace.path, 'sourceimages')

        self.createConnections()

        # obviously you need vray
        # load plugin if not loaded
        if not pm.system.pluginInfo("vrayformaya", q = True, l = True):
            pm.system.loadPlugin("vrayformaya")


    # linking buttons to functions
    def createConnections(self):
        self.browse_btn.clicked.connect(self.browse)
        self.confirm_assign_btn.clicked.connect(self.createAssignMat)
        self.confirm_create_btn.clicked.connect(self.createMat)

    # open a browse dialog to specify texture file
    def browse(self):
        assetPath, fileExtensions = QtWidgets.QFileDialog.getOpenFileName(
            parent = self,
            dir = self.resourcePath,
            caption = 'Specify Texture',
            filter = 'Images (*.png *.jpg *.jpeg *.exr *.tif *.tiff)'
        )

        if assetPath:
            self.browse_input.setText(assetPath)

    # link to core
    def createMat(self):
        self.core.createMaterial(self.browse_input.text())

    # link to core
    def createAssignMat(self):
        self.core.createAssignMaterial(self.browse_input.text())

