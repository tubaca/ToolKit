# This Python file uses the following encoding: utf-8
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from krita import *

DOCKER_NAME = 'KToolbox'
DOCKER_ID = 'kToolbox'

highlightedBack = QColor(86, 128, 194)
back = QColor(49, 49, 49)

class ToolButton(QToolButton):

    def __init__(self, name, text, icon, category, priority):
        super().__init__()
        self.name = name
        self.text = text
        self.icon = icon
        self.category = category
        self.priority = priority

#Tool definitions:

ToolList = [

ToolButton("KisToolTransform", "Transform Tool", "krita_tool_transform", "Transform", "0"),
ToolButton("KritaTransform/KisToolMove", "Move Tool", "krita_tool_move", "Transform", "1"),
ToolButton("KisToolCrop", "Crop Tool", "tool_crop", "Transform", "2"),

ToolButton("InteractionTool", "Select Shape", "select", "Vector", "0"),
ToolButton("SvgTextTool", "Text Tool", "draw-text", "Vector", "1"),
ToolButton("PathTool", "Edit Shape Tool", "shape_handling", "Vector", "2"),
ToolButton("KarbonCalligraphyTool", "Calligraphy", "calligraphy", "Vector", "3"),

ToolButton("KritaShape/KisToolBrush", "Freehand Brush", "krita_tool_freehand", "Paint", "0"),
ToolButton("KritaShape/KisToolDyna", "Dynamic Brush", "krita_tool_dyna", "Paint", "1"),
ToolButton("KritaShape/KisToolMultiBrush", "Multibrush", "krita_tool_multihand", "Paint", "2"),
ToolButton("KritaShape/KisToolSmartPatch", "Smart Patch Tool", "krita_tool_smart_patch", "Paint", "3"),
ToolButton("KisToolPencil", "Freehand Path", "krita_tool_freehandvector", "Paint", "4"),

ToolButton("KritaFill/KisToolFill", "Fill Tool", "krita_tool_color_fill", "Fill", "0"),
ToolButton("KritaSelected/KisToolColorPicker", "Color Picker", "krita_tool_color_picker", "Fill", "1"),
ToolButton("KritaShape/KisToolLazyBrush", "Colorize Brush", "krita_tool_lazybrush", "Fill", "2"),
ToolButton("KritaFill/KisToolGradient", "Gradient Tool", "krita_tool_gradient", "Fill", "3"),

ToolButton("KritaShape/KisToolRectangle", "Rectangle Tool", "krita_tool_rectangle", "Shape", "0"),
ToolButton("KritaShape/KisToolLine", "Line Tool", "krita_tool_line", "Shape", "1"),
ToolButton("KritaShape/KisToolEllipse", "Ellipse Tool", "krita_tool_ellipse", "Shape", "2"),
ToolButton("KisToolPolygon", "Polygon Tool", "krita_tool_polygon", "Shape", "3"),
ToolButton("KisToolPolyline", "Polyline Tool", "polyline", "Shape", "4"),
ToolButton("KisToolPath", "Bezier Tool", "krita_draw_path", "Shape", "5"),

ToolButton("KisToolSelectRectangular", "Rectangular Selection", "tool_rect_selection", "Select", "0"),
ToolButton("KisToolSelectElliptical", "Elliptical Selection", "tool_elliptical_selection", "Select", "1"),
ToolButton("KisToolSelectPolygonal", "Polygonal Selection", "tool_polygonal_selection", "Select", "2"),
ToolButton("KisToolSelectPath", "Bezier Selection", "tool_path_selection", "Select", "3"),

ToolButton("KisToolSelectOutline", "Outline Selection", "tool_outline_selection", "AutoSelect", "0"),
ToolButton("KisToolSelectContiguous", "Contiguous Selection", "tool_contiguous_selection", "AutoSelect", "1"),
ToolButton("KisToolSelectSimilar", "Similar Selection", "tool_similar_selection", "AutoSelect", "2"),
ToolButton("KisToolSelectMagnetic", "Magnetic Selection", "tool_magnetic_selection", "AutoSelect", "3"),

ToolButton("ToolReferenceImages", "Reference Image Tool", "krita_tool_reference_images", "Reference", "0"),
ToolButton("KisAssistantTool", "Assistant Tool", "krita_tool_assistant", "Reference", "1"),
ToolButton("KritaShape/KisToolMeasure", "Measure Tool", "krita_tool_measure", "Reference", "2"),

ToolButton("PanTool", "Pan", "tool_pan", "Navigation", "0"),
ToolButton("ZoomTool", "Zoom", "tool_zoom", "Navigation", "1"),

]

