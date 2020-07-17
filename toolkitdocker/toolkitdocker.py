# This Python file uses the following encoding: utf-8

"""
Constructs the ToolKit Docker

"""

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from krita import *

import json
from os import path

from toolkitdocker.json_class import json_class
from toolkitdocker.toolbuttons import ToolList
from toolkitdocker.tool_categories import CategoryDict
from toolkitdocker.flow_layout import FlowLayout
from toolkitdocker.category_select import CategorySelect


DOCKER_actionName = "ToolKit"
DOCKER_ID = "pykrita_toolkit"


# We need to create instances of these classes to access their functions
jsonMethod = json_class()
category_dictionary = CategoryDict()


# Loads the subtool menu delay time set by user
class delayClass:

    def __init__(self, delayValue: int):
        self.value = delayValue


menu_delayValue = delayClass(jsonMethod.loadJSON()["delayValue"])


class TKStyle(QProxyStyle):
    """
    Adjusts how the toolbutton indicator arrow, and delay time are processed by Qt
    Preferences are loaded from data.json via jsonMethod.loadJSON
    """
    def styleHint(self, element, option, widget, returnData):
        """
        Changes delay time for toolbutton subtool menu to appear
        """
        if element == QStyle.SH_ToolButton_PopupDelay:
            return menu_delayValue.value

        return super().styleHint(element, option, widget, returnData)

    def drawPrimitive(self, element, option, painter, widget):
        """
        Changes appearance of toolbutton indicator arrow using QPainter
        """
        if element == QStyle.PE_IndicatorArrowDown:
            # alternate start point for submenu button mode indicator
            if jsonMethod.loadJSON()["submenuButton"] == True:
                adjusted_point = QPoint(2, 7)

            else:
                adjusted_point = QPoint(0, 5)

            triangle = QPainterPath()
            startPoint = option.rect.bottomRight() - adjusted_point
            triangle.moveTo(startPoint)
            triangle.lineTo(startPoint + QPoint(0, 5))
            triangle.lineTo(startPoint + QPoint(-5, 5))
            painter.fillPath(triangle, Qt.white)

        else:
            super().drawPrimitive(element, option, painter, widget)


class Menu(QMenu):
    """
    Subtools menu for each main toolbutton
    """
    def __init__(self, parent):
        super().__init__()

        self.parent = parent
        self.setMouseTracking

    def showEvent(self, event):
        """
        Moves position of menu to top-right toolbutton corner
        """
        super().showEvent(event)

        # Fixes Windows issue of incorrect menu dimensions on secondary displays
        self.windowHandle().setScreen(self.parent.windowHandle())

        self.move(self.parent.mapToGlobal(QPoint(0,0)) + QPoint(self.parent.width(), 0))


    def mouseMoveEvent(self, event):
        """
        Causes the subtool menu to close if cursor exits
        """
        super().mouseMoveEvent(event)

        # boundary area
        buttonTLC = self.parent.geometry().topLeft()
        menuSize = QSize(self.geometry().size())
        buttonColumn = QRect(buttonTLC, menuSize)

        bounds = self.geometry().united(buttonColumn)

        if bounds.contains(QCursor.pos()) == False:
            self.close()


