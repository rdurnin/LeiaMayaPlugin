
import maya.api.OpenMaya as OpenMaya
import maya.api.OpenMayaRender as OpenMayaRender
import maya.api.OpenMayaUI as OpenMayaUI

import leia

kPluginNodeName = "LeiaCamera"
kPluginNodeID = OpenMaya.MTypeId(0x6368600)

kPluginManipName = "LeiaCameraManipulator"
kPluginManipId = OpenMaya.MTypeId(0x6368606)

kDrawDbClassification =  "drawdb/geometry/LeiaCamera"
kDrawRegistrantId = "LeiaCameraPlugin"

def maya_useNewAPI( ):
    pass


class LeiaCameraNode(OpenMayaUI.MPxLocatorNode):

    aCenterCamera = OpenMaya.MObject()

    aFocalLength = OpenMaya.MObject()
    aNearClipPlane = OpenMaya.MObject()
    aFarClipPlane = OpenMaya.MObject()

    aBaselineScaling = OpenMaya.MObject()
    aFocalDistance = OpenMaya.MObject()

    aHFilmAperture = OpenMaya.MObject()
    aVFilmAperture = OpenMaya.MObject()

    aBaseline = OpenMaya.MObject()
    aDisparityLimit = OpenMaya.MObject()

    aZeroParallaxColor = OpenMaya.MObject()
    aZeroParallaxTransparency = OpenMaya.MObject()
    aSafeVolumeColor = OpenMaya.MObject()
    aSafeVolumeTransparency = OpenMaya.MObject()

    aNearZ = OpenMaya.MObject()
    aNearHalfWidth = OpenMaya.MObject()
    aNearHalfHeight = OpenMaya.MObject()
    aScreenZ = OpenMaya.MObject()
    aScreenHalfWidth = OpenMaya.MObject()
    aScreenHalfHeight = OpenMaya.MObject()
    aFarZ = OpenMaya.MObject()
    aFarHalfWidth = OpenMaya.MObject()
    aFarHalfHeight = OpenMaya.MObject()

    aFilmOffset00 = OpenMaya.MObject()
    aFilmOffset01 = OpenMaya.MObject()
    aFilmOffset02 = OpenMaya.MObject()
    aFilmOffset03 = OpenMaya.MObject()

    aViewOffset00 = OpenMaya.MObject()
    aViewOffset01 = OpenMaya.MObject()
    aViewOffset02 = OpenMaya.MObject()
    aViewOffset03 = OpenMaya.MObject()

    def __init__(self):
        super(LeiaCameraNode, self).__init__()

    def postConstructor(self):
        nodeFn = OpenMaya.MFnDependencyNode(self.thisMObject())
        nodeFn.setName("%sShape" % kPluginNodeName)

    def className(self):
        return kPluginNodeName

    def isBounded(self):
        return False

    def excludeAsLocator(self):
        return True

    def compute(self, plug, data):
        if plug.isNull:
            return OpenMayaUI.MPxLocatorNode.compute(self, plug, data)

        if ((plug == self.aFilmOffset00)
        or  (plug == self.aFilmOffset01)
        or  (plug == self.aFilmOffset02)
        or  (plug == self.aFilmOffset03)
        or  (plug == self.aViewOffset00)
        or  (plug == self.aViewOffset01)
        or  (plug == self.aViewOffset02)
        or  (plug == self.aViewOffset03)):
            blData = data.inputValue(LeiaCameraNode.aBaselineScaling)
            fdData = data.inputValue(LeiaCameraNode.aFocalDistance)
            flData = data.inputValue(LeiaCameraNode.aFocalLength)
            hfData = data.inputValue(LeiaCameraNode.aHFilmAperture)

            baselineScaling = blData.asFloat()
            focalDistance = fdData.asFloat()
            focalLength = flData.asFloat()
            horizontalFilmAperture = hfData.asFloat()
            maxDisparity = 5.0
            deltaView = 0.133
            screenWidth = 2560.0
            screenHeight = 1440.0
            tileResX = 640.0

            try:
                lcam = leia.leiaCamera.computeLeiaCamera(horizontalFilmAperture, focalLength, focalDistance, baselineScaling,
                                                                    maxDisparity, deltaView, screenWidth, screenHeight, tileResX)

            except:
                error("Failed to compute LeiaCamera")
                raise

            aBaseline = data.outputValue(LeiaCameraNode.aBaseline)
            aBaseline.setFloat(lcam.baseline)
            aDisparityLimit = data.outputValue(LeiaCameraNode.aDisparityLimit)
            aDisparityLimit.setFloat(lcam.disparityLimit)

            aNearZ = data.outputValue(LeiaCameraNode.aNearZ)
            aNearZ.setFloat(lcam.nearZ)
            aNearHalfWidth = data.outputValue(LeiaCameraNode.aNearHalfWidth)
            aNearHalfWidth.setFloat(lcam.nearHalfWidth)
            aNearHalfHeight = data.outputValue(LeiaCameraNode.aNearHalfHeight)
            aNearHalfHeight.setFloat(lcam.nearHalfHeight)

            aScreenZ = data.outputValue(LeiaCameraNode.aScreenZ)
            aScreenZ.setFloat(lcam.screenZ)
            aScreenHalfWidth = data.outputValue(LeiaCameraNode.aScreenHalfWidth)
            aScreenHalfWidth.setFloat(lcam.screenHalfWidth)
            aScreenHalfHeight = data.outputValue(LeiaCameraNode.aScreenHalfHeight)
            aScreenHalfHeight.setFloat(lcam.screenHalfHeight)

            aFarZ = data.outputValue(LeiaCameraNode.aFarZ)
            aFarZ.setFloat(lcam.farZ)
            aFarHalfWidth = data.outputValue(LeiaCameraNode.aFarHalfWidth)
            aFarHalfWidth.setFloat(lcam.farHalfWidth)
            aFarHalfHeight = data.outputValue(LeiaCameraNode.aFarHalfHeight)
            aFarHalfHeight.setFloat(lcam.farHalfHeight)

            aFilmOffset00 = data.outputValue(LeiaCameraNode.aFilmOffset00)
            aFilmOffset00.setFloat(lcam.filmOffset00)
            aFilmOffset01 = data.outputValue(LeiaCameraNode.aFilmOffset01)
            aFilmOffset01.setFloat(lcam.filmOffset01)
            aFilmOffset02 = data.outputValue(LeiaCameraNode.aFilmOffset02)
            aFilmOffset02.setFloat(lcam.filmOffset02)
            aFilmOffset03 = data.outputValue(LeiaCameraNode.aFilmOffset03)
            aFilmOffset03.setFloat(lcam.filmOffset03)

            aViewOffset00 = data.outputValue(LeiaCameraNode.aViewOffset00)
            aViewOffset00.setFloat(lcam.viewOffset00)
            aViewOffset01 = data.outputValue(LeiaCameraNode.aViewOffset01)
            aViewOffset01.setFloat(lcam.viewOffset01)
            aViewOffset02 = data.outputValue(LeiaCameraNode.aViewOffset02)
            aViewOffset02.setFloat(lcam.viewOffset02)
            aViewOffset03 = data.outputValue(LeiaCameraNode.aViewOffset03)
            aViewOffset03.setFloat(lcam.viewOffset03)

            data.setClean(plug)

        return OpenMayaUI.MPxLocatorNode.compute(self, plug, data)

    @staticmethod
    def create( ):
        return LeiaCameraNode()

    @staticmethod
    def initialize( ):
        _num_Attr = OpenMaya.MFnNumericAttribute()
        _msg_Attr = OpenMaya.MFnMessageAttribute()

        LeiaCameraNode.aCenterCamera = _msg_Attr.create("centerCamera", "cam")
        _msg_Attr.keyable = False
        _msg_Attr.hidden = True
        LeiaCameraNode.addAttribute(LeiaCameraNode.aCenterCamera)

        LeiaCameraNode.aFocalLength = _num_Attr.create("focalLength", "fcl", OpenMaya.MFnNumericData.kFloat, 35.0)
        _num_Attr.keyable = True
        _num_Attr.hidden = False
        _num_Attr.setSoftMin(2.5)
        _num_Attr.setSoftMax(3500.0)
        LeiaCameraNode.addAttribute(LeiaCameraNode.aFocalLength)

        LeiaCameraNode.aNearClipPlane = _num_Attr.create("nearClipPlane", "ncp", OpenMaya.MFnNumericData.kFloat, 0.1)
        _num_Attr.keyable = False
        _num_Attr.hidden = False
        LeiaCameraNode.addAttribute(LeiaCameraNode.aNearClipPlane)

        LeiaCameraNode.aFarClipPlane = _num_Attr.create("farClipPlane", "fcp", OpenMaya.MFnNumericData.kFloat, 1000.0)
        _num_Attr.keyable = False
        _num_Attr.hidden = False
        LeiaCameraNode.addAttribute(LeiaCameraNode.aFarClipPlane)

        LeiaCameraNode.aBaselineScaling = _num_Attr.create("baselineScaling", "bsc", OpenMaya.MFnNumericData.kFloat, 0.455)
        _num_Attr.keyable = True
        _num_Attr.hidden = False
        _num_Attr.setSoftMin(0.001)
        _num_Attr.setSoftMax(1.0)
        LeiaCameraNode.addAttribute(LeiaCameraNode.aBaselineScaling)

        LeiaCameraNode.aFocalDistance = _num_Attr.create("focalDistance", "fcd", OpenMaya.MFnNumericData.kFloat, 5.0)
        _num_Attr.keyable = True
        _num_Attr.hidden = False
        LeiaCameraNode.addAttribute(LeiaCameraNode.aFocalDistance)

        LeiaCameraNode.aHFilmAperture = _num_Attr.create("horizontalFilmAperture", "hfa", OpenMaya.MFnNumericData.kFloat, 1.4173200000000001)
        _num_Attr.keyable = True
        _num_Attr.hidden = False
        LeiaCameraNode.addAttribute(LeiaCameraNode.aHFilmAperture)

        LeiaCameraNode.aVFilmAperture = _num_Attr.create("verticalFilmAperture", "vfa", OpenMaya.MFnNumericData.kFloat, 0.94488)
        _num_Attr.keyable = True
        _num_Attr.hidden = False
        LeiaCameraNode.addAttribute(LeiaCameraNode.aVFilmAperture)

        LeiaCameraNode.aZeroParallaxColor = _num_Attr.create("zeroParallaxColor", "zpc", OpenMaya.MFnNumericData.k3Float)
        _num_Attr.usedAsColor = True
        _num_Attr.keyable = False
        _num_Attr.default = 0.83, 0.23, 0.1
        LeiaCameraNode.addAttribute(LeiaCameraNode.aZeroParallaxColor)

        LeiaCameraNode.aZeroParallaxTransparency = _num_Attr.create("zeroParallaxTransparency", "zpt", OpenMaya.MFnNumericData.kFloat, 0.665)
        _num_Attr.keyable = False
        _num_Attr.setSoftMin(0.0)
        _num_Attr.setSoftMax(1.0)
        LeiaCameraNode.addAttribute(LeiaCameraNode.aZeroParallaxTransparency)

        LeiaCameraNode.aSafeVolumeColor = _num_Attr.create("safeVolumeColor", "svc", OpenMaya.MFnNumericData.k3Float)
        _num_Attr.usedAsColor = True
        _num_Attr.keyable = False
        _num_Attr.default = 0.238, 0.808, 1.0
        LeiaCameraNode.addAttribute(LeiaCameraNode.aSafeVolumeColor)

        LeiaCameraNode.aSafeVolumeTransparency = _num_Attr.create("safeVolumeTransparency", "svt", OpenMaya.MFnNumericData.kFloat, 0.845)
        _num_Attr.keyable = False
        _num_Attr.setSoftMin(0.0)
        _num_Attr.setSoftMax(1.0)
        LeiaCameraNode.addAttribute(LeiaCameraNode.aSafeVolumeTransparency)

        LeiaCameraNode.aBaseline = _num_Attr.create("baseline", "b", OpenMaya.MFnNumericData.kFloat)
        _num_Attr.keyable = False
        _num_Attr.writable = False
        _num_Attr.hidden = True
        _num_Attr.storable = False
        LeiaCameraNode.addAttribute(LeiaCameraNode.aBaseline)

        LeiaCameraNode.aDisparityLimit = _num_Attr.create("disparityLimit", "dl", OpenMaya.MFnNumericData.kFloat)
        _num_Attr.keyable = False
        _num_Attr.writable = False
        _num_Attr.hidden = True
        _num_Attr.storable = False
        LeiaCameraNode.addAttribute(LeiaCameraNode.aDisparityLimit)

        LeiaCameraNode.aNearZ = _num_Attr.create("nearZ", "nz", OpenMaya.MFnNumericData.kFloat)
        _num_Attr.keyable = False
        _num_Attr.writable = False
        _num_Attr.hidden = True
        _num_Attr.storable = False
        LeiaCameraNode.addAttribute(LeiaCameraNode.aNearZ)

        LeiaCameraNode.aNearHalfWidth = _num_Attr.create("nearHalfWidth", "nhw", OpenMaya.MFnNumericData.kFloat)
        _num_Attr.keyable = False
        _num_Attr.writable = False
        _num_Attr.hidden = True
        _num_Attr.storable = False
        LeiaCameraNode.addAttribute(LeiaCameraNode.aNearHalfWidth)

        LeiaCameraNode.aNearHalfHeight = _num_Attr.create("nearHalfHeight", "nhh", OpenMaya.MFnNumericData.kFloat)
        _num_Attr.keyable = False
        _num_Attr.writable = False
        _num_Attr.hidden = True
        _num_Attr.storable = False
        LeiaCameraNode.addAttribute(LeiaCameraNode.aNearHalfHeight)

        LeiaCameraNode.aScreenZ = _num_Attr.create("screenZ", "sz", OpenMaya.MFnNumericData.kFloat)
        _num_Attr.keyable = False
        _num_Attr.writable = False
        _num_Attr.hidden = True
        _num_Attr.storable = False
        LeiaCameraNode.addAttribute(LeiaCameraNode.aScreenZ)

        LeiaCameraNode.aScreenHalfWidth = _num_Attr.create("screenHalfWidth", "shw", OpenMaya.MFnNumericData.kFloat)
        _num_Attr.keyable = False
        _num_Attr.writable = False
        _num_Attr.hidden = True
        _num_Attr.storable = False
        LeiaCameraNode.addAttribute(LeiaCameraNode.aScreenHalfWidth)

        LeiaCameraNode.aScreenHalfHeight = _num_Attr.create("screenHalfHeight", "shh", OpenMaya.MFnNumericData.kFloat)
        _num_Attr.keyable = False
        _num_Attr.writable = False
        _num_Attr.hidden = True
        _num_Attr.storable = False
        LeiaCameraNode.addAttribute(LeiaCameraNode.aScreenHalfHeight)

        LeiaCameraNode.aFarZ = _num_Attr.create("farZ", "fz", OpenMaya.MFnNumericData.kFloat)
        _num_Attr.keyable = False
        _num_Attr.writable = False
        _num_Attr.hidden = True
        _num_Attr.storable = False
        LeiaCameraNode.addAttribute(LeiaCameraNode.aFarZ)

        LeiaCameraNode.aFarHalfWidth = _num_Attr.create("farHalfWidth", "fhw", OpenMaya.MFnNumericData.kFloat)
        _num_Attr.keyable = False
        _num_Attr.writable = False
        _num_Attr.hidden = True
        _num_Attr.storable = False
        LeiaCameraNode.addAttribute(LeiaCameraNode.aFarHalfWidth)

        LeiaCameraNode.aFarHalfHeight = _num_Attr.create("farHalfHeight", "fhh", OpenMaya.MFnNumericData.kFloat)
        _num_Attr.keyable = False
        _num_Attr.writable = False
        _num_Attr.hidden = True
        _num_Attr.storable = False
        LeiaCameraNode.addAttribute(LeiaCameraNode.aFarHalfHeight)

        LeiaCameraNode.aFilmOffset00 = _num_Attr.create("filmOffset00", "fo00", OpenMaya.MFnNumericData.kFloat, 0.0)
        _num_Attr.writable = False
        _msg_Attr.keyable = False
        _num_Attr.hidden = True
        _num_Attr.storable = False
        LeiaCameraNode.addAttribute(LeiaCameraNode.aFilmOffset00)

        LeiaCameraNode.aFilmOffset01 = _num_Attr.create("filmOffset01", "fo01", OpenMaya.MFnNumericData.kFloat, 0.0)
        _num_Attr.writable = False
        _msg_Attr.keyable = False
        _num_Attr.hidden = True
        _num_Attr.storable = False
        LeiaCameraNode.addAttribute(LeiaCameraNode.aFilmOffset01)

        LeiaCameraNode.aFilmOffset02 = _num_Attr.create("filmOffset02", "fo02", OpenMaya.MFnNumericData.kFloat, 0.0)
        _num_Attr.writable = False
        _msg_Attr.keyable = False
        _num_Attr.hidden = True
        _num_Attr.storable = False
        LeiaCameraNode.addAttribute(LeiaCameraNode.aFilmOffset02)

        LeiaCameraNode.aFilmOffset03 = _num_Attr.create("filmOffset03", "fo03", OpenMaya.MFnNumericData.kFloat, 0.0)
        _num_Attr.writable = False
        _msg_Attr.keyable = False
        _num_Attr.hidden = True
        _num_Attr.storable = False
        LeiaCameraNode.addAttribute(LeiaCameraNode.aFilmOffset03)

        LeiaCameraNode.aViewOffset00 = _num_Attr.create("viewOffset00", "vo00", OpenMaya.MFnNumericData.kFloat, 3.0)
        _num_Attr.writable = False
        _msg_Attr.keyable = False
        _num_Attr.hidden = True
        _num_Attr.storable = False
        LeiaCameraNode.addAttribute(LeiaCameraNode.aViewOffset00)

        LeiaCameraNode.aViewOffset01 = _num_Attr.create("viewOffset01", "vo01", OpenMaya.MFnNumericData.kFloat, 1.0)
        _num_Attr.writable = False
        _msg_Attr.keyable = False
        _num_Attr.hidden = True
        _num_Attr.storable = False
        LeiaCameraNode.addAttribute(LeiaCameraNode.aViewOffset01)

        LeiaCameraNode.aViewOffset02 = _num_Attr.create("viewOffset02", "vo02", OpenMaya.MFnNumericData.kFloat, -1.0)
        _num_Attr.writable = False
        _msg_Attr.keyable = False
        _num_Attr.hidden = True
        _num_Attr.storable = False
        LeiaCameraNode.addAttribute(LeiaCameraNode.aViewOffset02)

        LeiaCameraNode.aViewOffset03 = _num_Attr.create("viewOffset03", "vo03", OpenMaya.MFnNumericData.kFloat, -3.0)
        _num_Attr.writable = False
        _msg_Attr.keyable = False
        _num_Attr.hidden = True
        _num_Attr.storable = False
        LeiaCameraNode.addAttribute(LeiaCameraNode.aViewOffset03)

        LeiaCameraNode.attributeAffects(LeiaCameraNode.aFocalLength, LeiaCameraNode.aFilmOffset00)
        LeiaCameraNode.attributeAffects(LeiaCameraNode.aFocalLength, LeiaCameraNode.aFilmOffset01)
        LeiaCameraNode.attributeAffects(LeiaCameraNode.aFocalLength, LeiaCameraNode.aFilmOffset02)
        LeiaCameraNode.attributeAffects(LeiaCameraNode.aFocalLength, LeiaCameraNode.aFilmOffset03)
        LeiaCameraNode.attributeAffects(LeiaCameraNode.aFocalLength, LeiaCameraNode.aViewOffset00)
        LeiaCameraNode.attributeAffects(LeiaCameraNode.aFocalLength, LeiaCameraNode.aViewOffset01)
        LeiaCameraNode.attributeAffects(LeiaCameraNode.aFocalLength, LeiaCameraNode.aViewOffset02)
        LeiaCameraNode.attributeAffects(LeiaCameraNode.aFocalLength, LeiaCameraNode.aViewOffset03)

        LeiaCameraNode.attributeAffects(LeiaCameraNode.aHFilmAperture, LeiaCameraNode.aFilmOffset00)
        LeiaCameraNode.attributeAffects(LeiaCameraNode.aHFilmAperture, LeiaCameraNode.aFilmOffset01)
        LeiaCameraNode.attributeAffects(LeiaCameraNode.aHFilmAperture, LeiaCameraNode.aFilmOffset02)
        LeiaCameraNode.attributeAffects(LeiaCameraNode.aHFilmAperture, LeiaCameraNode.aFilmOffset03)
        LeiaCameraNode.attributeAffects(LeiaCameraNode.aHFilmAperture, LeiaCameraNode.aViewOffset00)
        LeiaCameraNode.attributeAffects(LeiaCameraNode.aHFilmAperture, LeiaCameraNode.aViewOffset01)
        LeiaCameraNode.attributeAffects(LeiaCameraNode.aHFilmAperture, LeiaCameraNode.aViewOffset02)
        LeiaCameraNode.attributeAffects(LeiaCameraNode.aHFilmAperture, LeiaCameraNode.aViewOffset03)

        LeiaCameraNode.attributeAffects(LeiaCameraNode.aVFilmAperture, LeiaCameraNode.aFilmOffset00)
        LeiaCameraNode.attributeAffects(LeiaCameraNode.aVFilmAperture, LeiaCameraNode.aFilmOffset01)
        LeiaCameraNode.attributeAffects(LeiaCameraNode.aVFilmAperture, LeiaCameraNode.aFilmOffset02)
        LeiaCameraNode.attributeAffects(LeiaCameraNode.aVFilmAperture, LeiaCameraNode.aFilmOffset03)
        LeiaCameraNode.attributeAffects(LeiaCameraNode.aVFilmAperture, LeiaCameraNode.aViewOffset00)
        LeiaCameraNode.attributeAffects(LeiaCameraNode.aVFilmAperture, LeiaCameraNode.aViewOffset01)
        LeiaCameraNode.attributeAffects(LeiaCameraNode.aVFilmAperture, LeiaCameraNode.aViewOffset02)
        LeiaCameraNode.attributeAffects(LeiaCameraNode.aVFilmAperture, LeiaCameraNode.aViewOffset03)

        LeiaCameraNode.attributeAffects(LeiaCameraNode.aBaselineScaling, LeiaCameraNode.aFilmOffset00)
        LeiaCameraNode.attributeAffects(LeiaCameraNode.aBaselineScaling, LeiaCameraNode.aFilmOffset01)
        LeiaCameraNode.attributeAffects(LeiaCameraNode.aBaselineScaling, LeiaCameraNode.aFilmOffset02)
        LeiaCameraNode.attributeAffects(LeiaCameraNode.aBaselineScaling, LeiaCameraNode.aFilmOffset03)
        LeiaCameraNode.attributeAffects(LeiaCameraNode.aBaselineScaling, LeiaCameraNode.aViewOffset00)
        LeiaCameraNode.attributeAffects(LeiaCameraNode.aBaselineScaling, LeiaCameraNode.aViewOffset01)
        LeiaCameraNode.attributeAffects(LeiaCameraNode.aBaselineScaling, LeiaCameraNode.aViewOffset02)
        LeiaCameraNode.attributeAffects(LeiaCameraNode.aBaselineScaling, LeiaCameraNode.aViewOffset03)

        LeiaCameraNode.attributeAffects(LeiaCameraNode.aFocalDistance, LeiaCameraNode.aFilmOffset00)
        LeiaCameraNode.attributeAffects(LeiaCameraNode.aFocalDistance, LeiaCameraNode.aFilmOffset01)
        LeiaCameraNode.attributeAffects(LeiaCameraNode.aFocalDistance, LeiaCameraNode.aFilmOffset02)
        LeiaCameraNode.attributeAffects(LeiaCameraNode.aFocalDistance, LeiaCameraNode.aFilmOffset03)
        LeiaCameraNode.attributeAffects(LeiaCameraNode.aFocalDistance, LeiaCameraNode.aViewOffset00)
        LeiaCameraNode.attributeAffects(LeiaCameraNode.aFocalDistance, LeiaCameraNode.aViewOffset01)
        LeiaCameraNode.attributeAffects(LeiaCameraNode.aFocalDistance, LeiaCameraNode.aViewOffset02)
        LeiaCameraNode.attributeAffects(LeiaCameraNode.aFocalDistance, LeiaCameraNode.aViewOffset03)

