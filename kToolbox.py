# This Python file uses the following encoding: utf-8
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import pyqtSlot, Qt
from krita import *
from . import mainwindow

highlightedBack = QColor(86, 128, 194)
back = QColor(49, 49, 49)

class toolButton(QToolButton):

    def __init__(self):
        super(toolButton, self).__init__(parent)

        self.action = krita.instance().action(activeTool[i].action)
        self.setIcon()
        self.setFixedSize(24, 24)
        self.setIconSize(QSize(24, 24)

    def onButtonClick():
        self.action().connect.krita.instance().action()

        toolButton.clicked.connect(onButtonClick)

class kToolBox(QDockWidget):

    def __init__(self, parent):
        super(kToolBox, self).__init__(parent)

        self.setWindowTitle(i18n("KToolBox"))
        mainWidget = QWidget()
        layout = QVBoxLayout()
        mainWidget.setLayout(layout)
        mainWidget.layout.addButton(toolButton)
        self.loadButtons()

    def loadButtons(self):
        self.kToolBox.buttons = []

        allTools = Application.resources("tool")

        for index, item in enumerate(toolList[]):
            buttonLayout = QVBoxLayout()
            button = dropbutton.DropButton(self.mainDialog)
            button.setObjectName(item)
            button.clicked.connect(button.selectTool)
            button.toolChooser = self.toolChooser

            action = self.kToolBox.actions[index]

            if action and action.tool and action.tool in allTools:
                p = allTools[action.tool]
                button.tool = p.name()
                button.setIcon(QIcon(QPixmap.fromImage(p.image())))

            buttonLayout.addWidget(button)

            label = QLabel(
                action.shortcut().toString())
            label.setAlignment(Qt.AlignHCentre)
            buttonLayout.addWidget(label)

            self.hbox.addLayout(buttonLayout)
            self.kToolBox.buttons.append(button)

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

Krita.instance().addDockWidgetFactory(DockWidgetFactory("kToolBox", DockWidgetFactoryBase.DockRight, kToolBox))


