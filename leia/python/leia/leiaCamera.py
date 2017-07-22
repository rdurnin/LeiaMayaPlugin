
import math
import maya.cmds as mc


class LeiaCamera(object):
    def __init__(self):
        super(LeiaCamera, self).__init__()

        self._distortedFocalDistance = 0.0
        self._distortedFieldOfView = 0.0
        self._baseline = 0.0
        self._screenHalfHeight = 0.0
        self._screenHalfWidth = 0.0
        self._disparityLimit = 0.0
        self._focalDistanceDifference = 0.0
        self._emissionRescalingFactor = 0.0

    @property
    def baseline(self):
        return self._baseline

    @property
    def disparityLimit(self):
        return self._disparityLimit

    @property
    def distortedFocalDistance(self):
        return self._distortedFocalDistance

    @property
    def screenHalfWidth(self):
        return self._screenHalfWidth

    @property
    def screenHalfHeight(self):
        return self._screenHalfHeight

    @property
    def emissionRescalingFactor(self):
        return self._emissionRescalingFactor

    @property
    def filmOffset00(self):
        return (-self.viewOffset00 / self._screenHalfWidth)

    @property
    def filmOffset01(self):
        return (-self.viewOffset01 / self._screenHalfWidth)

    @property
    def filmOffset02(self):
        return (-self.viewOffset02 / self._screenHalfWidth)

    @property
    def filmOffset03(self):
        return (-self.viewOffset03 / self._screenHalfWidth)

    @property
    def viewOffset00(self):
        return (self._emissionRescalingFactor * -0.24)

    @property
    def viewOffset01(self):
        return (self._emissionRescalingFactor * -0.08)

    @property
    def viewOffset02(self):
        return (self._emissionRescalingFactor * 0.08)

    @property
    def viewOffset03(self):
        return (self._emissionRescalingFactor * 0.24)

    @staticmethod
    def computeLeiaCamera(fieldOfView, focalDistance, baselineScaling, perspectiveScaling,
                            maxDisparity, deltaView, screenWidth, screenHeight, tileResX):

        lcam = LeiaCamera()
        lcam._distortedFocalDistance = focalDistance / perspectiveScaling
        lcam._distortedFieldOfView = math.atan(perspectiveScaling * math.tan(fieldOfView * math.pi / 360.0)) * 360.0 / math.pi
        lcam._baseline = deltaView * lcam._distortedFocalDistance * baselineScaling
        lcam._screenHalfHeight = focalDistance * math.tan(fieldOfView * math.pi / 360.0)
        lcam._screenHalfWidth = screenWidth / screenHeight * lcam._screenHalfHeight
        lcam._disparityLimit = 2.0 * maxDisparity * lcam._screenHalfWidth / tileResX
        lcam._focalDistanceDifference = focalDistance - lcam._distortedFocalDistance
        lcam._emissionRescalingFactor = baselineScaling * lcam._distortedFocalDistance

        return lcam

