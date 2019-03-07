import pymel.core as pm
import os
import assetIO.assetIOCore as assetIOCore
import assetIO.assetIOWidget as assetIOWidget
import assetIO.assetIOManageAssetWidget as assetIOManageAssetWidget
from PySide2 import QtWidgets, QtCore, QtGui
import maya.OpenMayaUI as omui
from shiboken2 import wrapInstance
import collections


'''
Open with

import pymel.core as pm
import assetIO.assetIOWindow as assetIOWindow
import assetIO.assetIOCore as assetIOCore

if __name__ == "__main__":
    try:
        assetIOWindow.close()
    except:
        pass

    assetIOWindow = assetIOWindow.AssetIOWindow(envVar="???")
    assetIOWindow.show()
    
'''
# wrapper to get mayas main window
def getMayaMainWindow():
    mayaPtr = omui.MQtUtil.mainWindow()
    return wrapInstance(long(mayaPtr), QtWidgets.QWidget)


# -----------------------------
# ASSET IO MAIN UI
# This class creates connections between UI and CORE
# -----------------------------
class AssetIOWindow(QtWidgets.QMainWindow, assetIOWidget.Ui_AssetIO):

    def __init__(self, envVar = None, parent = getMayaMainWindow()):
        super(AssetIOWindow, self).__init__(parent)
        
        self.envVar = envVar

        # this calls the compiled ui and creates the layout
        self.setupUi(self)

        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)

        # load the plugins if the are not already loaded
        if not pm.system.pluginInfo("AbcExport", q = True, l = True):
            pm.system.loadPlugin("AbcExport")
        if not pm.system.pluginInfo("AbcImport", q = True, l = True):
            pm.system.loadPlugin("AbcImport")
        if not pm.system.pluginInfo("gpuCache", q = True, l = True):
            pm.system.loadPlugin("gpuCache")

        # this instance has the core functionality
        self.assetIOCore = assetIOCore.AssetIOCore()

        # categories and assets are saved for faster access
        # asset list is a dict with a category as key to an asset list
        self.categoryList = []
        self.assetList = []

        # get the categories
        self.refreshCategoryList()

        # fill the category combo boxes
        self.updateCategoryCBox()

        # connect the buttons to functions
        self.createConnections()




    def createConnections(self):
        self.assetIO_tabWidget.currentChanged.connect(self.updateTabContents)

        self.exportAssetName_browseButton.clicked.connect(self.browseAssets)
        self.exportCategory_CB.currentIndexChanged.connect(self.categoryChanged)
        self.exportCategoryAdd_button.clicked.connect(self.addCategory)
        self.exportAll_button.clicked.connect(lambda: self.prepareExport(type = 'all'))
        self.exportSelected_button.clicked.connect(lambda: self.prepareExport(type = 'selected'))

        self.importCategory_cBox.currentIndexChanged.connect(self.updateAssetList)
        self.importSearch_lineEdit.textChanged.connect(self.updateAssetList)
        self.importList.currentItemChanged.connect(self.updateAssetProperties)
        self.importReference_button.clicked.connect(lambda: self.prepareImport(type = 'reference'))
        self.importImport_button.clicked.connect(lambda: self.prepareImport(type = 'import'))
        self.importProperties_locator_checkbox.stateChanged.connect(
            lambda: self.importProperties_selectable_checkbox.setEnabled(self.importProperties_locator_checkbox.isChecked())
        )

        self.manage_deleteSel_btn.clicked.connect(self.deleteSelReference)
        self.manage_duplicateSel_btn.clicked.connect(self.duplicateSelReference)


    # open a text dialog window and then send the name to the core
    # refresh afterwards
    def addCategory(self):
        text, ok = QtWidgets.QInputDialog.getText(self, 'Add Category', 'Category Name: ')
        if ok:
            self.assetIOCore.addCategory(text)
        self.refreshCategoryList()

    def categoryChanged(self):
        if self.exportCategory_CB.currentText() == 'env':
            self.export_breakRef_chkbox.setChecked(True)
            self.exportFrameSel_checkbox.setChecked(False)
        else:
            self.export_breakRef_chkbox.setChecked(False)
            self.exportFrameSel_checkbox.setChecked(True)


    # get all the properties set for export
    def prepareExport(self, **kwargs):
        exportType = kwargs.setdefault('type', 'all')
        assetName = self.exportAssetName_input.text()
        assetCategory = self.exportCategory_CB.currentText()
        assetDescription = str(self.exportDescription_textEdit.toPlainText())
        autoFrame = self.exportFrameSel_checkbox.isChecked()
        breakRef = self.export_breakRef_chkbox.isChecked()
        

        # tell the user if the asset already exists, and ask him if he wants to overwrite
        if self.assetIOCore.assetExists(assetCategory, assetName):
            msg = QtWidgets.QMessageBox()
            msg.setWindowTitle('Asset exists!')
            msg.setText('The specified Asset already exists. Overwrite?')
            msg.setStandardButtons(QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.Cancel)
            msgVal = msg.exec_()
            if msgVal == QtWidgets.QMessageBox.Cancel:
                return

       
        try:
            self.assetIOCore.export(
                assetName = assetName,
                assetCategory = assetCategory,
                assetDescription = assetDescription,
                type = exportType,
                autoFrame = autoFrame,
                breakRef = breakRef
            )
        except Exception, e: 
            pm.system.displayError(e)

    # get all properties for import
    def prepareImport(self, **kwargs):
        importType = kwargs.setdefault('type', 'reference')
        assetCategory = self.importPropertiesCategory_display.text()
        assetName = self.importPropertiesName_display.text()
        groupLocator = self.importProperties_locator_checkbox.isChecked()
        selectable = self.importProperties_selectable_checkbox.isChecked()

        try:
            if importType == 'reference':
                self.assetIOCore.reference(
                    assetCategory = assetCategory, 
                    assetName = assetName,
                    groupLocator = groupLocator,
                    selectable = selectable,
                    environmentVariable = self.envVar
                    )

            if importType == 'import':
                self.assetIOCore.importAsset(
                    assetCategory = assetCategory,
                    assetName = assetName
                )
        except Exception, e:
            pm.system.displayError(e)

    # open a file browser and fill the export tab with the info of the selected asset
    def browseAssets(self):
        assetPath = QtWidgets.QFileDialog.getExistingDirectory(
            parent = self, 
            dir = self.assetIOCore.getLibraryPath(), 
            caption = 'Specify Asset')

        if assetPath:
            try:
                assetInfo = self.assetIOCore.getAssetInfoFromPath(assetPath)
                self.exportAssetName_input.setText(assetInfo['name'])
                self.exportCategory_CB.setCurrentIndex(self.exportCategory_CB.findText(assetInfo['category']))
                self.exportDescription_textEdit.setText(assetInfo['description'])
            except Exception, e:
                pm.system.displayError(e)
            
        


    # gets a list of all categories
    def refreshCategoryList(self):
        self.categoryList = self.assetIOCore.getCategories()
        self.updateCategoryCBox()


    # gets a list of all assets
    def updateTabContents(self, tab):
        if tab == 1:
            self.assetList = self.assetIOCore.getAssets()
            self.updateAssetList()
            self.importSearch_lineEdit.setFocus()

        if tab == 2:
            self.updateReferenceObjectList()

    # updates the contents of the category combo boxes
    def updateCategoryCBox(self):
        self.exportCategory_CB.clear()
        self.importCategory_cBox.clear()
        self.importCategory_cBox.addItem('off')
        for category in self.categoryList:
            self.exportCategory_CB.addItem(category)
            self.importCategory_cBox.addItem(category)

    # updates the content of the asset list in the import tab
    # also applies filters to it
    def updateAssetList(self):
        stringFilter = self.importSearch_lineEdit.text()
        categoryFilter = self.importCategory_cBox.currentText()
        self.importList.clear()

        filteredAssetList = []

        # apply category filter
        if not categoryFilter == 'off':
            for asset in self.assetList:
                if asset.split('|')[1] == categoryFilter:
                    filteredAssetList.append(asset)
        else:
            filteredAssetList = self.assetList


        # apply string filter
        if stringFilter != '':
            filteredAssetList = [x for x in filteredAssetList if stringFilter in x]
        
        if filteredAssetList:
            for asset in sorted(filteredAssetList):
                listItem = QtWidgets.QListWidgetItem(str(asset.split('|')[0]))
                listItem.setData(QtCore.Qt.UserRole, asset.split('|')[1])
                self.importList.addItem(listItem)


    # fills the properties area in the import tab
    # sets icon, name, category and description
    def updateAssetProperties(self, item):
        if item:
            assetName = item.text()
            assetCategory = item.data(QtCore.Qt.UserRole)
            description = self.assetIOCore.getAssetDescription(assetCategory, assetName)
            iconPath = self.assetIOCore.getAssetIconPath(assetCategory, assetName)
            lastModified = self.assetIOCore.getAssetLastModified(assetCategory, assetName)
            
            self.importPropertiesName_display.setText(assetName)
            self.importPropertiesCategory_display.setText(assetCategory)
            self.importPropertiesDescription_textEdit.setText(description)
            self.importProperties_icon.setPixmap(iconPath)
            self.importProperties_locator_checkbox.setChecked(assetCategory != 'rigs')
            self.importProperties_selectable_checkbox.setEnabled(self.importProperties_locator_checkbox.isChecked())
            self.importProperties_selectable_checkbox.setChecked(False)
            self.importPropertiesMod_display.setText(lastModified)

    # update the list on the manage tab
    def updateReferenceObjectList(self):
        # clear list
        self.manage_referenceObjects_list.clear()

        # get reference objects
        referenceInfo = self.assetIOCore.getReferenceInfo()

        # for each one add an entry
        for ref in referenceInfo.values():
            self.buildRecursiveObjectList(ref)

            

    def buildRecursiveObjectList(self, ref, child = False):
        item = QtWidgets.QListWidgetItem()
        assetWidget = AssetIOManageAssetWidget(ref['nodes'])
        # set the name
        assetWidget.manage_assetName.setText(ref['name'])
        assetWidget.manage_instanceCount_display.setText('%s'%len(ref['nodes']))

        path = os.path.dirname(os.path.abspath(__file__))

        if ref.has_key('visibility'):
            assetWidget.manage_visibility_button.setChecked(not ref['visibility'])
            assetWidget.manage_annotationVisibility_button.setChecked(not ref['annotation'])
        else:
            assetWidget.manage_visibility_button.setEnabled(False)
            assetWidget.manage_annotationVisibility_button.setEnabled(False)
            assetWidget.manage_reference_button.setEnabled(False)

        # set icons
        # paper bin icon
        icon = QtGui.QIcon()
        icon.addPixmap(os.path.join(path, 'icons/deleteAsset.png'))
        assetWidget.manage_delete_button.setIcon(icon)

        # visibility icon
        icon = QtGui.QIcon()
        icon.addPixmap(os.path.join(path,'icons/visible.png'))
        icon.addPixmap(os.path.join(path,'icons/invisible.png'), QtGui.QIcon.Normal, QtGui.QIcon.On)
        assetWidget.manage_visibility_button.setIcon(icon)

        # label icon
        icon = QtGui.QIcon()
        icon.addPixmap(os.path.join(path,'icons/label.png'))
        icon.addPixmap(os.path.join(path,'icons/nolabel.png'), QtGui.QIcon.Normal, QtGui.QIcon.On)
        assetWidget.manage_annotationVisibility_button.setIcon(icon)


        # set size to make widget fit
        item.setSizeHint(assetWidget.sizeHint())
        self.manage_referenceObjects_list.addItem(item)
        self.manage_referenceObjects_list.setItemWidget(item, assetWidget)

        # create Connections
        assetWidget.manage_delete_button.clicked.connect(self.deleteReference)
        assetWidget.manage_visibility_button.clicked.connect(self.toggleVisibility)
        assetWidget.manage_reference_button.clicked.connect(self.duplicateReference)
        assetWidget.manage_annotationVisibility_button.clicked.connect(self.toggleLabel)

        if child:
            assetWidget.manage_delete_button.deleteLater()
            assetWidget.manage_delete_button = None
            spaceLabel = QtWidgets.QLabel('-')
            assetWidget.manage_widget_layout.insertWidget(0, spaceLabel)

        for child in ref['children'].values():
            self.buildRecursiveObjectList(child, child=True)


    def deleteReference(self):
        msg = QtWidgets.QMessageBox()
        msg.setWindowTitle('Delete Reference?')
        msg.setText('Deleting the Reference is not undoable!')
        msg.setStandardButtons(QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.Cancel)
        msgVal = msg.exec_()
        if msgVal == QtWidgets.QMessageBox.Cancel:
            return

        self.assetIOCore.deleteAsset(
            self.sender().parent().refNodes
        )
        self.updateReferenceObjectList()

    def deleteSelReference(self):
        self.assetIOCore.deleteSelReference()
        self.updateReferenceObjectList()
    
    def toggleVisibility(self):
        self.assetIOCore.setVisibility(
            self.sender().parent().refNodes,
            self.sender().isChecked()
        )

    def toggleLabel(self):
        self.assetIOCore.toggleLabel(
            self.sender().parent().refNodes,
            self.sender().isChecked()
        )

    def duplicateReference(self):
        refNode = self.sender().parent().refNodes[0]
        namespaces = refNode.namespace().split(':')
        self.assetIOCore.reference(
            assetCategory = namespaces[-3],
            assetName = namespaces[-2]
        )
        self.updateReferenceObjectList()

    def duplicateSelReference(self):
        self.assetIOCore.duplicateSelReference()
        self.updateReferenceObjectList()

    
    """Override keyPressEvent to keep focus on QWidget in Maya."""
    def keyPressEvent(self, event):
        if (event.modifiers() & QtCore.Qt.ShiftModifier):
            self.shift = True
            pass # make silent
            





# -----------------------------
# ASSET MANAGE WIDGET
# This class is instanced into the list on the manage tab
# -----------------------------
class AssetIOManageAssetWidget(QtWidgets.QWidget,assetIOManageAssetWidget.Ui_manage_widget):
    def __init__(self, refNodes, parent = getMayaMainWindow()):
        super(AssetIOManageAssetWidget, self).__init__(parent)
        
        # this calls the compiled ui and creates the layout
        self.setupUi(self)
        self.refNodes = refNodes


        



        