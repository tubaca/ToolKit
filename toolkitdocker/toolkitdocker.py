# This Python file uses the following encoding: utf-8
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from krita import *

import json
from os import path

from toolkitdocker.tool_list import ToolList

DOCKER_NAME = 'ToolKit'
DOCKER_ID = 'pykrita_toolkit'

class json_class:
    fileDir = path.dirname(path.realpath(__file__))
    def __init__(self):
        self.existing_data = {}

        with open(self.fileDir + '/data.json') as jsonFile:
            data = json.load(jsonFile)

        self.existing_data.update(data)

    def loadJSON(self):
        with open(self.fileDir + '/data.json') as jsonFile:
            data = json.load(jsonFile)
            return data

    def update_dict(self, new_data = {}):

        self.existing_data.update(new_data)

    def dumpJSON(self):

        json_object = json.dumps(self.existing_data, sort_keys = True, indent = 4)

        with open(self.fileDir + '/data.json', 'w') as jsonFile:
            jsonFile.write(json_object)

jsonMethod = json_class()

class delayClass:
    def __init__(self, delayValue: int):
        self.value = delayValue

menu_delayValue = delayClass(jsonMethod.loadJSON()["delayValue"])

class TKStyle(QProxyStyle):

    def styleHint(self, element, option,
                  widget, returnData):

        if element == QStyle.SH_ToolButton_PopupDelay:
            return menu_delayValue.value;

        return super().styleHint(element, option, widget, returnData);


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


class SettingsWidget(QWidget): # this is the settings tab

    def __init__(self, parent):
        super(SettingsWidget, self).__init__(parent)
        self.layout = QGridLayout(self)

        self.tabs = QTabWidget()
        self.tab1 = QWidget()
        self.tab2 = QWidget()
        self.tabs.resize(300, 200)

        self.tabs.addTab(self.tab1, "Layout")
        self.tabs.addTab(self.tab2, "General")

        self.tab1.layout = QVBoxLayout(self)

        self.label = QLabel()
        self.label.setText("This is the first tab")

        self.settings_ToolList = QListWidget()
        for ToolButton in ToolList:
            self.settings_ToolList.addItem(ToolButton.name)

        self.category_Dropdown = QComboBox()
        self.tab1.layout.addWidget(self.label)

        self.tab1.setLayout(self.tab1.layout)

        self.tab2.layout = QFormLayout(self)

        self.subMenuDelay = QSpinBox() # user input for submenu delay time
        self.subMenuDelay.setRange(0, 1000)
        self.subMenuDelay.setSingleStep(100)
        self.subMenuDelay.setValue(menu_delayValue.value)
        self.subMenuDelay.setSuffix("ms")

        self.subButtonBox = QCheckBox()
        self.subButtonBox.setChecked(jsonMethod.loadJSON()["submenuButton"])

        self.tab2.layout.addRow(i18n("&Submenu Delay:"), self.subMenuDelay)
        self.tab2.layout.addRow(i18n("&Submenu Button:"), self.subButtonBox)

        self.tab2.setLayout(self.tab2.layout)

        self.layout.addWidget(self.tabs)

        self.acceptButton = QPushButton(i18n("OK"))
        self.acceptButton.clicked.connect(self.parentWidget().close)
        self.acceptButton.clicked.connect(self.changeDelay)
        self.acceptButton.clicked.connect(self.changeSubButton)
        self.acceptButton.clicked.connect(jsonMethod.dumpJSON)

        self.cancelButton = QPushButton(i18n("Cancel"))
        self.cancelButton.clicked.connect(self.parentWidget().close)

        self.layout.addWidget(self.acceptButton)
        self.layout.addWidget(self.cancelButton)
        self.setLayout(self.layout)

    def changeDelay(self):
        menu_delayValue.value = self.subMenuDelay.value()
        jsonMethod.update_dict({"delayValue": menu_delayValue.value})
        for ToolButton in ToolList:
            ToolButton.setStyle(TKStyle("fusion"))

    def changeSubButton(self):
        jsonMethod.update_dict({"submenuButton": self.subButtonBox.isChecked()})

        for ToolButton in ToolList:
            if self.subButtonBox.isChecked() == True:
                ToolButton.setPopupMode(QToolButton.MenuButtonPopup)
            else:
                ToolButton.setPopupMode(QToolButton.DelayedPopup)
        for ToolButton in ToolList:
            if self.subButtonBox.isChecked() == True:
                ToolButton.setPopupMode(QToolButton.MenuButtonPopup)
            else:
                ToolButton.setPopupMode(QToolButton.DelayedPopup)