class LeiaCameraBounds(object):
    def __init__(self):
        super(LeiaCameraBounds, self).__init__()

        self._nearTopLeft = (0.0, 0.0, 0.0)
        self._nearTopRight = (0.0, 0.0, 0.0)
        self._nearBottomLeft = (0.0, 0.0, 0.0)
        self._nearBottomRight = (0.0, 0.0, 0.0)

        self._farTopLeft = (0.0, 0.0, 0.0)
        self._farTopRight = (0.0, 0.0, 0.0)
        self._farBottomLeft = (0.0, 0.0, 0.0)
        self._farBottomRight = (0.0, 0.0, 0.0)

        self._screenTopLeft = (0.0, 0.0, 0.0)
        self._screenTopRight = (0.0, 0.0, 0.0)
        self._screenBottomLeft = (0.0, 0.0, 0.0)
        self._screenBottomRight = (0.0, 0.0, 0.0)

    @property
    def screen(self):
        return ((self._screenTopLeft, self._screenTopRight, self._screenBottomRight, self._screenBottomLeft))

    @property
    def south(self):
        return ((self._nearTopLeft, self._nearTopRight, self._nearBottomRight, self._nearBottomLeft))

    @property
    def north(self):
        return ((self._farTopLeft, self._farTopRight, self._farBottomRight, self._farBottomLeft))

    @property
    def top(self):
        return ((self._nearTopLeft, self._nearTopRight, self._farTopRight, self._farTopLeft))

    @property
    def bottom(self):
        return ((self._nearBottomLeft, self._nearBottomRight, self._farBottomRight, self._farBottomLeft))

    @property
    def east(self):
        return ((self._nearTopRight, self._nearBottomRight, self._farBottomRight, self._farTopRight))

    @property
    def west(self):
        return ((self._nearTopLeft, self._nearBottomLeft, self._farBottomLeft, self._farTopLeft))

    @staticmethod
    def computeLeiaCameraBounds(screenHalfWidth, screenHalfHeight,
                                distortedFocalDistance, disparityLimit,
                                baseline, focalDistance):

        # added to correct camera z: see below
        focalDistance = -focalDistance
        distortedFocalDistance = -distortedFocalDistance

        lbounds = LeiaCameraBounds()

        lbounds._screenTopLeft = (-screenHalfWidth, screenHalfHeight, focalDistance)
        lbounds._screenTopRight = (screenHalfWidth, screenHalfHeight, focalDistance)
        lbounds._screenBottomLeft = (-screenHalfWidth, -screenHalfHeight, focalDistance)
        lbounds._screenBottomRight = (screenHalfWidth, -screenHalfHeight, focalDistance)

        # distortedNearZ = max(0.0, baseline * distortedFocalDistance / (baseline + disparityLimit))
        distortedNearZ = min(0.0, baseline * distortedFocalDistance / (baseline + disparityLimit))
        nearPlaneZ = distortedNearZ - distortedFocalDistance + focalDistance
        nearRatio = distortedNearZ / distortedFocalDistance

        lbounds._nearTopLeft = (-screenHalfWidth * nearRatio, screenHalfHeight * nearRatio, nearPlaneZ)
        lbounds._nearTopRight = (screenHalfWidth * nearRatio, screenHalfHeight * nearRatio, nearPlaneZ)
        lbounds._nearBottomLeft = (-screenHalfWidth * nearRatio, -screenHalfHeight * nearRatio, nearPlaneZ)
        lbounds._nearBottomRight = (screenHalfWidth * nearRatio, -screenHalfHeight * nearRatio, nearPlaneZ)

        distortedFarZ = baseline * distortedFocalDistance / (baseline - disparityLimit) if (baseline > disparityLimit) else 20000.0
        farPlaneZ = distortedFarZ - distortedFocalDistance + focalDistance
        farRatio = distortedFarZ / distortedFocalDistance

        lbounds._farTopLeft = (-screenHalfWidth * farRatio, screenHalfHeight * farRatio, farPlaneZ)
        lbounds._farTopRight = (screenHalfWidth * farRatio, screenHalfHeight * farRatio, farPlaneZ)
        lbounds._farBottomLeft = (-screenHalfWidth * farRatio, -screenHalfHeight * farRatio, farPlaneZ)
        lbounds._farBottomRight = (screenHalfWidth * farRatio, -screenHalfHeight * farRatio, farPlaneZ)

        return lbounds


def __createSlaveCamera(masterShape, leia, name, parent):
    slave = mc.camera()[0]
    slave = mc.parent(slave, parent)[0]
    slave = mc.rename(slave, name)
    slaveShape = mc.listRelatives(slave, path=True, shapes=True)[0]

    mc.setAttr(slave + '.renderable', 1)

    for attr in ['horizontalFilmAperture',
                'verticalFilmAperture',
                'focalLength',
                'lensSqueezeRatio',
                'fStop',
                'focusDistance',
                'shutterAngle',
                'cameraPrecompTemplate',
                'filmFit',
                'displayFilmGate',
                'displayResolution']:
        slaveAttr = slaveShape + '.' + attr
        mc.connectAttr(masterShape + '.' + attr, slaveAttr)
        mc.setAttr(slaveAttr, keyable=False)

    for attr in ['nearClipPlane',
                'farClipPlane']:
        slaveAttr = slaveShape + '.' + attr
        leiaAttr = leia + '.' + attr + 'Out'
        mc.connectAttr(leiaAttr, slaveAttr)
        mc.setAttr(slaveAttr, keyable=False)

    for attr in ['scaleX', 'scaleY', 'scaleZ',
                'visibility',
                'centerOfInterest']:
        mc.setAttr(slave + '.' + attr, keyable=False)

    return slave

