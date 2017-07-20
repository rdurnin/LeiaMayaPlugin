
import math
import maya.cmds as mc
import maya.mel as mm

def renderLeiaCamera(camera='leiaCamera'):
    print("leiaRender: renderLeiaCamera: Called")
    try:
        leiaViews = [str(child) for child in mc.listRelatives(camera, children=True, type="transform")]
    except:
        raise

    for leiaView in leiaViews:
        try:
            print("leiaRender: renderLeiaCamera: leiaView: " + leiaView)
            if (mc.getAttr(leiaView + ".renderable")):
                mm.eval("renderWindowRenderCamera render renderView %s;" % leiaView)
        except:
            raise