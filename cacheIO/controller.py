import pymel.core as pm
from PySide2 import QtWidgets, QtCore
import maya.OpenMayaUI as omui
from shiboken2 import wrapInstance
from PySide2 import QtWidgets, QtCore, QtGui
from maya.app.general.mayaMixin import MayaQWidgetDockableMixin

import cacheIO.core as core
import cacheIO.mainView as mainView


'''
Open with

import cacheIO.controller as cacheIOCtrl
cacheIOCtrl.open()
'''




# open function to wrap opening the ui into a small command
cacheIOUI = None
def open(develop = False, dockable = False, envVar = None):
    # load abc plugin
    if not pm.system.pluginInfo("AbcExport", q = True, l = True):
        pm.system.loadPlugin("AbcExport")
    if not pm.system.pluginInfo("AbcImport", q = True, l = True):
        pm.system.loadPlugin("AbcImport")
    if develop:
        reload(core)
        reload(mainView)

    try:
        cacheIOUI.close()
    except:
        pass

    cacheIOUI = Controller(envVar = envVar)
    cacheIOUI.show(dockable = dockable)


# wrapper to get mayas main window
def getMayaMainWindow():
    mayaPtr = omui.MQtUtil.mainWindow()
    return wrapInstance(long(mayaPtr), QtWidgets.QWidget)




'''
Main UI
This tool exports alembic caches and a json file with material info
and automatically reassigns materials on reimport
'''

class Controller(MayaQWidgetDockableMixin, QtWidgets.QMainWindow, mainView.Ui_cacheIO_mainWindow):

    def __init__(self, parent = getMayaMainWindow(), envVar = None):
        super(Controller, self).__init__(parent)

        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)

        self.core = core.Core()

        self.envVar = envVar

        self.setupUi(self)

        self.createConnections()

        self.fillSceneLevel()

        self.sceneLevel_list.viewport().installEventFilter(self)
        self.shotLevel_list.viewport().installEventFilter(self)



    def createConnections(self):
        self.exportSel_btn.clicked.connect(self.exportSelected)
        self.import_btn.clicked.connect(self.importSelectedCache)
        self.importAll_btn.clicked.connect(self.importAllCaches)

        self.sceneLevel_list.itemSelectionChanged.connect(self.fillShotLevel)
        self.sceneLevel_list.doubleClicked.connect(self.createFolder)
        self.shotLevel_list.itemSelectionChanged.connect(self.fillCacheLevel)
        self.cacheLevel_list.itemSelectionChanged.connect(self.fillNameLineEdit)
        self.export_name.textChanged.connect(self.toggleBtns)

    
    # ---------------
    # Connections
    # ---------------

    def exportSelected(self):
        currentScene = self.sceneLevel_list.currentItem().text()
        currentShot = self.shotLevel_list.currentItem().text()
        cacheName = self.export_name.text()
        dumbify = self.dumbify_chkBox.isChecked()
        history = self.history_chkBox.isChecked()
        self.core.exportSelected(currentScene, currentShot, cacheName, dumbify, history)
        self.fillCacheLevel()

    def importSelectedCache(self):
        currentScene = self.sceneLevel_list.currentItem().text()
        currentShot = self.shotLevel_list.currentItem().text()
        cacheName = self.export_name.text()
        self.core.importSelectedCache(currentScene, currentShot, cacheName, self.envVar)

    def importAllCaches(self):
        currentScene = self.sceneLevel_list.currentItem().text()
        currentShot = self.shotLevel_list.currentItem().text()
        self.core.importAllCache(currentScene, currentShot, self.envVar)

    def createFolder(self, scene = None):
        text, ok = QtWidgets.QInputDialog().getText(self, 'New Folder', 'Folder Name')
        if ok and text:
            self.core.createFolder(text, scene=scene)

        self.fillSceneLevel()


    # ---------------
    # UI refreshs
    # ---------------

    def fillSceneLevel(self):
        i = self.sceneLevel_list.currentIndex()
        self.sceneLevel_list.clear()
        for folder in self.core.getSceneLevelFolders():
            self.sceneLevel_list.addItem(folder)
        self.sceneLevel_list.setCurrentIndex(i)
        self.toggleBtns()

    def fillShotLevel(self):
        i = self.shotLevel_list.currentIndex()
        self.shotLevel_list.clear()
        currentScene = self.sceneLevel_list.currentItem().text()
        for folder in self.core.getShotLevelFolders(currentScene):
            self.shotLevel_list.addItem(folder)
        self.export_name.clear()
        self.shotLevel_list.setCurrentIndex(i)
        self.toggleBtns()

    def fillCacheLevel(self):
        self.cacheLevel_list.clear()
        try:
            currentScene = self.sceneLevel_list.currentItem().text()
            currentShot = self.shotLevel_list.currentItem().text()
            for cache in self.core.getCacheLevelItems(currentScene, currentShot):
                self.cacheLevel_list.addItem(cache)
        except:
            pass
        self.export_name.clear()
        self.toggleBtns()

    def fillNameLineEdit(self):
        self.export_name.setText(self.cacheLevel_list.currentItem().text())



    # ---------------
    # Event
    # somehow pressing shift makes the tool lose focus, this is the fix
    # ---------------
    
    def eventFilter(self, obj, event):
        if event.type() == QtCore.QEvent.MouseButtonDblClick:
            if obj.parent() == self.sceneLevel_list:
                self.createFolder()
                return True
            elif obj.parent() == self.shotLevel_list:
                self.createFolder(self.sceneLevel_list.currentItem().text())
                return True
        return False

    """Override keyPressEvent to keep focus on QWidget in Maya."""
    def keyPressEvent(self, event):
        if (event.modifiers() & QtCore.Qt.ShiftModifier):
            self.shift = True
            pass # make silent

    # ---------------
    # Utility
    # ---------------

    def toggleBtns(self):
        if (self.shotLevel_list.currentItem()
            and self.shotLevel_list.currentItem().text()):
            if self.export_name.text():
                self.exportSel_btn.setEnabled(True)
                self.import_btn.setEnabled(True)
            else:
                self.exportSel_btn.setEnabled(False)
                self.import_btn.setEnabled(False)
            self.importAll_btn.setEnabled(True)
        else:
            self.exportSel_btn.setEnabled(False)
            self.import_btn.setEnabled(False)
            self.importAll_btn.setEnabled(False)


    


    