def __createFrustumNode(mainCam, parent, baseName):
    frustum = mc.createNode('LeiaCameraFrustum', name=baseName, parent=parent)
    for attr in ['localPositionX', 'localPositionY', 'localPositionZ',
                'localScaleX', 'localScaleY', 'localScaleZ']:
        mc.setAttr(frustum + '.' + attr, channelBox=False)

    for attr in ['displayNearClip', 'displayFarClip', 'displayFrustum',
               'zeroParallaxPlane',
               'zeroParallaxTransparency',
               'zeroParallaxColor',
               'safeViewingVolume',
               'safeVolumeTransparency',
               'safeVolumeColor',
               'safeStereo',
               'zeroParallax'] :
        mc.connectAttr(mainCam + '.' + attr, frustum + '.' + attr)

    return frustum

def __disableTransformNode(xform, ignored=[]):
    for attr in ['translateX', 'translateY', 'translateZ',
                    'rotateX', 'rotateY', 'rotateZ',
                    'scaleX', 'scaleY', 'scaleZ']:
        if not attr in ignored:
            mc.setAttr(xform + "." + attr, lock=True)

def createLeiaCameraRig(baseName='leiaCamera'):
    root = mc.createNode('transform', name=baseName)
    rootName = root.split('|')[-1]

    leia = mc.createNode('LeiaCamera', parent=root, name=root + "Shape")

    centerCam = mc.camera()[0]
    centerCam = mc.rename(centerCam, root + '_Center')
    mc.connectAttr(centerCam + ".message", leia + ".centerCamera")

    centerCamShape = mc.listRelatives(centerCam, path=True, shapes=True)[0]
    mc.connectAttr(leia + ".horizontalFilmAperture", centerCamShape + ".horizontalFilmAperture")
    mc.connectAttr(leia + ".verticalFilmAperture", centerCamShape + ".verticalFilmAperture")
    mc.connectAttr(leia + ".nearClipPlane", centerCamShape + ".nearClipPlane")
    mc.connectAttr(leia + ".farClipPlane", centerCamShape + ".farClipPlane")
    mc.connectAttr(leia + ".focalLength", centerCamShape + ".focalLength")

    mc.setAttr(centerCamShape + '.renderable', 0)
    mc.setAttr(centerCamShape + '.visibility', 0)

    mc.parent(centerCam, root)

    view00 = __createSlaveCamera(centerCamShape, leia, root + '_view00', root)
    view01 = __createSlaveCamera(centerCamShape, leia, root + '_view01', root)
    view02 = __createSlaveCamera(centerCamShape, leia, root + '_view02', root)
    view03 = __createSlaveCamera(centerCamShape, leia, root + '_view03', root)

    mc.connectAttr(leia + '.viewOffset00', view00 + '.translateX')
    mc.connectAttr(leia + '.viewOffset01', view01 + '.translateX')
    mc.connectAttr(leia + '.viewOffset02', view02 + '.translateX')
    mc.connectAttr(leia + '.viewOffset03', view03 + '.translateX')

    mc.connectAttr(leia + '.filmOffset00', view00 + '.hfo')
    mc.connectAttr(leia + '.filmOffset01', view01 + '.hfo')
    mc.connectAttr(leia + '.filmOffset02', view02 + '.hfo')
    mc.connectAttr(leia + '.filmOffset03', view03 + '.hfo')

    __disableTransformNode(centerCam)
    __disableTransformNode(view00)
    __disableTransformNode(view01)
    __disableTransformNode(view02)
    __disableTransformNode(view03)

    mc.select(root)
    return root

def convertFovToFocalLength(fov, verticalFilmAperture):
    return (verticalFilmAperture / (2.0 * math.tan(0.5 * fieldOfView * math.pi / 180)))

def convertFocalLengthToFov(focalLength, verticalFilmAperture):
    return (2.0 * math.atan((0.5 * verticalFilmAperture) / (focalLength * 0.03937)) * 57.29578)

def computeLeiaCamera(fieldOfView, focalDistance, baselineScaling, perspectiveScaling,
                        maxDisparity, deltaView, screenWidth, screenHeight, tileResX):

    return LeiaCamera.computeLeiaCamera(fieldOfView, focalDistance, baselineScaling, perspectiveScaling,
                                            maxDisparity, deltaView, screenWidth, screenHeight, tileResX)

def computeLeiaCameraBounds(screenHalfWidth, screenHalfHeight, distortedFocalDistance,
                                                disparityLimit, baseline, focalDistance):

    return LeiaCameraBounds.computeLeiaCameraBounds(screenHalfWidth, screenHalfHeight, distortedFocalDistance,
                                                                        disparityLimit, baseline, focalDistance)