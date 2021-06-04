from PySide2.QtCore import Slot
from PySide2.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QTableWidget,
    QTableWidgetItem,
    QPushButton,
    QMessageBox,
)


class Widget(QWidget):
    def __init__(self, parent=None, **kwargs):
        super().__init__(parent, **kwargs)

        l = QVBoxLayout(self)

        # Create a blank 10x5 table
        self._tableWidget = QTableWidget(10, 5, self)

        # Create some test data, simply the text '(row,col)' for each cell
        for row in range(10):
            for col in range(5):
                self._tableWidget.setItem(
                    row, col, QTableWidgetItem(f"({row+1},{col+1})")
                )
        self._tableWidget.setSelectionBehavior(QTableWidget.SelectRows)

        l.addWidget(self._tableWidget)

        l.addWidget(QPushButton("Selected", self, clicked=self.getSelectedItems))

    @Slot()
    def getSelectedItems(self):
        try:
            # Get the first QTableWidgetItem from the selected row or catch the
            # exception if no row is selected.
            firstColValue: QTableWidgetItem = self._tableWidget.selectedItems()[0]
        except IndexError:
            return

        # Show a message box with the .text() value of the QTableWidgetItem
        QMessageBox.information(
            self, "Column Value", f"1st Column Value: {firstColValue.text()}"
        )


if __name__ == "__main__":
    from sys import argv, exit
    from PySide2.QtWidgets import QApplication

    a = QApplication(argv)
    m = Widget()
    m.show()
    exit(a.exec_())