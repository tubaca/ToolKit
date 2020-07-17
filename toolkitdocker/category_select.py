# This Python file uses the following encoding: utf-8
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from krita import *

import json
from os import path

from toolkitdocker.json_class import json_class
from toolkitdocker.toolbuttons import ToolList
from toolkitdocker.tool_categories import CategoryDict

category_dictionary = CategoryDict()

class CategorySelect(QWidget):

    def __init__(self):
        super().__init__()

        self.subtool_column = QVBoxLayout()
        self.columns = QHBoxLayout()
        self.config_layout = QVBoxLayout()
        self.header_row = QHBoxLayout()

        self.preset_dropbox = QComboBox()
        self.preset_dropbox.insertItem(0, "Painting")
        self.preset_dropbox.setEditable(True)

        self.columns.addLayout(self.subtool_column)

        self.header_row.addWidget(self.preset_dropbox)

        self.config_layout.addLayout(self.header_row)
        self.config_layout.addLayout(self.columns)
        self.config_layout.addWidget(QPushButton("Pop"))

        self.containers = {}

        for category in category_dictionary.categories:
            subtool_container = Container(category)

            self.containers.update({category : subtool_container})

        for ToolButton in ToolList:
            tool_panel = ToolPanel()
            tool_panel.setIcon(Application.icon(ToolButton.icon))
            tool_panel.setObjectName(ToolButton.actionName)
            if ToolButton.isMain == "1":
                self.containers[ToolButton.category].layout().addWidget(tool_panel)
                self.containers[ToolButton.category].layout().addWidget(QVSeparationLine())
            else:
                self.containers[ToolButton.category].layout().addWidget(tool_panel)

        for container in self.containers.values():
            self.subtool_column.addWidget(container)

        self.setLayout(self.config_layout)


class Container(QFrame):

    def __init__(self, name):
        super().__init__()
        self.name = name
        self.setFrameShape(QFrame.StyledPanel)
        self.setFrameShadow(QFrame.Sunken)

        self.setLayout(QHBoxLayout())
        self.layout().setAlignment(Qt.AlignLeft)

        self.setAcceptDrops(True)

    def dragEnterEvent(self, event):
        event.accept()

    def dropEvent(self, event):
        position = event.pos()
        self.layout().addWidget(QDropEvent.source(event))

        event.setDropAction(Qt.MoveAction)
        event.accept() # insertWidget

class QVSeparationLine(QFrame):

  def __init__(self):
    super().__init__()
    self.setFixedWidth(20)
    self.setMinimumHeight(1)
    self.setFrameShape(QFrame.VLine)
    self.setFrameShadow(QFrame.Sunken)
    self.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Preferred)
    return

class ToolPanel(QToolButton):
    def __init__(self):
        super().__init__()

    def mouseMoveEvent(self, event):
        mimeData = QMimeData()
        drag = QDrag(self)
        drag.setMimeData(mimeData)
        drag.setHotSpot(event.pos() - self.rect().topLeft())

        dropAction = drag.exec_(Qt.MoveAction)
