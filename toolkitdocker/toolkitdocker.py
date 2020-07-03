# This Python file uses the following encoding: utf-8
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from krita import *

DOCKER_NAME = 'ToolKit'
DOCKER_ID = 'pykrita_toolkit'

highlightedBack = QColor(61, 111, 145)
back = QColor(49, 49, 49)
indicator = QPixmap
TKStyleSheet = """

            QToolButton:hover { /* when the button is hovered over */
                background-color: rgb(49, 49, 49);
            }
            QToolButton:open { /* when the button has its menu open */
                background-color: rgb(89, 122, 153);
            }

            QToolButton::menu-indicator {
                image: None;
                subcontrol-origin: padding;
                subcontrol-position: bottom right;
            }

            QToolButton::menu-indicator:pressed, QToolButton::menu-indicator:open {
                position: relative;
                top: 2px; left: 2px; /* shift the arrow by 2 px */
            }
            QMenu {
                background-color: rgb(49, 49, 49);
                color: rgb(255,255,255);
                border: 1px solid #000;
            }
            QMenu::item:selected {
                background-color: rgb(89, 122, 153);
            }
        """

class ToolButton(QToolButton):

    def __init__(self, name, text, icon, category, isMain):
        super().__init__()
        self.name = name
        self.text = text
        self.icon = icon
        self.category = category
        self.isMain = isMain

        self.setStyleSheet(TKStyleSheet)

    def enterEvent(self, event):
        super().enterEvent(event)

        if len(Application.documents()) == 0: # disable buttons before document is visible
            self.setEnabled(False)
        else:
            self.setEnabled(True)


#Definitions for each tool:

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

class ToolCategory:

    def __init__(self, name):
        self.name = name
        self.ToolButtons = {} # Each ToolCategory has a dictionary of ToolButton.name : ToolButton items

    def addTool(self, ToolButton):
        self.ToolButtons[ToolButton.name] = ToolButton

class Menu(QMenu): # this is the subtools menu

    def __init__(self, parent):
        super().__init__()
        self.parent = parent

        self.setMouseTracking
        self.setStyleSheet(TKStyleSheet)

    def showEvent(self, event): # if the menu is shown
        super().showEvent(event)

        self.move(self.parent.mapToGlobal(QPoint(0,0)) + QPoint(self.parent.width(), 0)) # move menu to top-right button corner

    def mouseMoveEvent(self, event): # this causes the subtool menu to close if exited
        super().mouseMoveEvent(event)

        buttonTLC = self.parent.geometry().topLeft() # gets the clicked button's top left corner point
        menuSize = QSize(self.geometry().size()) # size of subtool menu
        buttonColumn = QRect(buttonTLC, menuSize) # column bounded by button and menu

        bounds = self.geometry().united(buttonColumn) # add safe area so the cursor doesn't accidentally exit

        if bounds.contains(QCursor.pos()) == False:
            self.close()


