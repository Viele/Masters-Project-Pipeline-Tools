import pymel.core as pm
import os
from collections import deque
from datetime import datetime





# -----------------------------
# ASSET IO WORKING CLASS
# this class handles the library management
# export and import functions
# and path management
# -----------------------------
class AssetIOCore(object):
    # -----------------------------
    # INIT
    # the script always works on the current maya project
    # by default it creates a folder 'library' where all assets are exported to
    # changing this folder in ui is not currently supported
    # -----------------------------
    def __init__(self):
        self.workspacePath = pm.system.workspace.path
        self.libraryFolder = 'library'
        self.checkPath(os.path.join(self.workspacePath, self.libraryFolder))
        self.libraryPath = os.path.join(self.workspacePath, self.libraryFolder)









    # -----------------------------
    # EXPORT A NEW ASSET
    # by default it exports the whole scene.
    # pass parameter tpye = 'selected' for selection only
    # -----------------------------
    def export(self,**kwargs):
        # the category is just a folder below the library path
        assetCategory = kwargs.setdefault('assetCategory', 'default')

        # if no name is specified it uses the scene name
        assetName = kwargs.setdefault('assetName', pm.sceneName().basename()[:-3])

        # an asset can have a .txt file associated with it. This should
        # help to clarify the contents of an asset
        assetDescription = kwargs.setdefault('assetDescription')

        # by default the exportAll command is called
        exportType = kwargs.setdefault('type', 'all')

        # if true automatically sets the camera to frame the exported objs
        autoFrame = kwargs.setdefault('autoFrame', True)

        breakRef = kwargs.setdefault('breakRef', False)


        # if the scene was not saved it has no name
        if assetName == '':
            raise Exception('Asset Name not specified')
        
        if exportType == 'selected' and not pm.selected():
            # if nothing is selected, stop the execution here
            raise Exception('Nothing Selected')
        
        # create the folders if they don't exist
        self.checkPath(os.path.join(self.libraryPath, assetCategory))
        assetPath = os.path.join(self.libraryPath, assetCategory, assetName)
        self.checkPath(assetPath)

        # save the selection now because enableIsolateSelect clears it
        selection = pm.selected()
        mpanel = pm.paneLayout('viewPanes', q = True, pane1=True)
        # disable selection highlighting and wireframe on shaded
        wireframeOnShadedState = pm.windows.modelEditor(mpanel, q = True, wireframeOnShaded = True)
        pm.windows.modelEditor(mpanel, e = True, sel = False, wireframeOnShaded = False)
        # set background color
        originalBackgroundColor = pm.general.displayRGBColor('background', q=True)
        pm.general.displayRGBColor('background', 0.3, 0.3, 0.3)
        # set the camera
        cam = pm.ls(pm.modelPanel(mpanel, q=True, cam=True), type='transform')[0]
        if autoFrame:
            wTrans = cam.getTranslation(ws=True)
            wRot = cam.getRotation(ws=True)
            try:
                cam.rx.set(-10)
                cam.ry.set(30)
                pm.viewFit()
            except:
                pass

        pm.general.refresh()

        if exportType == 'selected':
            # hide everything that is not selected for the playblast
            pm.mel.eval('enableIsolateSelect %s %d' %(mpanel, 1))

        # RENDER ICON
        # this is a simple playblast of the current frame
        # image is saved as .jpg with an _icon suffix
        pm.animation.playblast(
            cf = assetPath + '/' + assetName + '_icon.jpg', 
            format = 'image', 
            compression = 'jpg', 
            widthHeight = [128,128], 
            frame = [pm.animation.currentTime()],
            orn = False,
            os = True,
            v = False,
            percent = 100
            )
        if autoFrame:
            try:
                # reset camera
                cam.setTranslation(wTrans, ws=True)
                cam.setRotation(wRot, ws=True)
            except:
                pass

        if exportType == 'selected':
            # show the scene again. the user shouldn't notice
            pm.mel.eval('enableIsolateSelect %s %d' %(mpanel, 0))
        
        # reenable selection highlighting and reset wireframe on shaded to what it was before
        pm.windows.modelEditor(mpanel, e = True, sel = True, wireframeOnShaded = wireframeOnShadedState)

        #reset the background color to what it was before
        pm.general.displayRGBColor('background', 
            originalBackgroundColor[0],
            originalBackgroundColor[1],
            originalBackgroundColor[2]
        )
        
        # EXPORT FILE
        # reselect the selection, isolate select clears it.
        pm.select(selection)
        if exportType == 'all':
            self.fixNamespaces(
                self.removeStudentLic(
                    pm.system.exportAll(
                        assetPath + '/' + assetName + '.ma', 
                        preserveReferences= not breakRef, 
                        force=True
                    )
                )
            )
        if exportType == 'selected':
            self.fixNamespaces(
                self.removeStudentLic(
                    pm.system.exportSelected(
                        assetPath + '/' + assetName + '.ma', 
                        preserveReferences= not breakRef, 
                        force=True
                    )
                )
            )

        # SAVE DESCRIPTION
        # newlines are saved
        if assetDescription:
            text_file = open(assetPath + '/' + assetName + '.txt', 'wt')
            text_file.write(assetDescription.encode('utf8'))
            text_file.close()

        







    # -----------------------------
    # REFERENCE AN EXISTING ASSET
    # create a reference to an existing asset in the library
    # by default the project path is replaced with an environment variable
    # this cannot be changed in the ui for now
    # -----------------------------
    def reference(self, **kwargs):
        assetCategory = kwargs.setdefault('assetCategory')
        assetName = kwargs.setdefault('assetName')
        environmentVariable = kwargs.setdefault('environmentVariable', None)
        groupLocator = kwargs.setdefault('groupLocator', True)
        selectable = kwargs.setdefault('selectable', False)

        if not assetCategory or assetCategory == '-':
            raise Exception('No asset specified')
        if not assetName or assetName == '-':
            raise Exception('No asset specified')
        
        # build the reference Path and check if this asset exists
        referencePath = absolutePath = os.path.join(self.workspacePath, self.libraryFolder, assetCategory, assetName)

        if environmentVariable:
            referencePath = absolutePath.replace(self.workspacePath, environmentVariable)
            print referencePath

        if not os.path.exists(absolutePath):
            raise Exception ('Asset %s does not exist' %absolutePath)

        # check namespaces
        if not pm.system.namespace(exists=assetCategory):
            pm.system.namespace(add=assetCategory)

        if not pm.system.namespace(exists=assetCategory + ':' + assetName):
            pm.system.namespace(add=assetCategory + ':' + assetName)

        # multiple references are supported, namespace is incremented by 1 every time
        namespace = ':' + assetCategory + ':' + assetName + ':' + 'r%s'%1
        count = 1
        while pm.system.namespace(exists=namespace, r = True):
            count += 1
            namespace = ':' + assetCategory + ':' + assetName + ':' + ('r%s'%count)

        # create the reference
        newNodes = pm.system.createReference(
            referencePath + '/' + assetName + '.ma', 
            namespace = namespace, 
            groupReference = groupLocator, 
            groupLocator = groupLocator,
            returnNewNodes = True,
            shd = 'shadingNetworks'
        )
        
        refNode = pm.referenceQuery(newNodes[0], rfn = True, tr = True)
        refNode = pm.ls(refNode)[0]

        # rename the annotation and the top locator
        if groupLocator:
            annotationNode = pm.ls(newNodes, type = 'annotationShape')[0]
            annotationNode.getParent().v.set(False)
            pm.setAttr(annotationNode.text, assetName)
            pm.rename(annotationNode.root(), namespace + ':srt')
            annotationNode.root().lsx.set(10)
            annotationNode.root().lsy.set(10)
            annotationNode.root().lsz.set(10)

            # set the group transform to reference 
            # so the contents can't be selected by accident
            if(not selectable):
                topTransforms = pm.listRelatives(annotationNode.root(), type = 'transform')
                for transform in topTransforms:
                    pm.setAttr(transform.overrideEnabled, True)
                    pm.setAttr(transform.overrideDisplayType, 2)

        return newNodes






    # -----------------------------
    # IMPORT AN EXISTING ASSET
    # -----------------------------
    def importAsset(self, **kwargs):
        assetCategory = kwargs.setdefault('assetCategory')
        assetName = kwargs.setdefault('assetName')
        namespace = kwargs.setdefault('namespace', 'asset')

        if not assetCategory:
            pm.system.error('No category specified')
        if not assetName:
            pm.system.error('No asset specified')

        importPath = os.path.join(self.libraryPath, assetCategory, assetName, (assetName + '.ma'))

        if not os.path.exists(importPath):
            raise Exception ('Asset %s does not exist' %importPath)

        pm.system.importFile(importPath)
        














    # -----------------------------
    # GETTERS / SETTERS
    # functions called from outside
    # for getting information or updating existing info
    # -----------------------------

    def updateWorkspacePath(self):
        self.workspacePath = pm.system.workspace.path
        self.checkPath(os.path.join(self.workspacePath, self.libraryFolder))
        self.libraryPath = os.path.join(self.workspacePath, self.libraryFolder)

    def updateLibraryFolder(self, library):
        self.libraryFolder = library
        self.checkPath(os.path.join(self.workspacePath, self.libraryFolder))
        self.libraryPath = os.path.join(self.workspacePath, self.libraryFolder)

    def getLibraryPath(self):
        return self.libraryPath

    # add the given category as a folder to the library path
    def addCategory(self, category):
        os.mkdir(os.path.join(self.workspacePath, self.libraryFolder, category))

    # returns all folders in the library folder
    def getCategories(self):
        return self.listFolders(self.libraryPath)

    def getAssets(self):
        categories = self.getCategories()
        assets = []
        for category in categories:
            assetFolders = self.listFolders(os.path.join(self.libraryPath, category))
            if assetFolders:
                for asset in assetFolders:
                    assets.append('|'.join([asset, category]))

        return assets


    def getAssetDescription(self, category, asset):
        assetPath = os.path.join(self.libraryPath, category, asset)
        if not os.path.exists(assetPath):
            raise Exception('Asset %s in Category %s does not exist' %(asset, category))

        descriptionPath = assetPath + '/' + asset + '.txt'

        if not os.path.exists(descriptionPath):
            return '-'

        description = ''
        with open(descriptionPath, 'r') as assetDescrFile:
            description = assetDescrFile.read()

        return description

    # returns a formatted string  of the date the asset was last modified
    def getAssetLastModified(self, category, asset):
        assetPath = os.path.join(self.libraryPath, category, asset)
        if not os.path.exists(assetPath):
            raise Exception('Asset %s in Category %s does not exist' %(asset, category))

        mayaFilePath = assetPath + '/' + asset + '.ma'

        return datetime.fromtimestamp(os.path.getmtime(mayaFilePath)).strftime('%d-%m-%Y %H:%M')


    def getAssetIconPath(self, category, asset):
        assetPath = os.path.join(self.libraryPath, category, asset)
        if not os.path.exists(assetPath):
            raise Exception('Asset %s in Category %s does not exist' %(asset, category))

        iconPath = assetPath + '/' + asset + '_icon.jpg'

        if not os.path.exists(iconPath):
            return ''

        return iconPath
        

    # true if the folder for this asset exists
    def assetExists(self, category, asset):
        assetPath = os.path.join(self.libraryPath, category, asset)
        return os.path.exists(assetPath)


    def getAssetInfoFromPath(self,path):
        if not os.path.exists(os.path.join(path, (os.path.split(path)[1]+'.ma') )):
            raise Exception('Specified folder is not an Asset!')

        assetInfo = dict()
        path, assetInfo['name'] = os.path.split(path)
        path, assetInfo['category'] = os.path.split(path)
        assetInfo['description'] = self.getAssetDescription(assetInfo['category'], assetInfo['name'])

        return assetInfo


    # returns a dict containing info about the references in the scene
    def getReferenceInfo(self):
        referencesInfo = {}
        for ref in pm.ls(rf=True):
            # filtering out non top level refs
            try:
                if not pm.referenceQuery(ref, rfn=True, p=True) is None:
                    continue
            except:
                continue

            self.recursiveRefInfo(ref, referencesInfo)

        return referencesInfo

    
    def recursiveRefInfo(self, targetRef, parentDict):
        refInfo = {}

        assetName = targetRef.namespace().split(':')[-2]

        # if an object with that name exists multiple times only add the node
        if parentDict.has_key(assetName):
            parentDict[assetName]['nodes'].append(targetRef)
            return


        refInfo['name'] = assetName
        # get visibility
        refLoc = self.getReferenceLocator(targetRef)
        if refLoc:
            refInfo['visibility'] = refLoc.visibility.get()

            # get label visibility
            refInfo['annotation'] = self.findLabel(refLoc).visibility.get()

        refInfo['nodes'] = [targetRef]

        refInfo['children'] = {}
        childRefs = pm.referenceQuery(targetRef, rfn=True, ch=True)

        # if there are no child references return
        if childRefs:
            for childRef in childRefs:
                childRef = pm.PyNode(childRef)
                self.recursiveRefInfo(childRef, refInfo['children'])

        parentDict[assetName] = refInfo


    # remove a reference and delete all nodes from the namespace
    def deleteAsset(self, refNodes):
        namespace = refNodes[0].associatedNamespace(baseName = False)
        
        for ref in refNodes:
            pm.FileReference(ref).remove()

        # remove the namespace and any nodes that may still exist in it
        if pm.namespace(exists = namespace):
            pm.namespace(dnc = True, rm = namespace)

    def deleteSelReference(self):
        for sel in pm.selected():
            refNode = self.getReferenceNodeFromObject(sel)

            if refNode:
                pm.FileReference(refNode).remove()

    def duplicateSelReference(self):
        for sel in pm.selected():
            refNode = self.getReferenceNodeFromObject(sel)

            if refNode:
                namespaceTokens = refNode.name().split(':')
                refLoc = self.getReferenceLocator(refNode)
                selectable = False
                if refLoc:
                    selectable = refLoc.getChildren(type='transform')[0].overrideEnabled.get()

                self.reference(
                    assetCategory=namespaceTokens[0],
                    assetName = namespaceTokens[1],
                    groupLocator = not refLoc is None,
                    selectable = not selectable)

                if refLoc:
                    newRefLoc = pm.selected()[0]
                    newRefLoc.setMatrix(refLoc.getMatrix(ws=True), ws=True)


    # toggle visibility of a reference and all of its instances
    def setVisibility(self, refNodes, value):
        referenceLocators = self.getReferenceLocators(refNodes)
        
        for loc in referenceLocators:
            loc.visibility.set(not value)

    # toggles the visibility of the labels of the given asset
    def toggleLabel(self, refNodes, value):
        referenceLocators = self.getReferenceLocators(refNodes)
        for loc in referenceLocators:
            label = self.findLabel(loc)
            if label:
                label.visibility.set(not value)

















    # -----------------------------
    # HELPER FUNCTIONS
    # various functions used in class for avoiding code duplis
    # -----------------------------

    # used throughout the proxect to make sure a path exists
    # here the path is created if it doesn't
    def checkPath(self, path):
        if not os.path.exists(path):
            os.mkdir(path)


    # helper function that opens a maya ascii file and replaces the student
    # license line
    def removeStudentLic(self, filePath):
        file = open(filePath, 'r')
        filedata = file.read()
        filedata = filedata.replace('fileInfo "license" "student";', '')
        file = open(filePath, 'w')
        file.write(filedata)
        return filePath


    # remove leading ':' because they are a problem sometimes 
    def fixNamespaces(self, filePath):
        file = open(filePath, 'r')
        filedata = file.read()
        filedata = filedata.replace('":', '"')
        file = open(filePath, 'w')
        file.write(filedata)
        return filePath



    # os.listdir also returns files
    # this returns only folders
    def listFolders(self, path):
        if os.path.isdir(path):
            allFiles = os.listdir(path)
            directories = []
            for item in allFiles:
                if os.path.isdir(os.path.join(path, item)):
                    directories.append(item)
            return directories

        else:
            raise Exception('Path %s does not exit' %path)

    # return the locator that is on top of the reference
    def getReferenceLocator(self, refNode):
        associatedNodes = []
        associatedNodes.extend(pm.listConnections(
                refNode.associatedNode
                )
            )

        for node in associatedNodes:
            if node.getShape() and node.getShape().type() == 'locator':
                return node

    # same as getReferenceLocator but operates on multiple refNodes
    def getReferenceLocators(self, refNodes):
        locators = []
        for shape in pm.ls(refNodes[0].namespace() + '*:*', type = 'locator'):
            locators.append(shape.getParent())

        return locators

    # returns the label of the given reference locator
    # try except because for some reason there is a NoneType somewhere
    def findLabel(self, referenceLocator):
        for child in referenceLocator.getChildren():
            try:
                if child.getShape().type() == 'annotationShape':
                    return child
            except:
                pass
        return None

    def getReferenceNodeFromObject(self, obj):
        refNodeName = None
        refNode = None
        try: refNodeName = pm.referenceQuery(obj, rfn = True, tr = True)
        except: 
            if obj: refNodeName = obj.namespace()[:-1]+'RN'


        if refNodeName: refNode = pm.ls(refNodeName)[0]

        return refNode

    def listBreadthFirst(self, root):
        objList = []
        traversalQueue = deque()
        traversalQueue.append(root)
        while len(traversalQueue) > 0:
            obj = traversalQueue.popleft()
            if obj.getChildren():
                objList.extend(obj.getChildren())
                traversalQueue.extend(obj.getChildren())
                
        return objList
