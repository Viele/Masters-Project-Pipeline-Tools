import pymel.core as pm
import os

'''
The core holds all functionality
'''
class Core():

    def __init__(self, envVar):
        self.envVar = envVar

    # called from ui
    def createMaterial(self, assetPath):
        self.fileTokens = os.path.basename(assetPath).split('.')
        filename  = self.fileTokens[0] 
        extension = '.'.join(self.fileTokens[1:])
        self.dirname = os.path.dirname(assetPath)

        # the script also sets an environment variable
        environmentPath = pm.util.getEnv(self.envVar)
        if environmentPath:
            self.envDirname = self.dirname.replace(environmentPath, '${%s}'%self.envVar)

        tokens = filename.split('_')
        self.baseFilename = '_'.join(tokens[0:-1])
        
        # CREATE MATERIAL
        mat = pm.shadingNode('VRayMtl', asShader = True, name = '%s_mat'%self.baseFilename)
        shGrp = pm.sets(renderable=True, noSurfaceShader=True, empty=True, name="%sSG"%self.baseFilename)
        mat.outColor >> shGrp.surfaceShader

        # CREATE AND CONNECT TEXTURES
        # each block creates first the path, then the file node and links it to the correct
        # input of the material
        # note that the colorspace must be set each time
        textureName = '_'.join((self.baseFilename, 'Diffuse'))+ '.' + extension
        try:
            tex = self.createTextureNode(textureName, 'diffuse')
            tex.outColor >> mat.color
        except Exception as e:
            print e

        textureName = '_'.join((self.baseFilename, 'Reflection'))+ '.' + extension
        try:
            tex = self.createTextureNode(textureName, 'reflection')
            tex.outColor >> mat.reflectionColor
        except Exception as e:
            print e

        textureName = '_'.join((self.baseFilename, 'Glossiness'))+ '.' + extension
        try:
            tex = self.createTextureNode(textureName, 'glossiness')
            tex.outAlpha >> mat.reflectionGlossiness
            tex.colorSpace.set('Raw')
        except Exception as e:
            print e

        textureName = '_'.join((self.baseFilename, 'ior'))+ '.' + extension
        try:
            tex = self.createTextureNode(textureName, 'ior')
            tex.outAlpha >> mat.fresnelIOR
            tex.colorSpace.set('Raw')
            mat.lockFresnelIORToRefractionIOR.set(0)
        except Exception as e:
            print e

        textureName = '_'.join((self.baseFilename, 'Normal'))+ '.' + extension
        try:
            tex = self.createTextureNode(textureName, 'normal')
            tex.outColor >> mat.bumpMap
            tex.colorSpace.set('Raw')
            mat.bumpMapType.set(1)
        except Exception as e:
            print e

        return shGrp


    # called from ui
    def createAssignMaterial(self, assetPath):
        objs = pm.selected()
        shGrp = self.createMaterial(assetPath)
        pm.sets(shGrp, forceElement=objs)


    # helper function
    # creates file node and sets path and UDIM if necessary
    # returns the file node
    def createTextureNode(self, textureName, textureType):
        if os.path.exists(os.path.join(self.dirname, textureName)):
            colorTex = pm.shadingNode('file', asTexture = True, isColorManaged = True, name = '%s_%s'%(self.baseFilename, textureType))
            colorTex.fileTextureName.set(os.path.join(self.envDirname, textureName))
            if len(self.fileTokens)>2: colorTex.uvTilingMode.set('UDIM (Mari)')
            return colorTex
        else:
            pm.warning('%s Texture not found'%textureName)