# class LeiaCameraManipulator(OpenMayaMPx.MPxManipContainer):
#     def __init__(self):
#         super(LeiaCameraManipulator, self).__init__()

class LeiaCameraUserData(OpenMaya.MUserData):
    def __init__(self):
        super(LeiaCameraUserData, self).__init__(False)

        self.fZeroParallaxColor = OpenMaya.MColor()
        self.fSafeVolumeColor = OpenMaya.MColor()

        self.fNearZ = 0.0
        self.fNearHalfWidth = 0.0
        self.fNearHalfHeight = 0.0

        self.fScreenZ = 0.0
        self.fScreenHalfWidth = 0.0
        self.fScreenHalfHeight = 0.0

        self.fFarZ = 0.0
        self.fFarHalfWidth = 0.0
        self.fFarHalfHeight = 0.0

class LeiaCameraDrawOverride(OpenMayaRender.MPxDrawOverride):
    def __init__(self, mobject):
        super(LeiaCameraDrawOverride, self).__init__(mobject, LeiaCameraDrawOverride.draw)

    @staticmethod
    def creator(mobject):
        return LeiaCameraDrawOverride(mobject)

    @staticmethod
    def draw(context, data):
        return

    def isBounded(self, mobject, cameraPath):
        return False

    def supportedDrawAPIs(self):
        return OpenMayaRender.MRenderer.kOpenGL | OpenMayaRender.MRenderer.kDirectX11

    def prepareForDraw(self, mobject, cameraPath, frameContext, data):
        if not isinstance(data, LeiaCameraUserData):
            data = LeiaCameraUserData()

        node = mobject.node()
        if node.isNull():
            return

        plug = OpenMaya.MPlug(node, LeiaCameraNode.aSafeVolumeColor)
        if not plug.isNull:
            mfnd = OpenMaya.MFnNumericData(plug.asMObject())
            data.fSafeVolumeColor = OpenMaya.MColor(mfnd.getData())

        plug = OpenMaya.MPlug(node, LeiaCameraNode.aSafeVolumeTransparency)
        if not plug.isNull:
            data.fSafeVolumeColor.a = 1.0 - plug.asFloat()

        plug = OpenMaya.MPlug(node, LeiaCameraNode.aZeroParallaxColor)
        if not plug.isNull:
            mfnd = OpenMaya.MFnNumericData(plug.asMObject())
            data.fZeroParallaxColor = OpenMaya.MColor(mfnd.getData())

        plug = OpenMaya.MPlug(node, LeiaCameraNode.aZeroParallaxTransparency)
        if not plug.isNull:
            data.fZeroParallaxColor.a = 1.0 - plug.asFloat()

        plug = OpenMaya.MPlug(node, LeiaCameraNode.aNearZ)
        if not plug.isNull:
            data.fNearZ = plug.asFloat()

        plug = OpenMaya.MPlug(node, LeiaCameraNode.aNearHalfWidth)
        if not plug.isNull:
            data.fNearHalfWidth = plug.asFloat()

        plug = OpenMaya.MPlug(node, LeiaCameraNode.aNearHalfHeight)
        if not plug.isNull:
            data.fNearHalfHeight = plug.asFloat()

        plug = OpenMaya.MPlug(node, LeiaCameraNode.aScreenZ)
        if not plug.isNull:
            data.fScreenZ = plug.asFloat()

        plug = OpenMaya.MPlug(node, LeiaCameraNode.aScreenHalfWidth)
        if not plug.isNull:
            data.fScreenHalfWidth = plug.asFloat()

        plug = OpenMaya.MPlug(node, LeiaCameraNode.aScreenHalfHeight)
        if not plug.isNull:
            data.fScreenHalfHeight = plug.asFloat()

        plug = OpenMaya.MPlug(node, LeiaCameraNode.aFarZ)
        if not plug.isNull:
            data.fFarZ = plug.asFloat()

        plug = OpenMaya.MPlug(node, LeiaCameraNode.aFarHalfWidth)
        if not plug.isNull:
            data.fFarHalfWidth = plug.asFloat()

        plug = OpenMaya.MPlug(node, LeiaCameraNode.aFarHalfHeight)
        if not plug.isNull:
            data.fFarHalfHeight = plug.asFloat()

        return data

    def hasUIDrawables(self):
        return True

    def addUIDrawables(self, mobject, drawManager, frameContext, data):
        if not isinstance(data, LeiaCameraUserData):
            return

        try:
            lbounds = leia.leiaCamera.computeLeiaCameraBounds(data.fNearHalfWidth, data.fNearHalfHeight, data.fNearZ,
                                                                data.fScreenHalfWidth, data.fScreenHalfHeight, data.fScreenZ,
                                                                data.fFarHalfWidth, data.fFarHalfHeight, data.fFarZ)

        except:
            error("Failed to compute LeiaCameraBounds")
            raise

        wireContrast = OpenMaya.MColor((0.85, 0.85, 0.85))

        drawManager.beginDrawable()
        drawManager.setDepthPriority(5)

        drawManager.setColor(data.fZeroParallaxColor)
        drawManager.mesh(OpenMayaRender.MGeometry.kTriangles, triangles(lbounds.screen))

        drawManager.setColor(data.fZeroParallaxColor * wireContrast)
        drawManager.mesh(OpenMayaRender.MUIDrawManager.kClosedLine, quad(lbounds.screen))

        drawManager.setColor(data.fSafeVolumeColor)

        planes = [lbounds.south, lbounds.north, lbounds.east, lbounds.west, lbounds.top, lbounds.bottom]

        for plane in planes:
            drawManager.mesh(OpenMayaRender.MGeometry.kTriangles, triangles(plane))

        drawManager.setColor(data.fSafeVolumeColor * wireContrast)

        for plane in planes:
            drawManager.mesh(OpenMayaRender.MUIDrawManager.kClosedLine, quad(plane))

        drawManager.endDrawable()


