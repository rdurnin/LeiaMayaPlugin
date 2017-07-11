
import maya.cmds as mc

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
    root = mc.createNode('LeiaCameraTransform', name=baseName)
    rootName = root.split('|')[-1]

    leia = mc.createNode('LeiaCamera', name=root + "Shape")
    mc.connectAttr(leia + ".message", root + ".leiaCamera")

    centerCam = mc.camera()[0]
    centerCam = mc.rename(centerCam, baseName + '_Center')
    mc.connectAttr(centerCam + ".message", leia + ".centerCamera")

    centerCamShape = mc.listRelatives(centerCam, path=True, shapes=True)[0]
    mc.connectAttr(leia + ".horizontalFilmAperture", centerCamShape + ".horizontalFilmAperture")
    mc.connectAttr(leia + ".verticalFilmAperture", centerCamShape + ".verticalFilmAperture")
    mc.connectAttr(leia + ".nearClipPlane", centerCamShape + ".nearClipPlane")
    mc.connectAttr(leia + ".farClipPlane", centerCamShape + ".farClipPlane")
    mc.connectAttr(leia + ".focalLength", centerCamShape + ".focalLength")

    mc.setAttr(centerCamShape + '.renderable', 0)
    mc.setAttr(centerCamShape + '.visibility', 0)

    xform_track = mc.createNode('transform', name='cameraTrack')
    mc.parent(xform_track, root)
    mc.connectAttr(root + ".cameraTrack0", xform_track + ".translateX")
    mc.connectAttr(root + ".cameraTrack1", xform_track + ".translateZ")
    mc.setAttr(xform_track + ".translateX", keyable=False)
    mc.setAttr(xform_track + ".translateZ", keyable=False)
    __disableTransformNode(xform_track, ['translateX', 'translateZ'])

    xform_roll = mc.createNode('transform', name='cameraRoll')
    mc.parent(xform_roll, xform_track)
    mc.connectAttr(root + ".cameraRoll", xform_roll + ".rotateZ")
    mc.setAttr(xform_roll + ".rotateZ", keyable=False)
    __disableTransformNode(xform_roll, ['rotateZ'])

    xform_tilt = mc.createNode('transform', name='cameraTilt')
    mc.parent(xform_tilt, xform_roll)
    mc.connectAttr(root + ".cameraTilt", xform_tilt + ".rotateX")
    mc.setAttr(xform_tilt + ".rotateX", keyable=False)
    __disableTransformNode(xform_tilt, ['rotateX'])

    xform_pan = mc.createNode('transform', name='cameraPan')
    mc.parent(xform_pan, xform_tilt)
    mc.connectAttr(root + ".cameraPan", xform_pan + ".rotateY")
    mc.setAttr(xform_pan + ".rotateY", keyable=False)
    __disableTransformNode(xform_pan, ['rotateY'])

    mc.parent(centerCam, xform_pan)

    view00 = __createSlaveCamera(centerCamShape, leia, baseName + '_view00', xform_pan)
    view01 = __createSlaveCamera(centerCamShape, leia, baseName + '_view01', xform_pan)
    view02 = __createSlaveCamera(centerCamShape, leia, baseName + '_view02', xform_pan)
    view03 = __createSlaveCamera(centerCamShape, leia, baseName + '_view03', xform_pan)

    mc.connectAttr(leia + '.viewOffset00', view00 + '.translateX')
    mc.connectAttr(leia + '.viewOffset01', view01 + '.translateX')
    mc.connectAttr(leia + '.viewOffset02', view02 + '.translateX')
    mc.connectAttr(leia + '.viewOffset03', view03 + '.translateX')

    mc.connectAttr(leia + '.filmOffset00', view00 + '.hfo')
    mc.connectAttr(leia + '.filmOffset01', view01 + '.hfo')
    mc.connectAttr(leia + '.filmOffset02', view02 + '.hfo')
    mc.connectAttr(leia + '.filmOffset03', view03 + '.hfo')

    for attr in ['translate', 'rotate']:
        mc.setAttr(view00 + '.' + attr, lock=True)
        mc.setAttr(view01 + '.' + attr, lock=True)
        mc.setAttr(view02 + '.' + attr, lock=True)
        mc.setAttr(view03 + '.' + attr, lock=True)

    mc.select(root)
    return root
