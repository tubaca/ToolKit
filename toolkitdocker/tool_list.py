from PyQt5.QtWidgets import QToolButton
from PyQt5.QtGui import QPalette, QColor
import json
from os import path

class json_class:

    fileDir = path.dirname(path.realpath(__file__))

    def loadJSON(self):
        with open(self.fileDir + '/data.json') as jsonFile:
            data = json.load(jsonFile)
            return data

jsonMethod = json_class()

class ToolButton(QToolButton):


    def __init__(self, name, text, icon, category, isMain):
        super().__init__()
        self.name = name
        self.text = text
        self.icon = icon
        self.category = category
        self.isMain = isMain

        palette = QPalette()
        palette.setColor(QPalette.Button, QColor(74, 108, 134))
        self.setPalette(palette)

#    def mouseDoubleClickEvent(self, event):
#        super().mouseDoubleClickEvent(event)

#        if jsonMethod.loadJSON()["dblClickSubmenu"] == True:
#            self.setPopupMode(QToolButton.MenuButtonPopup)
#            self.menu().setVisible(True)

    def enterEvent(self, event):
        super().enterEvent(event)

        if len(Application.documents()) == 0: # disable buttons before document is visible
            self.setEnabled(False)
        else:
            self.setEnabled(True)


ToolList = [

ToolButton("KisToolTransform", "Transform Tool", "krita_tool_transform", "Transform", "1"),
ToolButton("KritaTransform/KisToolMove", "Move Tool", "krita_tool_move", "Transform", "0"),
ToolButton("KisToolCrop", "Crop Tool", "tool_crop", "Transform", "0"),

ToolButton("InteractionTool", "Select Shape", "select", "Vector", "1"),
ToolButton("SvgTextTool", "Text Tool", "draw-text", "Vector", "0"),
ToolButton("PathTool", "Edit Shape Tool", "shape_handling", "Vector", "0"),
ToolButton("KarbonCalligraphyTool", "Calligraphy", "calligraphy", "Vector", "0"),

ToolButton("KritaShape/KisToolBrush", "Freehand Brush", "krita_tool_freehand", "Paint", "1"),
ToolButton("KritaShape/KisToolDyna", "Dynamic Brush", "krita_tool_dyna", "Paint", "0"),
ToolButton("KritaShape/KisToolMultiBrush", "Multibrush", "krita_tool_multihand", "Paint", "0"),
ToolButton("KritaShape/KisToolSmartPatch", "Smart Patch Tool", "krita_tool_smart_patch", "Paint", "0"),
ToolButton("KisToolPencil", "Freehand Path", "krita_tool_freehandvector", "Paint", "0"),

ToolButton("KritaFill/KisToolFill", "Fill Tool", "krita_tool_color_fill", "Fill", "1"),
ToolButton("KritaSelected/KisToolColorPicker", "Color Picker", "krita_tool_color_picker", "Fill", "0"),
ToolButton("KritaShape/KisToolLazyBrush", "Colorize Brush", "krita_tool_lazybrush", "Fill", "0"),
ToolButton("KritaFill/KisToolGradient", "Gradient Tool", "krita_tool_gradient", "Fill", "0"),

ToolButton("KritaShape/KisToolRectangle", "Rectangle Tool", "krita_tool_rectangle", "Shape", "1"),
ToolButton("KritaShape/KisToolLine", "Line Tool", "krita_tool_line", "Shape", "0"),
ToolButton("KritaShape/KisToolEllipse", "Ellipse Tool", "krita_tool_ellipse", "Shape", "0"),
ToolButton("KisToolPolygon", "Polygon Tool", "krita_tool_polygon", "Shape", "0"),
ToolButton("KisToolPolyline", "Polyline Tool", "polyline", "Shape", "0"),
ToolButton("KisToolPath", "Bezier Tool", "krita_draw_path", "Shape", "0"),

ToolButton("KisToolSelectRectangular", "Rectangular Selection", "tool_rect_selection", "Select", "1"),
ToolButton("KisToolSelectElliptical", "Elliptical Selection", "tool_elliptical_selection", "Select", "0"),
ToolButton("KisToolSelectPolygonal", "Polygonal Selection", "tool_polygonal_selection", "Select", "0"),
ToolButton("KisToolSelectPath", "Bezier Selection", "tool_path_selection", "Select", "0"),

ToolButton("KisToolSelectOutline", "Outline Selection", "tool_outline_selection", "AutoSelect", "1"),
ToolButton("KisToolSelectContiguous", "Contiguous Selection", "tool_contiguous_selection", "AutoSelect", "0"),
ToolButton("KisToolSelectSimilar", "Similar Selection", "tool_similar_selection", "AutoSelect", "0"),
ToolButton("KisToolSelectMagnetic", "Magnetic Selection", "tool_magnetic_selection", "AutoSelect", "0"),

ToolButton("ToolReferenceImages", "Reference Image Tool", "krita_tool_reference_images", "Reference", "1"),
ToolButton("KisAssistantTool", "Assistant Tool", "krita_tool_assistant", "Reference", "0"),
ToolButton("KritaShape/KisToolMeasure", "Measure Tool", "krita_tool_measure", "Reference", "0"),

ToolButton("PanTool", "Pan", "tool_pan", "Navigation", "1"),
ToolButton("ZoomTool", "Zoom", "tool_zoom", "Navigation", "0"),

]
