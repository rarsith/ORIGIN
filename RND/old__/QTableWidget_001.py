import sys
from PySide2 import QtGui, QtCore, QtWidgets


def CurrentPos():
    clickme = QtWidgets.QApplication.focusWidget()
    index = table.indexAt(clickme.pos())
    if index.isValid():
        print(index.row(), index.column())


def AddValues():
    table.setRowCount(5)
    for i in range(5):
        button = QtWidgets.QPushButton('Click1')
        table.setCellWidget(i, 1, button)
        button.clicked.connect(CurrentPos)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    table = QtWidgets.QTableWidget()
    table.setFixedSize(QtCore.QSize(330, 250))

    table.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
    table.setSelectionBehavior(QtWidgets.QTableWidget.SelectRows)
    table.setSelectionMode(QtWidgets.QTableWidget.NoSelection)
    table.horizontalHeader().setStretchLastSection(True)
    table.setFocusPolicy(QtCore.Qt.NoFocus)

    table.setColumnCount(3)
    table.setHorizontalHeaderLabels(['A', 'B', 'C'])
    table.setColumnWidth(0, 50)
    table.setColumnWidth(1, 200)
    table.show()

    AddValues()

    app.exec_()