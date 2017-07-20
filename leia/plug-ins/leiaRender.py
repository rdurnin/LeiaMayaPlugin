
import maya.api.OpenMaya as OpenMaya

kPluginCommandName = "LeiaRender"

def info(message):
    fullMsg = "%s: %s" % (kPluginCommandName, message)
    OpenMaya.MGlobal.displayInfo(fullMsg)

def warn(message):
    fullMsg = "%s: %s" % (kPluginCommandName, message)
    OpenMaya.MGlobal.displayWarning(fullMsg)

def error(message):
    fullMsg = "%s: %s" % (kPluginCommandName, message)
    OpenMaya.MGlobal.displayError(fullMsg)

def initializePlugin(mobject):
    info("Plug-in initialized")

def uninitializePlugin(mobject):
    info("Plug-in uninitialized")
