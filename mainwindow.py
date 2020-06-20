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

Tool.transformTool = ("KisToolTransform", "Transform", "(Ctrl + T)")
Tool.moveTool = ("KisToolMove", "Move", "(T)")
Tool.cropTool = ("KisToolCrop", "Crop", "(C)")
transformTool.addSubTool(moveTool)
transformTool.addSubTool(cropTool)

Tool.shapeSelectTool = ("InteractionTool", "Shape Select", "(V)")
Tool.editShapesTool = ("VectorTool", "Edit Shapes", "(T)")
Tool.textTool = ("Text", "(T)")
Tool.calligraphyTool = ("KarbonCalligraphyTool", "Calligraphy", "(T)")
shapeSelectTool.addSubTool(editShapesTool)
shapeSelectTool.addSubTool(textTool)
shapeSelectTool.addSubTool(calligraphyTool)

#add actions below

Tool.brushTool("Brush", "(T)")
Tool.dynamicBrushTool("Dynamic Brush", "(T)")
Tool.multiBrushTool("Multi Brush", "(T)")
Tool.smartPatchTool("Smart Patch", "(T)")
brushTool.addSubTool(dynamicBrushTool)
brushTool.addSubTool(multiBrushTool)
brushTool.addSubTool(smartPatchTool)

Tool.fillTool("Fill", "(T)")
Tool.colorPicker("Color Picker", "(T)")
Tool.lazyBrushTool("Lazy Brush", "(T)")
Tool.gradientTool("Gradient", "(T)")
fillTool.addSubTool(colorPicker)
fillTool.addSubTool(lazyBrushTool)
fillTool.addSubTool(gradientTool)

Tool.rectangleTool("Rectangle", "(T)")
Tool.lineTool("Line", "(T)")
Tool.freehandTool("Freehand", "(T)")
Tool.ellipseTool("Ellipse", "(T)")
Tool.polylineTool("Polygon", "(T)")
Tool.pathTool("Path", "(T)")
rectangleTool.addSubTool(lineTool)
rectangleTool.addSubTool(ellipseTool)
rectangleTool.addSubTool(polylineTool)
rectangleTool.addSubTool(freehandTool)
rectangleTool.addSubTool(pathTool)

Tool.rectangularMarqueeTool("Rectangular Selection", "(T)")
Tool.circularMarqueeTool("Elliptical Selection", "(T)")
Tool.polygonalLasso("Polygonal Selection", "(T)")
Tool.lassoTool("Freehand Selection", "(T)")
rectangularMarqueeTool.addSubTool(circularMarqueeTool)
rectangularMarqueeTool.addSubTool(polygonalLasso)
rectangularMarqueeTool.addSubTool(lassoTool)

Tool.contiguousSelectionTool("Contiguous Selection", "(T)")
Tool.similarSelectionTool("Similar Selection", "(T)")
Tool.magneticLasso("Magnetic Selection", "(T)")
Tool.bezierCurveLasso("Path Selection", "(T)")
contiguousSelectionTool.addSubTool(similarSelectionTool)
contiguousSelectionTool.addSubTool(polygonalLasso)
contiguousSelectionTool.addSubTool(magneticLasso)
contiguousSelectionTool.addSubTool(bezierCurveLasso)

Tool.referenceImagesTool("Reference Images", "(T)")
Tool.assistantTool("Assistants", "(T)")
Tool.measureTool("Measure", "(T)")
referenceImagesTool.addSubTool(assistantTool)
referenceImagesTool.addSubTool(measureTool)

Tool.panTool("Pan", "(T)")
Tool.zoomTool("Zoom", "(T)")
panTool.addSubTool(zoomTool)


