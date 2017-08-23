
import math
import maya.cmds as mc

class LeiaCamera(object):
    def __init__(self):
        super(LeiaCamera, self).__init__()

        self._baseline = 0.0
        self._disparityLimit = 0.0
        self._normalizedShift = 0.0
        self._nearZ = 0.0
        self._nearHalfHeight = 0.0
        self._nearHalfWidth = 0.0
        self._screenZ = 0.0
        self._screenHalfHeight = 0.0
        self._screenHalfWidth = 0.0
        self._farZ = 0.0
        self._farHalfHeight = 0.0
        self._farHalfWidth = 0.0

    @property
    def baseline(self):
        return self._baseline

    @property
    def disparityLimit(self):
        return self._disparityLimit

    @property
    def nearZ(self):
        return self._nearZ

    @property
    def nearHalfWidth(self):
        return self._nearHalfWidth

    @property
    def nearHalfHeight(self):
        return self._nearHalfHeight

    @property
    def screenZ(self):
        return self._screenZ

    @property
    def screenHalfWidth(self):
        return self._screenHalfWidth

    @property
    def screenHalfHeight(self):
        return self._screenHalfHeight

    @property
    def farZ(self):
        return self._farZ

    @property
    def farHalfWidth(self):
        return self._farHalfWidth

    @property
    def farHalfHeight(self):
        return self._farHalfHeight

    @property
    def filmOffset00(self):
        return (-self.viewOffset00 * self._normalizedShift)

    @property
    def filmOffset01(self):
        return (-self.viewOffset01 * self._normalizedShift)

    @property
    def filmOffset02(self):
        return (-self.viewOffset02 * self._normalizedShift)

    @property
    def filmOffset03(self):
        return (-self.viewOffset03 * self._normalizedShift)

    @property
    def viewOffset00(self):
        return (self._baseline * -1.5)

    @property
    def viewOffset01(self):
        return (self._baseline * -0.5)

    @property
    def viewOffset02(self):
        return (self._baseline * 0.5)

    @property
    def viewOffset03(self):
        return (self._baseline * 1.5)

    @staticmethod
    def computeLeiaCamera(horizontalFilmAperture, focalLength, focalDistance, baselineScaling,
                                    maxDisparity, deltaView, screenWidth, screenHeight, tileResX):

        lcam = LeiaCamera()
        lcam._baseline = deltaView * focalDistance * baselineScaling
        lcam._normalizedShift = focalLength / (25.4 * focalDistance)

        lcam._screenZ = focalDistance
        lcam._screenHalfWidth = 25.4 * horizontalFilmAperture * focalDistance / (2.0 * focalLength)
        lcam._screenHalfHeight = lcam._screenHalfWidth / (screenWidth / screenHeight)

        lcam._disparityLimit = 2.0 * maxDisparity * lcam._screenHalfWidth / tileResX

        lcam._nearZ = -(max(0.0, lcam._baseline * focalDistance / (lcam._baseline + lcam._disparityLimit)))
        lcam._nearHalfWidth = 25.4 * horizontalFilmAperture * lcam._nearZ / (2.0 * focalLength)
        lcam._nearHalfHeight = lcam._nearHalfWidth / (screenWidth / screenHeight)

        lcam._farZ = -(lcam._baseline * focalDistance / (lcam._baseline - lcam._disparityLimit) if (lcam._baseline > lcam._disparityLimit) else 20000.0)
        lcam._farHalfWidth = 25.4 * horizontalFilmAperture * lcam._farZ / (2.0 * focalLength)
        lcam._farHalfHeight = lcam._farHalfWidth / (screenWidth / screenHeight)

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
    def computeLeiaCameraBounds(nearHalfWidth, nearHalfHeight, nearZ,
                                screenHalfWidth, screenHalfHeight, screenZ,
                                farHalfWidth, farHalfHeight, farZ):

        lbounds = LeiaCameraBounds()

        lbounds._nearTopLeft = (-nearHalfWidth, nearHalfHeight, nearZ)
        lbounds._nearTopRight = (nearHalfWidth, nearHalfHeight, nearZ)
        lbounds._nearBottomLeft = (-nearHalfWidth, -nearHalfHeight, nearZ)
        lbounds._nearBottomRight = (nearHalfWidth, -nearHalfHeight, nearZ)

        lbounds._screenTopLeft = (-screenHalfWidth, screenHalfHeight, -screenZ)
        lbounds._screenTopRight = (screenHalfWidth, screenHalfHeight, -screenZ)
        lbounds._screenBottomLeft = (-screenHalfWidth, -screenHalfHeight, -screenZ)
        lbounds._screenBottomRight = (screenHalfWidth, -screenHalfHeight, -screenZ)

        lbounds._farTopLeft = (-farHalfWidth, farHalfHeight, farZ)
        lbounds._farTopRight = (farHalfWidth, farHalfHeight, farZ)
        lbounds._farBottomLeft = (-farHalfWidth, -farHalfHeight, farZ)
        lbounds._farBottomRight = (farHalfWidth, -farHalfHeight, farZ)

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
        leiaAttr = leia + '.' + attr
        mc.connectAttr(leiaAttr, slaveAttr)
        mc.setAttr(slaveAttr, keyable=False)

    for attr in ['scaleX', 'scaleY', 'scaleZ',
                'visibility',
                'centerOfInterest']:
        mc.setAttr(slave + '.' + attr, keyable=False)

    return slave

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

def computeLeiaCamera(horizontalFilmAperture, focalLength, focalDistance, baselineScaling,
                                maxDisparity, deltaView, screenWidth, screenHeight, tileResX):

    return LeiaCamera.computeLeiaCamera(horizontalFilmAperture, focalLength, focalDistance, baselineScaling,
                                                    maxDisparity, deltaView, screenWidth, screenHeight, tileResX)

def computeLeiaCameraBounds(nearHalfWidth, nearHalfHeight, nearZ,
                            screenHalfWidth, screenHalfHeight, screenZ,
                            farHalfWidth, farHalfHeight, farZ):

    return LeiaCameraBounds.computeLeiaCameraBounds(nearHalfWidth, nearHalfHeight, nearZ,
                                                    screenHalfWidth, screenHalfHeight, screenZ,
                                                    farHalfWidth, farHalfHeight, farZ)