class SettingsWidget(QWidget):
    """
    Settings interface widget for the user to alter ToolKit layout, and toolbutton properties
    """
    def __init__(self, parent):
        super(SettingsWidget, self).__init__(parent)
        self.layout = QVBoxLayout(self)

        # Create settings tabs
        self.tabs = QTabWidget()
        self.tab1 = QWidget()
        self.tab2 = QWidget()

        self.tab1.layout = QVBoxLayout(self)
        self.tab2.layout = QFormLayout(self)

        self.tabs.addTab(self.tab1, "Layout")
        self.tabs.addTab(self.tab2, "General")

        """
        Set up first tab
        """
        # Interface for rearranging toolbutton layout
        self.category_select = CategorySelect()
        self.tab1.layout.addWidget(self.category_select)

        self.tab1.setLayout(self.tab1.layout)

        """
        Set up second tab
        """
        # Create submenu delay time input
        self.subMenuDelay = QSpinBox()
        self.subMenuDelay.setRange(0, 1000)
        self.subMenuDelay.setSingleStep(100)
        self.subMenuDelay.setValue(menu_delayValue.value)
        self.subMenuDelay.setSuffix("ms")

        # Create submenu button mode toggle
        self.subButtonBox = QCheckBox()
        self.subButtonBox.setChecked(jsonMethod.existing_data["submenuButton"])
        
        self.tab2.layout.addRow(i18n("&Submenu Delay:"), self.subMenuDelay)
        self.tab2.layout.addRow(i18n("&Submenu Button:"), self.subButtonBox)

        self.tab2.setLayout(self.tab2.layout)

        self.layout.addWidget(self.tabs)

        """
        Add "cancel" and "accept" buttons to main layout
        """
        # Create "OK" button
        self.acceptButton = QPushButton(i18n("OK"))
        self.acceptButton.clicked.connect(self.parentWidget().close)
        self.acceptButton.clicked.connect(self.changeDelay)
        self.acceptButton.clicked.connect(self.changeSubButton)        
        self.acceptButton.clicked.connect(jsonMethod.dumpJSON)

        # Create "Cancel" button
        self.cancelButton = QPushButton(i18n("Cancel"))
        self.cancelButton.clicked.connect(self.parentWidget().close)

        self.buttons_footer = QHBoxLayout()

        # Add the buttons to layout
        self.buttons_footer.addItem(QSpacerItem(80, 0))
        self.buttons_footer.addWidget(self.acceptButton)
        self.buttons_footer.addWidget(self.cancelButton)

        self.layout.addLayout(self.buttons_footer)

        self.setLayout(self.layout)


    def changeDelay(self):
        """
        Receives and updates the new subtool menu delay value
        """
        menu_delayValue.value = self.subMenuDelay.value()
        jsonMethod.update_dict({"delayValue": menu_delayValue.value})

        for ToolButton in ToolList:
            ToolButton.setStyle(TKStyle("fusion"))


    def changeSubButton(self):
        """
        Receives and updates the subtool menu mode
        """
        jsonMethod.update_dict({"submenuButton": self.subButtonBox.isChecked()})


class SDialog(QDialog):
    """
    Dialog container for Settings interface widget
    """
    def __init__(self):
        super().__init__()

        self.setWindowTitle("ToolKit Settings")
        self.setWindowModality(Qt.ApplicationModal)

        SLayout = QGridLayout()

        # Add Settings interface widget
        SLayout.addWidget(SettingsWidget(self))

        self.setLayout(SLayout)


class ToolKitDocker(QDockWidget):
    """
    Main ToolKit Docker body, contains the main toolbuttons with subtool menus
    """
    activate_layout = pyqtSignal()

    def __init__(self):
        super().__init__()

        self.setFloating(False)
        # Set Docker title in Settings > Dockers
        self.setWindowTitle('ToolKit')

        # Create button group to handle main toolbuttons
        self.mainToolButtons = QButtonGroup()
        self.mainToolButtons.setExclusive(True)

        # Create settings dialog container
        self.dialog = SDialog()

        # Paint the ToolKitlayout when settings dialog is finalised
        self.dialog.children()[0].acceptButton.clicked.connect(self.setupLayout)

        self.widget = QWidget()

        # Conceal the 'exit' buttons and Docker title with QLabel
        label = QLabel(" ")

        label.setFrameShape(QFrame.StyledPanel)
        label.setFrameShadow(QFrame.Raised)
        label.setFrameStyle(QFrame.Panel | QFrame.Raised)
        label.setMinimumWidth(16)
        label.setFixedHeight(12)

        self.setWidget(self.widget)
        self.setTitleBarWidget(label)

        """
        Initialise ToolKit Docker layout and toolbuttons
        """
        layout = FlowLayout()
        self.widget.setLayout(layout)

        for ToolButton in ToolList:

            category_dictionary.categories[ToolButton.category].addTool(ToolButton)

            ToolButton.setParent(self)

            ToolButton.setStyle(TKStyle("fusion"))

            ToolButton.clicked.connect(self.activateTool)

        # The rest of the layout setup is handled by the "setupLayout" function
        self.activate_layout.connect(self.setupLayout)
        self.activate_layout.emit()

