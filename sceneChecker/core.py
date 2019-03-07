import pymel.core as pm
import os

'''
The core holds all functionality
'''
class Core():

    def __init__(self):
        self.noSubdivObjects = []
        self.noShadowObjects = []

    # check for proxy textures
    def checkProxyTextures(self):
        for f in pm.ls(type='file'):
            filepath = f.fileTextureName.get()
            if '256' in filepath or '512' in filepath:
                return False
        return True
        

    # search for opensubdivs
    def checkOpenSubdiv(self):
        noSubdivCount = 0
        self.noSubdivObjects = []

        for mesh in pm.ls(type='mesh'):
            if not mesh.hasAttr('vrayOsdSubdivEnable'):
                noSubdivCount += 1
                self.noSubdivObjects.append(mesh)

        return noSubdivCount

    # returns amount of aovs in scene
    def checkAOVs(self):
        aovCount = len(pm.ls(type='VRayRenderElement'))
        return aovCount

    # checks various render settings and raises exception if something is wrong
    def checkRenderSettings(self):
        globalSettings = pm.ls(type='renderGlobals')[0]
        resolution = globalSettings.resolution.get()
        # check resoltion
        if not resolution.width.get() == 1440 or not resolution.height.get() == 1080:
            raise Exception('Resolution not set correctly')

        vraySettings = pm.ls(type='VRaySettingsNode')[0]
        # check rendering quallity
        if not vraySettings.dmcThreshold.get() == 0.01:
            raise Exception('Rendering quality not set to 0.010')

        # check subdivision enabled
        if not vraySettings.globopt_subdivision.get():
            raise Exception('Subdivisions disabled')
        
        # check GI quality
        if not vraySettings.subdivs.get() == 1500:
            raise Exception('Gi subdivisions not set to 1500')

        # check number of lights for gi
        #if vraySettings.globopt_num_probabilistic_lights.get() < 15:
        #    raise Exception('Number of lights for gi set to lower than 15')

        # check if animation is enabled
        if vraySettings.animType.get() != 1:
            raise Exception('Animation not set to Standard')

        if vraySettings.globopt_probabilistic_lights_on.get() != 0:
            raise Exception('Light Evaluation not set to Full')

        # check if frame step is set to 1
        if globalSettings.byFrameStep.get() != 1:
            raise Exception('Frame Step not set to 1')

        # check if image format is set to exr multichannel
        if vraySettings.imageFormatStr.get() != 'exr (multichannel)':
            raise Exception('Image Format not set to exr (multichannel)')

        # check if filename prefix is set to correct scene
        if vraySettings.fileNamePrefix.get().split('/')[0][-2:] != pm.sceneName().basename().split('_')[1]:
            raise Exception('File Name Prefix not set correctly')

    def checkShadowCasting(self):
        self.noShadowObjects = []
        noShadowCounter = 0

        for mesh in pm.ls(type='mesh'):
            if not mesh.castsShadows.get(): 
                noShadowCounter += 1
                self.noShadowObjects.append(mesh.getParent())
        
        return noShadowCounter




    

