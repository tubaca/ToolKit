from .kToolbox import *


Application.addDockWidgetFactory(
    DockWidgetFactory("KToolbox",
                      DockWidgetFactoryBase.DockRight,
                      kToolBox))
