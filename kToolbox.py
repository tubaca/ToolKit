# This Python file uses the following encoding: utf-8
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import pyqtSlot, Qt
from krita import *
from . import mainwindow

highlightedBack = QColor(86, 128, 194)
back = QColor(49, 49, 49)

class kToolBox(QDockWidget):

    def __init__(self):
        super(kToolBox, self).__init__()

        self.setWindowTitle(i18n("KToolBox"))
        mainWidget = QWidget(self)
        self.setWidget(mainWidget)
        layout = QVBoxLayout()
        mainWidget.setLayout(layout)

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