class ToolCategory:

    def __init__(self, name):
        self.name = name
        self.ToolButtons = {} # Each ToolCategory has a dictionary of ToolButton.name : ToolButton items

    def addTool(self, ToolButton):
        self.ToolButtons[ToolButton.name] = ToolButton

class ToolboxDocker(QDockWidget):

    def __init__(self):
        super(ToolboxDocker, self).__init__()

        self.floating = False
        self.setStyleSheet("""
            QMenu {
                background-color: rgb(49, 49, 49);
                color: rgb(255,255,255);
                border: 1px solid #000;
            }

            QMenu::item::selected {
                background-color: rgb(30,30,30);
            }
        """)

        buttonSize = QSize(14, 14)
#        rc = QRect(QGuiApplication.screens().at(screen).availableGeometry())
#
#        if (rc.width() <= 1024):
#            buttonSize = QSize(12, 12)
#
#        elif (rc.width() <= 1377):             (attempt adaptive button scaling based
#            buttonSize = QSize(14, 14)                 on screen dimensions)
#
#        elif (rc.width() <= 1920 ):
#            buttonSize = QSize(16, 16)
#
#        else:
#            buttonSize = QSize(22, 22)

        self.categories = { #State the categories for the tools:
                           "Transform": ToolCategory("Transform"),
                           "Vector": ToolCategory("Vector"),
                           "Paint": ToolCategory("Paint"),
                           "Fill": ToolCategory("Fill"),
                           "Shape": ToolCategory("Shape"),
                           "Select": ToolCategory("Select"),
                           "AutoSelect": ToolCategory("AutoSelect"),
                           "Reference": ToolCategory("Reference"),
                           "Navigation": ToolCategory("Navigation")
                           }

        widget = QWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        widget.setLayout(layout)

        self.setWindowTitle(i18n("Tool Kit"))

        for ToolButton in ToolList: # Set up button logic

            self.categories[ToolButton.category].addTool(ToolButton)
            ToolButton.setIconSize(buttonSize)

            ToolButton.setIcon(Application.icon(ToolButton.icon)) # Link ToolButton attributes
            ToolButton.setObjectName(ToolButton.name)
            ToolButton.setToolTip(i18n(ToolButton.text))

            ToolButton.setCheckable(True)
            ToolButton.setAutoRaise(True)
            ToolButton.setAutoExclusive(True)

            ToolButton.clicked.connect(self.activateTool) # Connect activation actions when clicked
            ToolButton.clicked.connect(self.showSubMenu)

            if ToolButton.priority == "0":

                layout.addWidget(ToolButton)
            else:
                pass

        self.setWidget(widget)


    @pyqtSlot()
    def showSubMenu(self): # Define activation actions

        subMenu = QMenu('')

        categoryName = self.sender().category
        category = self.categories[categoryName] # get the category

        for key in category.ToolButtons: # iterate through all the tools in the category

            toolIcon = QIcon(Application.icon(category.ToolButtons[key].icon))
            toolText = category.ToolButtons[key].text
            toolName = category.ToolButtons[key].name
            toolAction = QAction(toolIcon, toolText, self) # pykrita doesn't seem to allow shortcuts for QActions,
                                                           # the following is an attempted workaround

            toolShortcut = QAction(Application.action(toolName)).shortcut() # find the global shortcut

            toolAction.setShortcut(toolShortcut) # add the global shortcut
            toolAction.setObjectName(toolName)

            toolAction.triggered.connect(self.activateTool) # activate menu tool on click

            subMenu.addAction(toolAction) # add the button for this tool

        for action in subMenu.actions(): # show tool icons in submenu

            action.setIconVisibleInMenu(True)

          # here would be 'action.setShortcutVisibleInMenu', which doesn't exist

        self.sender().setMenu(subMenu) # set the submenu to the clicked button

        mousePosition = QCursor.pos()
        subMenu.popup(mousePosition + QPoint(10, 0)) # adjust the submenu position to the right

    def activateTool(self):

        actionName = self.sender().objectName(); # get ToolButton name
        ac = Application.action(actionName) # Search this name in Krita's action list
        print(actionName, ac)
        if ac:
            ac.trigger()

    def canvasChanged(self, canvas):
        pass

instance = Krita.instance() # Register as Krita Docker
dock_widget_factory = DockWidgetFactory(DOCKER_ID,
                                        DockWidgetFactoryBase.DockRight,
                                        ToolboxDocker)

instance.addDockWidgetFactory(dock_widget_factory)
