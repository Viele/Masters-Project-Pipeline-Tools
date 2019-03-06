import pymel.core as pm
import os
from PySide2 import QtWidgets, QtCore, QtGui

class Core():

    def __init__(self):
        pass
        
    def listAllFiles(self):
        for f in pm.ls(type='file'):
            print f.fileTextureName.get()

    def changeTextureSize(self, size, envVar):
        for f in pm.ls(type='file'):
            originalPath = f.fileTextureName.get()
            colorSpace = f.colorSpace.get()

            # substitute the environment variable for the actual path
            # this is highly unflexible, but hey, it's crunch
            env = pm.util.getEnv(envVar)
            if env:
                originalPath = originalPath.replace('${%s}'%envVar, env)

            path, filename = os.path.split(originalPath)

            # script wouldn't work if image is not png
            if not filename.split('.')[-1] == 'png':
                pm.error("Only supports pngs")

            if ( os.path.basename(path) == '256' or
                 os.path.basename(path) == '512'):
                # we are already in a subsized proxy and need to cut one folder from the path
                path = os.path.dirname(path)

            # we are at the root texture level and can just insert the size to path
            # only if we don't want the original
            if not size == 'original':
                path = os.path.join(path, size)
                if not os.path.exists(path):
                    os.mkdir(path)
            
            finalPath = os.path.join(path, filename)

            # if the file does not yet exist, create it
            if not os.path.exists(finalPath):
                picture = QtGui.QImage(originalPath)
                pic_rescaled = picture.scaled(int(size), int(size), QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)
                pic_rescaled.save(finalPath, "PNG")

            # set the path
            if env:
                finalPath = finalPath.replace(env, '${%s}'%envVar)
            f.fileTextureName.set(finalPath)
            f.colorSpace.set(colorSpace)

            
            