import pymel.core as pm


class Core():

    def __init__(self):
        pass

    def addAttrFromGroup(self, targets, attrType):
        for obj in targets:
            pm.vray('addAttributesFromGroup', obj, attrType, 1)

    def rmAttrFromGroup(self, targets, attrType):
        for obj in targets:
            pm.vray('addAttributesFromGroup', obj, attrType, 0)

    