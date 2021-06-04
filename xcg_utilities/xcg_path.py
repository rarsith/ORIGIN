import sys
from xcg_ui.xchange_master_control_ui import ProjectTreeViewWidget
from PySide2 import QtWidgets, QtCore, QtGui



class XcgPath():
    def __init__(self):

        self.show_name()
        self.branch_name()
        self.category_name()
        self.entry_name()
        self.task_name()

    def show_name(self):
        show = ProjectTreeViewWidget.selectedItems()
        return show


    def branch_name(self):
        pass

    def category_name(self):
        pass

    def entry_name(self):
        pass

    def task_name(self):
        pass

if __name__ == '__main__':
    x = XcgPath()
    get_show = x.show_name()
    print (get_show)