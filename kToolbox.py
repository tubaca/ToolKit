# This Python file uses the following encoding: utf-8
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from krita import *

highlightedBack = QColor(86, 128, 194)
back = QColor(49, 49, 49)

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

class kToolBox(QDockWidget):

    def __init__(self):
        super(kToolBox, self).__init__()

        self.setWindowTitle(i18n("KToolBox"))

        mainWidget = QWidget(self)
        toolbar = QToolBar(self)
        layout = QGridLayout()

        self.setWidget(mainWidget)
        mainWidget.setLayout(layout)
        layout.addWidget(toolbar)

        toolbar.setOrientation(Qt.Vertical)

        for Tool in currentToolList:
            toolbar.addAction(Tool.action)
            print(Tool.text)

        Tool.action = Krita.instance().action("")

    @pyqtSlot()
    def on_click(self):
        self.connect.paintEvent.drawRectangles(qp)

        button.clicked.connect(self.on_click)

        def paintEvent(self, e):
            qp = QPainter()
            qp.begin(self)
            self.drawRectangles(qp)
            qp.end()

        def drawRectangles(self, qp):
            qp.setPen(highlightedBack)

            qp.setBrush(highlightedBack)
            qp.drawRect(10, 15, 90, 60)

    def canvasChanged(self, canvas):
        pass

    def temptopLeft(self, event):
        tempTopLeft = QPoint.event.rect().topLeft();

    def orientationChange(self):
        if toolbar.orientationChanged(i):
            toolbar.setOrientation(i)
            pass

Krita.instance().addDockWidgetFactory(DockWidgetFactory("kToolBox", DockWidgetFactoryBase.DockRight, kToolBox))


