import pymel.core as pm
import os


class Core():

    def __init__(self):
        self.workspacePath = pm.system.workspace.path
        self.cacheFolder = 'cache/IO'
        self.cachePath = os.path.join(self.workspacePath, self.cacheFolder)
        if not os.path.exists(self.cachePath):
            os.mkdir(self.cachePath)

    # exports selected objects to .ma and .abc
    # the main reason for the .ma is to keep the materials
    def exportSelected(self, scene, shot, filename, dumbify, history):
        # geo list is the one that will be exported
        geoList = []
        # dumbify set contains all geo under current selection
        dumbifySet = set()
        lightSet = set()

        selection = pm.selected()

        # add file node from displacements to selection. otherwise it will be ignored in export
        for obj in selection:
            if obj.type() =='VRayDisplacement' and obj.displacement.connections():
                selection.append(obj.displacement.connections()[0])

        if dumbify:
            # dumbify
            # this duplicates all geometry and links them with a blendshape.
            # the duplicates are moved to a seperate group and then cached.
            # this has the effect of removing any logic and just leaving geometry
            for sel in selection:
                for mesh in sel.getChildren(ad=True, type='mesh'):
                    if not mesh.intermediateObject.get() and self.visibleInHierarchy(mesh):
                        dumbifySet.add(mesh.getParent())
                for light in sel.getChildren(ad=True, type=['VRayLightSphereShape', 'VRayLightDomeShape', 'VRayLightRectShape','VRayLightIESShape', 'VRayLightMesh']):
                    lightSet.add(light.getParent())

            exportGrp = pm.group(em=True, name=filename+'_grp')
            geoGrp = pm.group(em=True, name='geoGrp')
            geoGrp.setParent(exportGrp)

            for obj in dumbifySet:
                dupli = pm.duplicate(obj)[0]
                for child in dupli.getChildren():
                    if not child.type() == 'mesh':
                        pm.delete(child)
                    elif child.hasAttr('intermediateObject') and child.intermediateObject.get():
                        pm.delete(child)
                dupli.setParent(geoGrp)
                # renaming the duplicate so it get's the namespace back
                dupli.rename(obj.nodeName())
                try:
                    pm.blendShape(self.getNonIntermediateShape(obj), self.getNonIntermediateShape(dupli), origin='world', n=dupli.nodeName()+'_bs', w=[0,1])
                except Exception as e:
                    print '%s throws %s'%(obj,e)
                # keep object sets for easy vray clipping
                inheritedSets = self.getInheritedSetMembership(obj)
                for s in inheritedSets:
                    if not pm.objExists(s.nodeName(stripNamespace=True)+'Export'):
                        newSet = pm.sets(em=True, n = s.nodeName(stripNamespace=True)+'Export')
                        geoList.append(newSet)
                    pm.sets(pm.PyNode(s.nodeName(stripNamespace=True)+'Export'), forceElement=dupli)

            if lightSet:
                lightGrp = pm.group(em=True, name='lightGrp')        
                lightGrp.setParent(exportGrp)
                for light in lightSet:
                    dupli = pm.duplicate(light)[0]                
                    dupli.setParent(lightGrp)
                    dupli.rename(light.nodeName())
                
            geoList.append(exportGrp)
        else:
            geoList = selection


        # export geo
        pm.select(geoList, r=True, ne=True)
        geoPath = pm.exportSelected(os.path.join(self.cachePath, scene, shot, filename+'.ma'), 
                typ='mayaAscii', 
                constructionHistory = history, 
                channels = False, 
                constraints = False, 
                expressions = False, 
                force =True, 
                shader = True,
                preserveReferences=False
                )
        self.removeStudentLic(geoPath)
        self.removeNamespaces(geoPath)


        # export abc
        abcOptions = []
        for sel in geoList:
            if 'dagNode' in sel.type(inherited=True):
                abcOptions.append('-root %s'%sel.fullPath())

        frameRange = [pm.playbackOptions(q=True, min=True), pm.playbackOptions(q=True, max=True)]
        abcOptions.append('-frameRange %s %s'%(frameRange[0], frameRange[1]))

        abcPath = os.path.join(self.cachePath, scene, shot, filename+'.abc')
        abcOptions.append('-file "' + abcPath.replace('\\', '/') + '"')
        abcOptions.append('-uvWrite')
        abcOptions.append('-wholeFrameGeo')
        abcOptions.append('-worldSpace')
        abcOptions.append('-writeVisibility')
        abcOptions.append('-writeCreases')
        abcOptions.append('-writeUVSets')
        abcOptions.append('-dataFormat ogawa')

        pm.AbcExport(verbose = True, jobArg = ' '.join(abcOptions))

        # cleanup
        if dumbify:
            for obj in geoList:
                pm.delete(obj)

    # imports the .ma file first and then drives it with the .abc cache
    def importSelectedCache(self, scene, shot, filename, envVar = None):
        # import geo
        try:
            pm.importFile(os.path.join(self.cachePath, scene, shot, filename +'.ma'), ra = False, mergeNamespacesOnClash = True, namespace = ':', returnNewNodes=True)
        except Exception as e:
            print e


        # clear intermediate objects
        for s in pm.ls(type='mesh'):
            if s.intermediateObject.get():
                pm.delete(s)

        # import abc
        try:
            abc = pm.PyNode(pm.AbcImport(os.path.join(self.cachePath, scene, shot, filename+'.abc'), mode = 'import', fitTimeRange=True, connect='/'))
        except Exception as e:
            print e
        
        if envVar:
            environmentPath = pm.util.getEnv(envVar)
            abc.abc_File.set(abc.abc_File.get().replace(environmentPath, '$'+envVar))


    def importAllCache(self, scene, shot, envVar = None):
        for cache in self.getCacheLevelItems(scene, shot):
            self.importSelectedCache(scene, shot, cache)




    # ---------------
    # Getters
    # ---------------

    def getSceneLevelFolders(self):
        return os.listdir(self.cachePath)

    def getShotLevelFolders(self, scene):
        try:
            return os.listdir(os.path.join(self.cachePath, scene))
        except:
            return []

    def getCacheLevelItems(self, scene, shot):
        try:
            fileSet = set()
            for f in os.listdir(os.path.join(self.cachePath, scene, shot)):
                if not '_mat' in f:
                    fileSet.add(f.split('.')[0])
            return fileSet
        except:
            return []
    
    def createFolder(self, name, scene = None):
        if scene: os.mkdir(os.path.join(self.cachePath, scene, name))
        else: os.mkdir(os.path.join(self.cachePath, name))
    
        


    # ---------------
    # UTILITY
    # ---------------

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
    # is probably some kind of maya bug
    # solution is a hack, but hey, it works
    def removeNamespaces(self, filePath):
        file = open(filePath, 'r')
        filedata = file.read()
        filedata = filedata.replace('":', '"')
        file = open(filePath, 'w')
        file.write(filedata)
        return filePath

    def getInheritedSetMembership(self, obj):
        sets = set()
        setList = obj.listSets()
        if setList:
            for s in setList:
                sets.add(s)
        while obj.getParent():
            obj = obj.getParent()
            setList = obj.listSets()
            if setList:
                for s in setList:
                    sets.add(s)
        return sets

    def visibleInHierarchy(self, obj):
        v = obj.v.get()
        if not v: return v
        for p in obj.getAllParents():
            v = p.v.get()
            if not v: return v
        return v

    def getNonIntermediateShape(self, obj):
        for shape in obj.getShapes():
            if not shape.intermediateObject.get():
                return shape

    



'''
LEGACY
        # fill shader list
        # limitation if one shader drives multiple shader grps
        pm.hyperShade(shaderNetworksSelectMaterialNodes=True)
        for shd in pm.selected(materials=True):
            if [c for c in shd.classification() if 'shader/surface' in c]:
                shaderList.add(shd)

        # export materials
        pm.select(shaderList, r =True)
        self.removeStudentLic(
            pm.exportSelected(
                os.path.join(self.cachePath, scene, shot, filename+'_mat.ma'),
                type='mayaAscii',
                force = True,
                constructionHistory = True, 
                shader = True
            )
        )

        # connect with materialMaster
        materialMaster = pm.createNode('simpleTestNode', name = 'materialMaster')

        for shd in shaderList:
            pm.select(shd, r=True)
            pm.hyperShade(objects='')
            attrName=shd.nodeName().replace(':', '___')
            if not materialMaster.hasAttr(attrName):
                materialMaster.addAttr(attrName, type='message')
            for obj in pm.selected():
                try:
                    if not obj.hasAttr('mtl'):
                        obj.addAttr('mtl', type='message')
                    materialMaster.attr(attrName) >> obj.mtl
                except: pass
'''