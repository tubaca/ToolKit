# This Python file uses the following encoding: utf-8
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from krita import *
from collections import namedtuple
from . import kToolbox

class ToolSlot(object):
    __slots__ = ['currentToolList']

    def __init__(self, t):
        self.currentToolList = t

    def currentTool(QAction):
        t.append()
        pass
#This is the code in question:
class Tool(object):

    def __init__(self, action, name, shortcut):

        self.action = action
        self.text = name
        self.shortcut = shortcut

Tool(transformTool) = "KisToolTransform", "Transform", "(Ctrl + T)"
moveTool = Tool("KisToolMove", "Move", "(T)")
cropTool = Tool("KisToolCrop", "Crop", "(C)")
currentTool(transformTool)


shapeSelectTool = Tool("InteractionTool", "Shape Select", "(V)")
editShapesTool = Tool("VectorTool", "Edit Shapes", "(T)")
textTool = Tool("Text", "(T)")
calligraphyTool = Tool("KarbonCalligraphyTool", "Calligraphy", "(T)")
currentTool(shapeSelectTool)

#add actions below

brushTool = Tool("Brush", "(T)")
dynamicBrushTool = Tool("Dynamic Brush", "(T)")
multiBrushTool = Tool("Multi Brush", "(T)")
Tool.smartPatchTool("Smart Patch", "(T)")
currentTool(brushTool)

fillTool = Tool("Fill", "(T)")
colorPicker = Tool("Color Picker", "(T)")
lazyBrushTool = Tool("Lazy Brush", "(T)")
gradientTool = Tool("Gradient", "(T)")
currentTool(fillTool)

rectangleTool = Tool("Rectangle", "(T)")
lineTool = Tool("Line", "(T)")
freehandTool = Tool("Freehand", "(T)")
ellipseTool = Tool("Ellipse", "(T)")
polylineTool = Tool("Polygon", "(T)")
pathTool = Tool("Path", "(T)")
currentTool(rectangleTool)

rectangularMarqueeTool = Tool("Rectangular Selection", "(T)")
circularMarqueeTool = Tool("Elliptical Selection", "(T)")
polygonalLasso = Tool("Polygonal Selection", "(T)")
lassoTool = Tool("Freehand Selection", "(T)")
currentTool(rectangularMarqueeTool)

contiguousSelectionTool = Tool("Contiguous Selection", "(T)")
similarSelectionTool = Tool("Similar Selection", "(T)")
magneticLasso = Tool("Magnetic Selection", "(T)")
bezierCurveLasso = Tool("Path Selection", "(T)")
currentTool(contiguousSelectionTool)

referenceImagesTool = Tool("Reference Images", "(T)")
assistantTool = Tool("Assistants", "(T)")
measureTool = Tool("Measure", "(T)")
currentTool(referenceImagesTool)

panTool = Tool("Pan", "(T)")
zoomTool = Tool("Zoom", "(T)")
currentTool(panTool)