class ToolboxDocker(QDockWidget):

    activate_layout = pyqtSignal()

    def __init__(self):
        super().__init__()

        self.floating = False
        self.setWindowTitle('Tool Kit') # window title also acts as the Docker title in Settings > Dockers

        self.setStyleSheet(TKStyleSheet)

        buttonSize = QSize(22, 22)

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

        self.mainToolButtons = QButtonGroup()
        self.mainToolButtons.setExclusive(True)

        widget = QWidget()
        label = QLabel(" ") # label conceals the 'exit' buttons and Docker title
        label.setFrameShape(QFrame.StyledPanel)
        label.setFrameShadow(QFrame.Raised)
        label.setFrameStyle(QFrame.Panel | QFrame.Raised)
        label.setMinimumWidth(16)
        label.setFixedHeight(12)
        self.setWidget(widget)

        self.setTitleBarWidget(label)

        layout = QVBoxLayout()
        widget.setLayout(layout)

        for ToolButton in ToolList: # Set up button logic

            self.categories[ToolButton.category].addTool(ToolButton)

            ToolButton.setIcon(Application.icon(ToolButton.icon)) # Link ToolButton attributes
            ToolButton.setObjectName(ToolButton.name)
            ToolButton.setToolTip(i18n(ToolButton.text))

            ToolButton.setCheckable(True)
            ToolButton.setAutoRaise(True)

            ToolButton.setPopupMode(QToolButton.DelayedPopup)

            ToolButton.pressed.connect(self.activateTool) # Activate when clicked
            ToolButton.pressed.connect(self.linkMenu) # Show submenu when clicked

        self.activate_layout.connect(self.setupLayout) # Paint the layout
        self.activate_layout.emit()

    def activateTool(self):

        if len(Application.documents()) != 0: # prevents the toolbox activating without an open document

            actionName = self.sender().objectName() # get ToolButton name
            ac = Application.action(actionName) # Search this name in Krita's action list

            print(actionName, ac)
            if ac:
                ac.trigger() # trigger the action in Krita

            else:
                pass

    def linkMenu(self):

        if len(Application.documents()) != 0: # prevents the toolbox activating without an open document

            subMenu = self.sender().menu() # link the toolbutton menu to this function

            if subMenu.isEmpty(): # prevents the menu from continuously adding actions every click

                categoryName = self.sender().category
                category = self.categories[categoryName] # get the category

                for key in category.ToolButtons: # iterate through all the tools in the category

                    toolIcon = QIcon(Application.icon(category.ToolButtons[key].icon))
                    toolText = category.ToolButtons[key].text
                    toolName = category.ToolButtons[key].name
                    toolAction = QAction(toolIcon, toolText, self) # set up initial toolAction

                    # we need to call Krita's shortcut for the toolAction:
                    try:
                        Application.action(toolName).shortcut()

                        toolShortcut = Application.action(toolName).shortcut().toString() # find the global shortcut

                        toolAction.setShortcut(toolShortcut)

                    except:
                        pass

                    toolAction.setObjectName(toolName)
                    toolAction.setParent(self.sender()) # set toolbutton as parent

                    toolAction.triggered.connect(self.activateTool) # activate menu tool on click
                    toolAction.triggered.connect(self.swapToolButton)

                    subMenu.addAction(toolAction) # add the button for this tool in the menu

                for action in subMenu.actions(): # show tool icons in submenu

                    action.setIconVisibleInMenu(True)

    def swapToolButton(self):
        actionName = self.sender().objectName()

        for ToolButton in ToolList:
            if ToolButton.name == actionName: # for the selected subtool

                mainToolButton = self.sender().parentWidget() # the current main tool shown

                if mainToolButton.isMain != ToolButton.isMain:
                    mainToolButton.isMain = "0" # swap the tool's main status
                    ToolButton.isMain = "1"
                    ToolButton.setChecked(True)
                    self.activate_layout.emit() # recall the setupLayout function

                else:
                    ToolButton.setChecked(True)

            else:
                pass

    @pyqtSlot()
    def setupLayout(self):
        layout = self.widget().layout()
        for ToolButton in ToolList:

            if ToolButton.isMain == "1": # Add the main tool from each category to the Docker

                self.mainToolButtons.addButton(ToolButton)
                layout.addWidget(ToolButton)
                ToolButton.show()
                subMenu = Menu(ToolButton)
                ToolButton.setMenu(subMenu) # this will be the submenu for each main tool

            else: # if ToolButton isn't main
                layout.removeWidget(ToolButton) # remove ToolButton

                ToolButton.close() # close the toolbutton


    def canvasChanged(self, canvas):
        pass

instance = Krita.instance() # Register as Krita Docker

dock_widget_factory = DockWidgetFactory(DOCKER_ID,
                                        DockWidgetFactoryBase.DockLeft,
                                        ToolboxDocker)

instance.addDockWidgetFactory(dock_widget_factory)
