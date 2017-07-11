
import maya.OpenMaya as OpenMaya
import maya.OpenMayaMPx as OpenMayaMPx

kPluginNodeName = "LeiaCamera"
kPluginNodeID = OpenMaya.MTypeId(0x6368600)

kPluginTransformNodeName = "LeiaCameraTransform"
kPluginTransformNodeID = OpenMaya.MTypeId(0x6368601)
kPluginTransformMatrixID = OpenMaya.MTypeId(0x6368602)

kDrawDbClassification =  "drawdb/geometry/leiaCamera"
kDrawRegistrantId = "leiaCameraPlugin"

class LeiaCameraNode(OpenMayaMPx.MPxNode):

    aCenterCamera = OpenMaya.MObject()

    aNearClipPlane = OpenMaya.MObject()
    aFarClipPlane = OpenMaya.MObject()

    aBaselineScaling = OpenMaya.MObject()
    aFocalDistance = OpenMaya.MObject()

    aHFilmAperture = OpenMaya.MObject()
    aVFilmAperture = OpenMaya.MObject()
    aFieldOfView = OpenMaya.MObject()

    aZeroParallaxColor = OpenMaya.MObject()
    aZeroParallaxTransparency = OpenMaya.MObject()
    aSafeVolumeColor = OpenMaya.MObject()
    aSafeVolumeTransparency = OpenMaya.MObject()

    aNearClipPlaneOut = OpenMaya.MObject()
    aFarClipPlaneOut = OpenMaya.MObject()

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

    def compute(self, plug, data):
        if plug.isNull():
            return OpenMayaMPx.MPxNode.compute(self, plug, data)

        if ((plug == self.aNearClipPlaneOut)
        or  (plug == self.aFarClipPlaneOut)
        or  (plug == self.aFilmOffset00)
        or  (plug == self.aFilmOffset01)
        or  (plug == self.aFilmOffset02)
        or  (plug == self.aFilmOffset03)
        or  (plug == self.aViewOffset00)
        or  (plug == self.aViewOffset01)
        or  (plug == self.aViewOffset02)
        or  (plug == self.aViewOffset03)):
            try:
                info("Compute called")
            except Exception, ex:
                error("Failed to compute value for plugin")

        return OpenMayaMPx.MPxNode.compute(self, plug, data)

    @staticmethod
    def create( ):
        return LeiaCameraNode()

    @staticmethod
    def initialize( ):
        _num_Attr = OpenMaya.MFnNumericAttribute()
        _msg_Attr = OpenMaya.MFnMessageAttribute()

        LeiaCameraNode.aCenterCamera = _msg_Attr.create("centerCamera", "cam")
        _msg_Attr.keyable = False
        _msg_Attr.storable = True
        _msg_Attr.hidden = True
        LeiaCameraNode.addAttribute(LeiaCameraNode.aCenterCamera)

        LeiaCameraNode.aFocalLength = _num_Attr.create("focalLength", "fcl", OpenMaya.MFnNumericData.kFloat, 35.0)
        _num_Attr.keyable = True
        _num_Attr.storable = True
        _num_Attr.hidden = False
        LeiaCameraNode.addAttribute(LeiaCameraNode.aFocalLength)

        LeiaCameraNode.aNearClipPlane = _num_Attr.create("nearClipPlane", "ncp", OpenMaya.MFnNumericData.kFloat, 0.1)
        _num_Attr.keyable = False
        _num_Attr.storable = True
        _num_Attr.hidden = False
        LeiaCameraNode.addAttribute(LeiaCameraNode.aNearClipPlane)

        LeiaCameraNode.aFarClipPlane = _num_Attr.create("farClipPlane", "fcp", OpenMaya.MFnNumericData.kFloat, 1000.0)
        _num_Attr.keyable = False
        _num_Attr.storable = True
        _num_Attr.hidden = False
        LeiaCameraNode.addAttribute(LeiaCameraNode.aFarClipPlane)

        LeiaCameraNode.aBaselineScaling = _num_Attr.create("baselineScaling", "bsc", OpenMaya.MFnNumericData.kFloat, 0.455)
        _num_Attr.keyable = True
        _num_Attr.storable = True
        _num_Attr.hidden = False
        LeiaCameraNode.addAttribute(LeiaCameraNode.aBaselineScaling)

        LeiaCameraNode.aFocalDistance = _num_Attr.create("focalDistance", "fcd", OpenMaya.MFnNumericData.kFloat, 5.0)
        _num_Attr.keyable = True
        _num_Attr.storable = True
        _num_Attr.hidden = False
        LeiaCameraNode.addAttribute(LeiaCameraNode.aFocalDistance)

        LeiaCameraNode.aHFilmAperture = _num_Attr.create("horizontalFilmAperture", "hfa", OpenMaya.MFnNumericData.kFloat, 1.4173200000000001)
        _num_Attr.keyable = True
        _num_Attr.readable = True
        _num_Attr.writable = False
        _num_Attr.storable = True
        _num_Attr.hidden = False
        LeiaCameraNode.addAttribute(LeiaCameraNode.aHFilmAperture)

        LeiaCameraNode.aVFilmAperture = _num_Attr.create("verticalFilmAperture", "vfa", OpenMaya.MFnNumericData.kFloat, 0.94488)
        _num_Attr.keyable = True
        _num_Attr.readable = True
        _num_Attr.writable = False
        _num_Attr.storable = True
        _num_Attr.hidden = False
        LeiaCameraNode.addAttribute(LeiaCameraNode.aVFilmAperture)

        LeiaCameraNode.aFieldOfView = _num_Attr.create("fieldOfView", "fov", OpenMaya.MFnNumericData.kFloat, 0.0)
        _num_Attr.keyable = False
        _num_Attr.readable = True
        _num_Attr.writable = False
        _num_Attr.storable = True
        _num_Attr.hidden = False
        LeiaCameraNode.addAttribute(LeiaCameraNode.aFieldOfView)

        LeiaCameraNode.aZeroParallaxColor = _num_Attr.create("zeroParallaxColor", "zpc", OpenMaya.MFnNumericData.k3Float)
        _num_Attr.default = (0.238, 0.808, 1.0)
        _num_Attr.usedAsColor = True
        _num_Attr.keyable = False
        _num_Attr.storable = True
        LeiaCameraNode.addAttribute(LeiaCameraNode.aZeroParallaxColor)

        LeiaCameraNode.aZeroParallaxTransparency = _num_Attr.create("zeroParallaxTransparency", "zpt", OpenMaya.MFnNumericData.kFloat, 0.25)
        _num_Attr.setSoftMin(0.0)
        _num_Attr.setSoftMax(1.0)
        _num_Attr.keyable = False
        _num_Attr.storable = True
        LeiaCameraNode.addAttribute(LeiaCameraNode.aZeroParallaxTransparency)

        LeiaCameraNode.aSafeVolumeColor = _num_Attr.create("safeVolumeColor", "svc", OpenMaya.MFnNumericData.k3Float)
        _num_Attr.default = (0.238, 0.808, 1.0)
        _num_Attr.usedAsColor = True
        _num_Attr.keyable = False
        _num_Attr.storable = True
        LeiaCameraNode.addAttribute(LeiaCameraNode.aSafeVolumeColor)

        LeiaCameraNode.aSafeVolumeTransparency = _num_Attr.create("safeVolumeTransparency", "svt", OpenMaya.MFnNumericData.kFloat, 0.25)
        _num_Attr.setSoftMin(0.0)
        _num_Attr.setSoftMax(1.0)
        _num_Attr.keyable = False
        _num_Attr.storable = True
        LeiaCameraNode.addAttribute(LeiaCameraNode.aSafeVolumeTransparency)

        LeiaCameraNode.aNearClipPlaneOut = _num_Attr.create("nearClipPlaneOut", "ncpo", OpenMaya.MFnNumericData.kFloat, 0.1)
        _num_Attr.keyable = False
        _num_Attr.readable = True
        _num_Attr.writable = False
        _num_Attr.storable = True
        _num_Attr.hidden = True
        LeiaCameraNode.addAttribute(LeiaCameraNode.aNearClipPlaneOut)

        LeiaCameraNode.aFarClipPlaneOut = _num_Attr.create("farClipPlaneOut", "fcpo", OpenMaya.MFnNumericData.kFloat, 1000.0)
        _num_Attr.keyable = False
        _num_Attr.readable = True
        _num_Attr.writable = False
        _num_Attr.storable = True
        _num_Attr.hidden = True
        LeiaCameraNode.addAttribute(LeiaCameraNode.aFarClipPlaneOut)

        LeiaCameraNode.aFilmOffset00 = _num_Attr.create("filmOffset00", "fo00", OpenMaya.MFnNumericData.kFloat, 0.0)
        _num_Attr.storable = True
        _num_Attr.readable = True
        _num_Attr.writable = False
        _msg_Attr.keyable = False
        LeiaCameraNode.addAttribute(LeiaCameraNode.aFilmOffset00)

        LeiaCameraNode.aFilmOffset01 = _num_Attr.create("filmOffset01", "fo01", OpenMaya.MFnNumericData.kFloat, 0.0)
        _num_Attr.storable = True
        _num_Attr.readable = True
        _num_Attr.writable = False
        _msg_Attr.keyable = False
        LeiaCameraNode.addAttribute(LeiaCameraNode.aFilmOffset01)

        LeiaCameraNode.aFilmOffset02 = _num_Attr.create("filmOffset02", "fo02", OpenMaya.MFnNumericData.kFloat, 0.0)
        _num_Attr.storable = True
        _num_Attr.readable = True
        _num_Attr.writable = False
        _msg_Attr.keyable = False
        LeiaCameraNode.addAttribute(LeiaCameraNode.aFilmOffset02)

        LeiaCameraNode.aFilmOffset03 = _num_Attr.create("filmOffset03", "fo03", OpenMaya.MFnNumericData.kFloat, 0.0)
        _num_Attr.storable = True
        _num_Attr.readable = True
        _num_Attr.writable = False
        _msg_Attr.keyable = False
        LeiaCameraNode.addAttribute(LeiaCameraNode.aFilmOffset03)

        LeiaCameraNode.aViewOffset00 = _num_Attr.create("viewOffset00", "vo00", OpenMaya.MFnNumericData.kFloat, 3.0)
        _num_Attr.storable = True
        _num_Attr.readable = True
        _num_Attr.writable = False
        _msg_Attr.keyable = False
        LeiaCameraNode.addAttribute(LeiaCameraNode.aViewOffset00)

        LeiaCameraNode.aViewOffset01 = _num_Attr.create("viewOffset01", "vo01", OpenMaya.MFnNumericData.kFloat, 1.0)
        _num_Attr.storable = True
        _num_Attr.readable = True
        _num_Attr.writable = False
        _msg_Attr.keyable = False
        LeiaCameraNode.addAttribute(LeiaCameraNode.aViewOffset01)

        LeiaCameraNode.aViewOffset02 = _num_Attr.create("viewOffset02", "vo02", OpenMaya.MFnNumericData.kFloat, -1.0)
        _num_Attr.storable = True
        _num_Attr.readable = True
        _num_Attr.writable = False
        _msg_Attr.keyable = False
        LeiaCameraNode.addAttribute(LeiaCameraNode.aViewOffset02)

        LeiaCameraNode.aViewOffset03 = _num_Attr.create("viewOffset03", "vo03", OpenMaya.MFnNumericData.kFloat, -3.0)
        _num_Attr.storable = True
        _num_Attr.readable = True
        _num_Attr.writable = False
        _msg_Attr.keyable = False
        LeiaCameraNode.addAttribute(LeiaCameraNode.aViewOffset03)

        LeiaCameraNode.attributeAffects(LeiaCameraNode.aNearClipPlane, LeiaCameraNode.aNearClipPlaneOut)
        LeiaCameraNode.attributeAffects(LeiaCameraNode.aFarClipPlane, LeiaCameraNode.aFarClipPlaneOut)

        LeiaCameraNode.attributeAffects(LeiaCameraNode.aHFilmAperture, LeiaCameraNode.aFieldOfView)
        LeiaCameraNode.attributeAffects(LeiaCameraNode.aHFilmAperture, LeiaCameraNode.aFilmOffset00)
        LeiaCameraNode.attributeAffects(LeiaCameraNode.aHFilmAperture, LeiaCameraNode.aFilmOffset01)
        LeiaCameraNode.attributeAffects(LeiaCameraNode.aHFilmAperture, LeiaCameraNode.aFilmOffset02)
        LeiaCameraNode.attributeAffects(LeiaCameraNode.aHFilmAperture, LeiaCameraNode.aFilmOffset03)
        LeiaCameraNode.attributeAffects(LeiaCameraNode.aHFilmAperture, LeiaCameraNode.aViewOffset00)
        LeiaCameraNode.attributeAffects(LeiaCameraNode.aHFilmAperture, LeiaCameraNode.aViewOffset01)
        LeiaCameraNode.attributeAffects(LeiaCameraNode.aHFilmAperture, LeiaCameraNode.aViewOffset02)
        LeiaCameraNode.attributeAffects(LeiaCameraNode.aHFilmAperture, LeiaCameraNode.aViewOffset03)

        LeiaCameraNode.attributeAffects(LeiaCameraNode.aVFilmAperture, LeiaCameraNode.aFieldOfView)
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

