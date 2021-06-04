#!/usr/bin/env python
#-*- coding:utf-8 -*-

import sys
# sys.setapi('QString', 2)
# sys.setapi('QVariant', 2)

from PySide2 import QtCore, QtGui, QtWidgets

class MyWindow(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(MyWindow, self).__init__(parent)

        self.pathRoot = QtCore.QDir.rootPath()

        self.model = QtWidgets.QFileSystemModel(self)
        self.model.setRootPath(self.pathRoot)

        self.indexRoot = self.model.index(self.model.rootPath())

        self.treeView = QtWidgets.QTreeView(self)
        self.treeView.setModel(self.model)
        self.treeView.setRootIndex(self.indexRoot)
        self.treeView.clicked.connect(self.on_treeView_clicked)

        self.labelFileName = QtWidgets.QLabel(self)
        self.labelFileName.setText("File Name:")

        self.lineEditFileName = QtWidgets.QLineEdit(self)

        self.labelFilePath = QtWidgets.QLabel(self)
        self.labelFilePath.setText("File Path:")

        self.lineEditFilePath = QtWidgets.QLineEdit(self)

        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.addWidget(self.labelFileName, 0, 0)
        self.gridLayout.addWidget(self.lineEditFileName, 0, 1)
        self.gridLayout.addWidget(self.labelFilePath, 1, 0)
        self.gridLayout.addWidget(self.lineEditFilePath, 1, 1)

        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addLayout(self.gridLayout)
        self.layout.addWidget(self.treeView)

    @QSlot(QtCore.QModelIndex)
    def on_treeView_clicked(self, index):
        indexItem = self.model.index(index.row(), 0, index.parent())

        fileName = self.model.fileName(indexItem)
        filePath = self.model.filePath(indexItem)

        self.lineEditFileName.setText(fileName)
        self.lineEditFilePath.setText(filePath)

if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    app.setApplicationName('MyWindow')

    main = MyWindow()
    main.resize(666, 333)
    main.move(app.desktop().screen().rect().center() - main.rect().center())
    main.show()

    sys.exit(app.exec_())