def triangles(l):
    t = OpenMaya.MPointArray()

    t.append(OpenMaya.MPoint(l[0]))
    t.append(OpenMaya.MPoint(l[1]))
    t.append(OpenMaya.MPoint(l[2]))
    t.append(OpenMaya.MPoint(l[0]))
    t.append(OpenMaya.MPoint(l[2]))
    t.append(OpenMaya.MPoint(l[3]))

    return t

def quad(l):
    t = OpenMaya.MPointArray()

    t.append(OpenMaya.MPoint(l[0]))
    t.append(OpenMaya.MPoint(l[1]))
    t.append(OpenMaya.MPoint(l[2]))
    t.append(OpenMaya.MPoint(l[3]))

    return t

def info(message):
    fullMsg = "%s: %s" % (kPluginNodeName, message)
    OpenMaya.MGlobal.displayInfo(fullMsg)

def warn(message):
    fullMsg = "%s: %s" % (kPluginNodeName, message)
    OpenMaya.MGlobal.displayWarning(fullMsg)

def error(message):
    fullMsg = "%s: %s" % (kPluginNodeName, message)
    OpenMaya.MGlobal.displayError(fullMsg)

def initializePlugin(mobject):
    mplugin = OpenMaya.MFnPlugin(mobject, "LeiaInc", "1.0", "Any")

    try:
        mplugin.registerNode(kPluginNodeName, kPluginNodeID,
                            LeiaCameraNode.create, LeiaCameraNode.initialize,
                            OpenMaya.MPxNode.kLocatorNode, kDrawDbClassification)
    except:
        error("Failed to register node")
        raise

    # try:
    #     mplugin.registerNode(kPluginManipName, kPluginManipId,
    #                         LeiaCameraManip.create, LeiaCameraManip.initialize,
    #                         OpenMayaMPx.MPxNode.kManipContainer)
    # except:
    #     error("Failed to register manipulator")
    #     raise

    try:
        OpenMayaRender.MDrawRegistry.registerDrawOverrideCreator(kDrawDbClassification, kDrawRegistrantId,
                                                                            LeiaCameraDrawOverride.creator)
    except:
        error("Failed to register draw override")
        raise

    info("Plug-in initialized")

def uninitializePlugin(mobject):
    mplugin = OpenMaya.getMFunctionPlugin(mobject)

    try:
        mplugin.deregisterNode(kPluginNodeName)
    except:
        error("Failed to deregister node")
        raise

    try:
        OpenMayaRender.MDrawRegistry.deregisterDrawOverrideCreator(kDrawDbClassification, kDrawRegistrantId)
    except:
        error("Failed to deregister draw override")
        pass

    info("Plug-in uninitialized")