class LeiaCameraTransformMatrix(OpenMayaMPx.MPxTransformationMatrix):
    def __init__(self):
        super(LeiaCameraTransformMatrix, self).__init__()

class LeiaCameraTransform(OpenMayaMPx.MPxTransform):

    aleiaCamera = OpenMaya.MObject()

    aCameraPan = OpenMaya.MObject()
    aCameraRoll = OpenMaya.MObject()
    aCameraTilt = OpenMaya.MObject()
    aCameraTrack = OpenMaya.MObject()

    def __init__(self):
        super(LeiaCameraTransform, self).__init__()

    def className(self):
        return kPluginTransformNodeName

    def validateAndSetValue(self, plug, handle):
        OpenMayaMPx.MPxTransform.validateAndSetValue(self, plug, handle)

    @staticmethod
    def matrix():
        return OpenMayaMPx.asMPxPtr(LeiaCameraTransformMatrix())

    @staticmethod
    def create( ):
        return LeiaCameraTransform()

    @staticmethod
    def initialize( ):
        _num_Attr = OpenMaya.MFnNumericAttribute()
        _msg_Attr = OpenMaya.MFnMessageAttribute()

        LeiaCameraNode.aCenterCamera = _msg_Attr.create("leiaCamera", "cam")
        _num_Attr.writable = False
        _msg_Attr.storable = True
        _msg_Attr.hidden = True
        LeiaCameraNode.addAttribute(LeiaCameraNode.aCenterCamera)

        LeiaCameraTransform.aCameraPan = _num_Attr.create("cameraPan", "pan", OpenMaya.MFnNumericData.kFloat, 0.0)
        _num_Attr.storable = True
        _num_Attr.readable = True
        _num_Attr.writable = True
        LeiaCameraTransform.addAttribute(LeiaCameraTransform.aCameraPan)

        LeiaCameraTransform.aCameraRoll = _num_Attr.create("cameraRoll", "rol", OpenMaya.MFnNumericData.kFloat, 0.0)
        _num_Attr.storable = True
        _num_Attr.readable = True
        _num_Attr.writable = True
        LeiaCameraTransform.addAttribute(LeiaCameraTransform.aCameraRoll)

        LeiaCameraTransform.aCameraTilt = _num_Attr.create("cameraTilt", "tlt", OpenMaya.MFnNumericData.kFloat, 0.0)
        _num_Attr.storable = True
        _num_Attr.readable = True
        _num_Attr.writable = True
        LeiaCameraTransform.addAttribute(LeiaCameraTransform.aCameraTilt)

        LeiaCameraTransform.aCameraTrack = _num_Attr.create("cameraTrack", "trk", OpenMaya.MFnNumericData.k2Float)
        _num_Attr.default = (0.0, 0.0)
        _num_Attr.storable = True
        _num_Attr.readable = True
        _num_Attr.writable = True
        LeiaCameraTransform.addAttribute(LeiaCameraTransform.aCameraTrack)

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
    mplugin = OpenMayaMPx.MFnPlugin(mobject, "LeiaInc", "1.0", "Any")

    try:
        mplugin.registerNode(kPluginNodeName, kPluginNodeID,
                            LeiaCameraNode.create, LeiaCameraNode.initialize,
                            OpenMayaMPx.MPxNode.kDependNode, kDrawDbClassification)
    except:
        error("Failed to register node")
        raise

    try:
        mplugin.registerTransform(kPluginTransformNodeName, kPluginTransformNodeID,
                                LeiaCameraTransform.create, LeiaCameraTransform.initialize, LeiaCameraTransform.matrix,
                                kPluginTransformMatrixID)
    except:
        error( "Failed to register transform")
        raise

    info("Plug-in initialized")

def uninitializePlugin(mobject):
    mplugin = OpenMayaMPx.getMFunctionPlugin(mobject)

    try:
        mplugin.deregisterNode(kPluginNodeName)
    except:
        error("Failed to deregister node")
        raise

    try:
        mplugin.deregisterNode(kPluginTransformNodeID)
    except:
        error("Failed to deregister node")
        raise

    info("Plug-in uninitialized")
