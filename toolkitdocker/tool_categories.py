"""
Contains the tool category definitions

"""

from toolkitdocker.toolbuttons import ToolList

class ToolCategory:
    """
    Holds a dictionary of {ToolButton.name : ToolButton} pairs
    """
    def __init__(self, name):
        self.name = name
        self.ToolButtons = {}

    # Adds new Toolbutton pair to dictionary
    def addTool(self, ToolButton):
        self.ToolButtons[ToolButton.actionName] = ToolButton

class CategoryDict:
    """
    Holds a dictionary of ToolCategories
    """
    def __init__(self):
        super().__init__()

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
