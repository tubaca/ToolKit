# This Python file uses the following encoding: utf-8
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from krita import *
from . import kToolbox

class Tool(object):
    activeTools = []
    subTools = []

    def __init__(self, action, name, shortcut):

        self.action = action
        self.name = name
        self.shortcut = shortcut

    def addSubTool(self, Tool):

        Tool.temp = subTools[index]
        Tool.subTools.append(Tool)
        pass

transformTool = Tool("KisToolTransform", "Transform", "(Ctrl + T)")
moveTool = Tool("KisToolMove", "Move", "(T)")
cropTool = Tool("KisToolCrop", "Crop", "(C)")
transformTool.addSubTool(moveTool)
transformTool.addSubTool(cropTool)

shapeSelectTool = Tool("InteractionTool", "Shape Select", "(V)")
editShapesTool = Tool("VectorTool", "Edit Shapes", "(T)")
textTool = Tool("Text", "(T)")
calligraphyTool = Tool("KarbonCalligraphyTool", "Calligraphy", "(T)")
shapeSelectTool.addSubTool(editShapesTool)
shapeSelectTool.addSubTool(textTool)
shapeSelectTool.addSubTool(calligraphyTool)

#add actions below

brushTool = Tool("Brush", "(T)")
dynamicBrushTool = Tool("Dynamic Brush", "(T)")
multiBrushTool = Tool("Multi Brush", "(T)")
Tool.smartPatchTool("Smart Patch", "(T)")
brushTool.addSubTool(dynamicBrushTool)
brushTool.addSubTool(multiBrushTool)
brushTool.addSubTool(smartPatchTool)

fillTool = Tool("Fill", "(T)")
colorPicker = Tool("Color Picker", "(T)")
lazyBrushTool = Tool("Lazy Brush", "(T)")
gradientTool = Tool("Gradient", "(T)")
fillTool.addSubTool(colorPicker)
fillTool.addSubTool(lazyBrushTool)
fillTool.addSubTool(gradientTool)

rectangleTool = Tool("Rectangle", "(T)")
lineTool = Tool("Line", "(T)")
freehandTool = Tool("Freehand", "(T)")
ellipseTool = Tool("Ellipse", "(T)")
polylineTool = Tool("Polygon", "(T)")
pathTool = Tool("Path", "(T)")
rectangleTool.addSubTool(lineTool)
rectangleTool.addSubTool(ellipseTool)
rectangleTool.addSubTool(polylineTool)
rectangleTool.addSubTool(freehandTool)
rectangleTool.addSubTool(pathTool)

rectangularMarqueeTool = Tool("Rectangular Selection", "(T)")
circularMarqueeTool = Tool("Elliptical Selection", "(T)")
polygonalLasso = Tool("Polygonal Selection", "(T)")
lassoTool = Tool("Freehand Selection", "(T)")
rectangularMarqueeTool.addSubTool(circularMarqueeTool)
rectangularMarqueeTool.addSubTool(polygonalLasso)
rectangularMarqueeTool.addSubTool(lassoTool)

contiguousSelectionTool = Tool("Contiguous Selection", "(T)")
similarSelectionTool = Tool("Similar Selection", "(T)")
magneticLasso = Tool("Magnetic Selection", "(T)")
bezierCurveLasso = Tool("Path Selection", "(T)")
contiguousSelectionTool.addSubTool(similarSelectionTool)
contiguousSelectionTool.addSubTool(polygonalLasso)
contiguousSelectionTool.addSubTool(magneticLasso)
contiguousSelectionTool.addSubTool(bezierCurveLasso)

referenceImagesTool = Tool("Reference Images", "(T)")
assistantTool = Tool("Assistants", "(T)")
measureTool = Tool("Measure", "(T)")
referenceImagesTool.addSubTool(assistantTool)
referenceImagesTool.addSubTool(measureTool)

panTool = Tool("Pan", "(T)")
zoomTool = Tool("Zoom", "(T)")
panTool.addSubTool(zoomTool)