SDialog = QDialog()

SDialog.setWindowTitle("ToolKit Settings")
SDialog.setWindowModality(Qt.ApplicationModal)

SLayout = QGridLayout()
SLayout.addWidget(SettingsWidget(SDialog))
SDialog.setLayout(SLayout)

settings_widget = SettingsWidget(SDialog)

class ToolboxDocker(QDockWidget):

    activate_layout = pyqtSignal()

    def __init__(self):
        super().__init__()

        self.floating = False
        self.setWindowTitle('ToolKit') # window title also acts as the Docker title in Settings > Dockers


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

        self.widget = QWidget()
        label = QLabel(" ") # label conceals the 'exit' buttons and Docker title

        label.setFrameShape(QFrame.StyledPanel)
        label.setFrameShadow(QFrame.Raised)
        label.setFrameStyle(QFrame.Panel | QFrame.Raised)
        label.setMinimumWidth(16)
        label.setFixedHeight(12)

        self.setWidget(self.widget)
        self.setTitleBarWidget(label)

        layout = QGridLayout()

        self.widget.setLayout(layout)

        for ToolButton in ToolList: # Set up button logic

            self.categories[ToolButton.category].addTool(ToolButton)

            ToolButton.setIcon(Application.icon(ToolButton.icon)) # Link ToolButton attributes
            ToolButton.setObjectName(ToolButton.name)
            ToolButton.setToolTip(i18n(ToolButton.text))

            ToolButton.setStyle(TKStyle("fusion"))

            ToolButton.setCheckable(True)
            ToolButton.setAutoRaise(True)
            if jsonMethod.loadJSON()["submenuButton"] == True:
                ToolButton.setPopupMode(QToolButton.MenuButtonPopup)
            else:
                ToolButton.setPopupMode(QToolButton.DelayedPopup)

            ToolButton.pressed.connect(self.activateTool) # Activate when clicked


        self.activate_layout.connect(self.setupLayout) # Paint the layout
        self.activate_layout.emit()

#        if len(Application.documents()) != 0: # attempted canvas-only mode
#            QAction(Application.action("view_show_canvas_only")).triggered.connect(self.layout.removeWidget(widget))

    def contextMenuEvent(self, event):
        super().contextMenuEvent(event)
        SDialog.exec()


    def activateTool(self):

        actionName = self.sender().objectName() # get ToolButton name
        ac = Application.action(actionName) # Search this name in Krita's action list

        print(actionName, ac)
        if ac:
            ac.trigger() # trigger the action in Krita

        else:
            pass


    def linkMenu(self):

        subMenu = self.sender() # link the toolbutton menu to this function

        if subMenu.isEmpty(): # prevents the menu from continuously adding actions every click

            categoryName = self.sender().parent.category
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
                toolAction.setParent(self.sender().parent) # set toolbutton as parent

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
        layout = self.widget.layout()

        for ToolButton in ToolList:

            if ToolButton.isMain == "1": # Add the main tool from each category to the Docker

                self.mainToolButtons.addButton(ToolButton) # add tool to button group
                layout.addWidget(ToolButton)

                ToolButton.show()
                subMenu = Menu(ToolButton)
                ToolButton.setMenu(subMenu) # this will be the submenu for each main tool

                ToolButton.menu().aboutToShow.connect(self.linkMenu) # Show submenu when clicked
                if jsonMethod.loadJSON()["submenuButton"] == True:
                    ToolButton.menu().aboutToShow.connect(self.linkMenu)

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
