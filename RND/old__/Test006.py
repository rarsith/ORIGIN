import sys
from PySide2 import QtWidgets

# from mydesign import *

import sys

data = ['PyQt5','Is','Awesome']

class mywindow(QtWidgets.QMainWindow):

        def __init__(self):

            super(mywindow, self).__init__()

            self.tableWidget = QtWidgets.QTableWidget()
            self.tableWidget.setRowCount(3)
            self.tableWidget.setColumnCount(2)





            row=0

            for item in data:

                cellinfo = QtWidgets.QTableWidgetItem(item)

                combo = QtWidgets.QComboBox()

                combo.addItem("First item")

                combo.addItem("Second item")

                self.tableWidget.setItem(row, 0, cellinfo)

                self.tableWidget.setCellWidget(row, 1, combo)

                row += 1

if __name__ == '__main__':

    app = QtWidgets.QApplication(sys.argv)

    create_shot = mywindow()
    create_shot.show()
    sys.exit(app.exec_())