#        if len(Application.documents()) != 0: # attempted canvas-only mode
#            QAction(Application.action("view_show_canvas_only")).triggered.connect(self.layout.removeWidget(widget))

    def contextMenuEvent(self, event):
        """
        Shows the Settings dialog on right-click of ToolKit Docker
        """
        super().contextMenuEvent(event)

        self.dialog.exec()


    def activateTool(self):
        """
        Registers and performs the toolbutton's action in Krita
        """
        actionName = self.sender().objectName()
        ac = Application.action(actionName) 

        print(actionName, ac)
        if ac:
            ac.trigger()

        else:
            pass


    def linkMenu(self):
        """
        Populates the toolbutton's menu with subtools from its category
        """
        subMenu = self.sender()

        # Prevent the menu from continuously adding actions every click
        if subMenu.isEmpty():

            categoryName = self.sender().parent.category
            category = category_dictionary.categories[categoryName]

            # Iterate through all the tools in the category
            for key in category.ToolButtons:

                toolIcon = QIcon(Application.icon(category.ToolButtons[key].icon))
                toolText = category.ToolButtons[key].toolName
                toolName = category.ToolButtons[key].actionName
                toolAction = QAction(toolIcon, toolText, self) # set up initial toolAction

                # We need to call Krita's shortcut for the toolAction:
                try:
                    Application.action(toolName).shortcut()

                    # Find the global shortcut
                    toolShortcut = Application.action(toolName).shortcut().toString()

                    toolAction.setShortcut(toolShortcut)

                except:
                    pass

                toolAction.setObjectName(toolName)
                toolAction.setParent(self.sender().parent) # set toolbutton as parent

                toolAction.triggered.connect(self.activateTool) # activate menu tool on click
                toolAction.triggered.connect(self.swapToolButton)

                subMenu.addAction(toolAction) # add the button for this tool in the menu

            for action in subMenu.actions(): # show tool icons in submenu

                action.setIconVisibleInMenu(True)


    def swapToolButton(self):
        """
        Swaps the clicked subtool with the main toolbutton
        """
        subtool_actionName = self.sender().objectName()

        for ToolButton in ToolList:
            if ToolButton.actionName == subtool_actionName:

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
        layout = self.widget.layout()

        for ToolButton in ToolList:

            if ToolButton.isMain == "1": # Add the main tool from each category to the Docker

                self.mainToolButtons.addButton(ToolButton) # add tool to button group
                layout.addWidget(ToolButton)

                ToolButton.show()

                subMenu = Menu(ToolButton)
                subMenu.setWindowFlags(Qt.Popup)

                ToolButton.setMenu(subMenu) # this will be the submenu for each main tool

                ToolButton.menu().aboutToShow.connect(self.linkMenu) # Show submenu when clicked

                if jsonMethod.existing_data["submenuButton"] == True:
                    ToolButton.setPopupMode(QToolButton.MenuButtonPopup)

                else:
                    ToolButton.setPopupMode(QToolButton.DelayedPopup)

            else: # if ToolButton isn't main
                layout.removeWidget(ToolButton) # remove ToolButton

                ToolButton.close() # close the toolbutton

        if jsonMethod.loadJSON()["submenuButton"] == True:
            self.setMinimumWidth(40)
        else:
            self.setMinimumWidth(0)


    def canvasChanged(self, canvas):
        pass


instance = Krita.instance() # Register as Krita Docker

dock_widget_factory = DockWidgetFactory(DOCKER_ID,
                                        DockWidgetFactoryBase.DockLeft,
                                        ToolKitDocker)

instance.addDockWidgetFactory(dock_widget_factory)
