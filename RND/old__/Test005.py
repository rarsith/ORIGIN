import sys
from PySide2 import QtWidgets, QtCore


class Window(QtWidgets.QWidget):

    def __init__(self):
        super(Window, self).__init__()
        # self.setMaximumSize(150, 50)
        # self.setWindowTitle('PyQt Tuts')
        self.table()
        self.get_values()


    def table(self):


        self.tableWidget = QtWidgets.QTableWidget()
        self.tableWidget.setGeometry(QtCore.QRect(220, 100, 285, 292))
        self.tableWidget.setColumnCount(4)
        self.tableWidget.setShowGrid(False)
        self.tableWidget.setAlternatingRowColors(True)
        header = self.tableWidget.verticalHeader()
        header.hide()


        self.tableWidget.setColumnWidth(0, 70)
        self.tableWidget.setColumnWidth(3, 20)
        self.tableWidget.setColumnWidth(4, 20)
        self.tableWidget.setColumnWidth(5, 20)

        self.tableWidget.show()


        attr = ['one', 'two', 'three']
        i = 0
        for j in attr:

            self.tableWidget.setItem(i, 1, QtWidgets.QTableWidgetItem(j))
            self.tableWidget.setRowCount(len(attr))
            comboBox = QtWidgets.QComboBox()
            comboBox.addItems(['ff', 'gg', 'cc', 'aa'])
            checkBox = QtWidgets.QCheckBox()
            checkBox01 = QtWidgets.QCheckBox()
            checkBox02 = QtWidgets.QCheckBox()
            checkBox03 = QtWidgets.QCheckBox()

            self.tableWidget.setCellWidget(i, 0, checkBox01)
            self.tableWidget.setCellWidget(i, 2, comboBox)
            self.tableWidget.setCellWidget(i, 3, checkBox)
            self.tableWidget.setCellWidget(i, 4, checkBox02)
            self.tableWidget.setCellWidget(i, 5, checkBox03)

            i += 1

    def get_values(self):
        v = self.tableWidget.item(1, 1)
        print v.text()

        type = self.tableWidget.cellWidget(0, 2)
        print type.currentText()

        x = self.tableWidget.cellWidget(0, 2)
        print x.currentText()

        rows = self.tableWidget.rowCount()
        print rows
        for i in range(rows):
            print i



if __name__=="__main__":

    def run():
        app = QtWidgets.QApplication(sys.argv)
        w = Window()
        sys.exit(app.exec_())

    run()
