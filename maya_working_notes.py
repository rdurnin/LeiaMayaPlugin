
(horizontalFilmoffset.x * 25.4) / cameraAperture.x (mm) * 2.0 = matrix[2,0]

2.0 * horizontalFilmoffset.x / cameraAperture.x (in) = matrix[2,0]
horizontalFilmoffset.x = matrix[2,0] * cameraAperture.x (in) / 2.0

import maya.cmds as mc
import maya.OpenMaya as OpenMaya

#cameraName = "leiaCamera_view01"
cameraName = "camera1"
#cameraName = "leiaCamera_Center"

selectionList = OpenMaya.MSelectionList()
objDagPath = OpenMaya.MDagPath()
selectionList.add(cameraName)
selectionList.getDagPath(0, objDagPath)
camera = OpenMaya.MFnCamera(objDagPath)

projMatrix = camera.projectionMatrix()
     
for x in xrange(0, 4):
    print(round(projMatrix(0, x), 3),
          round(projMatrix(1, x), 3),
          round(projMatrix(2, x), 3),
          round(projMatrix(3, x), 3))
          
print camera.horizontalFilmOffset()