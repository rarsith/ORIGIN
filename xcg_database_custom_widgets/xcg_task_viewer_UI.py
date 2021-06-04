from PySide2 import QtWidgets, QtCore, QtGui




class TaskViewerBuild(QtWidgets.QListWidget):
    def __init__(self, parent=None):
        super(TaskViewerBuild, self).__init__(parent)

        self.widget_build()

    def widget_build(self):

        self.setSelectionMode(QtWidgets.QListWidget.ExtendedSelection)
        self.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)

class TaskViewerUI(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(TaskViewerUI, self).__init__(parent)
        self.setMinimumWidth(120)
        self.setMaximumWidth(120)
        self.create_widgets()
        self.create_layout()

    def create_widgets(self):
        self.task_viewer_wdg = TaskViewerBuild()

    def create_layout(self):
        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.addWidget(self.task_viewer_wdg)


if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    font = app.instance().setFont(QtGui.QFont())
    test_dialog = TaskViewerUI()
    test_dialog.show()
    sys.exit(app.exec_())