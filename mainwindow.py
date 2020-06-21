# This Python file uses the following encoding: utf-8
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from krita import *

#This is the code in question:
class Tool():

    def __init__(self, action, name, shortcut):

        self.action = action
        self.text = name
        self.shortcut = shortcut

currentToolList = []

transformTool = Tool("KisToolTransform", "Transform", "(Ctrl + T)")
moveTool = Tool("KisToolMove", "Move", "(T)")
cropTool = Tool("KisToolCrop", "Crop", "(C)")
currentToolList.append(transformTool)


shapeSelectTool = Tool("InteractionTool", "Shape Select", "(V)")
editShapesTool = Tool("VectorTool", "Edit Shapes", "(T)")
#textTool = Tool("KisToolText", "Text", "(T)")
calligraphyTool = Tool("KarbonCalligraphyTool", "Calligraphy", "(T)")
currentToolList.append(shapeSelectTool)

#add actions below

brushTool = Tool("KisToolCrop", "Brush", "(T)")
dynamicBrushTool = Tool("KisToolCrop", "Dynamic Brush", "(T)")
multiBrushTool = Tool("KisToolCrop", "Multi Brush", "(T)")
smartPatchTool = Tool("KisToolCrop", "Smart Patch", "(T)")
currentToolList.append(brushTool)

fillTool = Tool("KisToolCrop", "Fill", "(T)")
colorPicker = Tool("KisToolCrop", "Color Picker", "(T)")
lazyBrushTool = Tool("KisToolCrop", "Lazy Brush", "(T)")
gradientTool = Tool("KisToolCrop", "Gradient", "(T)")
currentToolList.append(fillTool)

rectangleTool = Tool("KisToolCrop", "Rectangle", "(T)")
lineTool = Tool("KisToolCrop", "Line", "(T)")
freehandTool = Tool("KisToolCrop", "Freehand", "(T)")
ellipseTool = Tool("KisToolCrop", "Ellipse", "(T)")
polylineTool = Tool("KisToolCrop", "Polygon", "(T)")
pathTool = Tool("KisToolCrop", "Path", "(T)")
currentToolList.append(rectangleTool)

rectangularMarqueeTool = Tool("KisToolCrop", "Rectangular Selection", "(T)")
circularMarqueeTool = Tool("KisToolCrop", "Elliptical Selection", "(T)")
polygonalLasso = Tool("KisToolCrop", "Polygonal Selection", "(T)")
lassoTool = Tool("KisToolCrop", "Freehand Selection", "(T)")
currentToolList.append(rectangularMarqueeTool)

contiguousSelectionTool = Tool("KisToolCrop", "Contiguous Selection", "(T)")
similarSelectionTool = Tool("KisToolCrop", "Similar Selection", "(T)")
magneticLasso = Tool("KisToolCrop", "Magnetic Selection", "(T)")
bezierCurveLasso = Tool("KisToolCrop", "Path Selection", "(T)")
currentToolList.append(contiguousSelectionTool)

referenceImagesTool = Tool("KisToolCrop", "Reference Images", "(T)")
assistantTool = Tool("KisToolCrop", "Assistants", "(T)")
measureTool = Tool("KisToolCrop", "Measure", "(T)")
currentToolList.append(referenceImagesTool)

panTool = Tool("KisToolCrop", "Pan", "(T)")
zoomTool = Tool("KisToolCrop", "Zoom", "(T)")
currentToolList.append(panTool)

print(currentToolList)
