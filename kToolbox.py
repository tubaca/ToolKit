# This Python file uses the following encoding: utf-8
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from krita import *

DOCKER_NAME = 'KToolbox'
DOCKER_ID = 'kToolbox'

highlightedBack = QColor(86, 128, 194)
back = QColor(49, 49, 49)

class Tool(QToolButton):

    def __init__(self, name, text, icon, category, priority):
        super().__init__()
        self.name = name
        self.text = text
        self.icon = icon
        self.category = category
        self.priority = priority

ToolList = [

Tool("KisToolTransform", "Transform Tool", "krita_tool_transform", "Transform", "0"),
Tool("KritaTransform/KisToolMove", "Move Tool", "krita_tool_move", "Transform", "1"),
Tool("KisToolCrop", "Crop Tool", "tool_crop", "Transform", "2"),

Tool("KoInteractionTool_ID", "Select Shape", "select", "Vector", "0"),
Tool("SvgTextTool", "Text Tool", "draw-text", "Vector", "1"),
Tool("PathTool", "Edit Shape Tool", "shape_handling", "Vector", "2"),
Tool("KarbonCalligraphyTool", "Calligraphy", "calligraphy", "Vector", "3"),

Tool("KritaShape/KisToolBrush", "Freehand Brush", "krita_tool_freehand", "Paint", "0"),
Tool("KritaShape/KisToolDyna", "Dynamic Brush", "krita_tool_dyna", "Paint", "1"),
Tool("KritaShape/KisToolMultiBrush", "Multibrush", "krita_tool_multihand", "Paint", "2"),
Tool("KritaShape/KisToolSmartPatch", "Smart Patch Tool", "krita_tool_smart_patch", "Paint", "3"),
Tool("KisToolPencil", "Freehand Path", "krita_tool_freehandvector", "Paint", "4"),

Tool("KritaFill/KisToolFill", "Fill Tool", "krita_tool_color_fill", "Fill", "0"),
Tool("KritaSelected/KisToolColorPicker", "Color Picker", "krita_tool_color_picker", "Fill", "1"),
Tool("KritaShape/KisToolLazyBrush", "Colorize Brush", "krita_tool_lazybrush", "Fill", "2"),
Tool("KritaFill/KisToolGradient", "Gradient Tool", "krita_tool_gradient", "Fill", "3"),

Tool("KritaShape/KisToolRectangle", "Rectangle Tool", "krita_tool_rectangle", "Shape", "0"),
Tool("KritaShape/KisToolLine", "Line Tool", "krita_tool_line", "Shape", "1"),
Tool("KritaShape/KisToolEllipse", "Ellipse Tool", "krita_tool_ellipse", "Shape", "2"),
Tool("KisToolPolygon", "Polygon Tool", "krita_tool_polygon", "Shape", "3"),
Tool("KisToolPolyline", "Polyline Tool", "polyline", "Shape", "4"),
Tool("KisToolPath", "Bezier Tool", "krita_draw_path", "Shape", "5"),

Tool("KisToolSelectRectangular", "Rectangular Selection", "tool_rect_selection", "Select", "0"),
Tool("KisToolSelectElliptical", "Elliptical Selection", "tool_elliptical_selection", "Select", "1"),
Tool("KisToolSelectPolygonal", "Polygonal Selection", "tool_polygonal_selection", "Select", "2"),
Tool("KisToolSelectPath", "Bezier Selection", "tool_path_selection", "Select", "3"),

Tool("KisToolSelectOutline", "Outline Selection", "tool_outline_selection", "AutoSelect", "0"),
Tool("KisToolSelectContiguous", "Contiguous Selection", "tool_contiguous_selection", "AutoSelect", "1"),
Tool("KisToolSelectSimilar", "Similar Selection", "tool_similar_selection", "AutoSelect", "2"),
Tool("KisToolSelectMagnetic", "Magnetic Selection", "tool_magnetic_selection", "AutoSelect", "3"),

Tool("ToolReferenceImages", "Reference Image Tool", "krita_tool_reference_images", "Reference", "0"),
Tool("KisAssistantTool", "Assistant Tool", "krita_tool_assistant", "Reference", "1"),
Tool("KritaShape/KisToolMeasure", "Measure Tool", "krita_tool_measure", "Reference", "2"),

Tool("PanTool", "Pan", "tool_pan", "Navigation", "0"),
Tool("ZoomTool", "Zoom", "tool_zoom", "Navigation", "1"),

]

class ToolCategory:
    def __init__(self, name):
        self.name = name
        self.tools = {}

    def addTool(self, tool):
        self.tools[tool.name] = tool

class ToolboxDocker(QDockWidget):

    def __init__(self):
        super(ToolboxDocker, self).__init__()

        self.categories = {"Transform": ToolCategory("Transform"),
                           "Vector": ToolCategory("Vector"),
                           "Paint": ToolCategory("Paint"),
                           "Shape": ToolCategory("Shape"),
                           "Select": ToolCategory("Select"),
                           "AutoSelect": ToolCategory("AutoSelect"),
                           "Reference": ToolCategory("Reference"),
                           "Navigation": ToolCategory("Navigation")}

        widget = QWidget()
        layout = QVBoxLayout()
        widget.setLayout(layout)
        self.setWindowTitle(i18n("Tool Kit"))

        for Tool in ToolList:
            Tool.setIconSize(QSize(24, 24))
            Tool.setIcon(Application.icon(Tool.icon))
            Tool.setObjectName(Tool.name)
            Tool.setToolTip(i18n(Tool.text))
            Tool.clicked.connect(self.activateTool)

            layout.addWidget(Tool)

        self.setWidget(widget)

    @pyqtSlot()
    def on_click(self):
        self.connect.paintEvent

        toolbar.actions.triggered.connect(self.on_click)

        def paintEvent(self, e):
            qp = QPainter()
            qp.begin(self)
            self.drawRectangles(qp)
            qp.end()

        def drawRectangles(self, qp):
            qp.setPen(highlightedBack)

            qp.setBrush(highlightedBack)
            qp.drawRect(10, 15, 90, 60)

    def temptopLeft(self, event):
        tempTopLeft = QPoint.event.rect().topLeft();

    def activateTool(self):
        actionName = self.sender().objectName();
        ac = Application.action(actionName)
        print(actionName, ac)
        if ac:
            ac.trigger()

    def canvasChanged(self, canvas):
        pass

instance = Krita.instance()
dock_widget_factory = DockWidgetFactory(DOCKER_ID,
                                        DockWidgetFactoryBase.DockRight,
                                        ToolboxDocker)

instance.addDockWidgetFactory(dock_widget_factory)
