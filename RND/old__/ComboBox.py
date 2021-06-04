from PySide2 import QtCore, QtGui, QtWidgets
import sys

class CheckableComboBox(QtWidgets.QComboBox):
    def __init__(self, parent = None):
        super(CheckableComboBox, self).__init__(parent)
        self.view().pressed.connect(self.handleItemPressed)
        self.setModel(QtGui.QStandardItemModel(self))

    def handleItemPressed(self, index):
        item = self.model().itemFromIndex(index)
        if item.checkState() == QtCore.Qt.Checked:
            item.setCheckState(QtCore.Qt.Unchecked)
        else:
            item.setCheckState(QtCore.Qt.Checked)

    def checkedItems(self):
        checkedItems = []
        for index in range(self.count()):
            item = self.item(index)
            if item.checkState() == Qt.Checked:
                checkedItems.append(item)
        return checkedItems

class Ui_dialogCreateBatch(object):
    def setupUi(self, dialogCreateBatch):
        dialogCreateBatch.resize(400, 338)
        dialogCreateBatch.setMouseTracking(True)

        self.gridLayoutWidget = QtWidgets.QWidget(dialogCreateBatch)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(10, 10, 360, 115))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")

        self.cboItemList = CheckableComboBox(self.gridLayoutWidget)
        self.cboItemList.setObjectName("cboItemList")
        self.gridLayout.addWidget(self.cboItemList, 0, 0, 1, 1)

        data = ('item1', 'item2', 'item3')
        for index, element in enumerate(data):
            self.cboItemList.addItem(element)
            item = self.cboItemList.model().item(index, 0)
            item.setCheckState(QtCore.Qt.Unchecked)

        self.buttonBox = QtWidgets.QDialogButtonBox(dialogCreateBatch)
        self.buttonBox.setGeometry(QtCore.QRect(100, 300, 156, 23))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)

        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")

        self.retranslateUi(dialogCreateBatch)

        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(dialogCreateBatch.reject)
        QtCore.QMetaObject.connectSlotsByName(dialogCreateBatch)

    def retranslateUi(self, dialogCreateBatch):
        _translate = QtCore.QCoreApplication.translate
        dialogCreateBatch.setWindowTitle(_translate("dialogCreateBatch", "Create Item Batch"))

    def accept(self):
        selectedItems = self.cboItemList.checkedItems()
        print(selectedItems)
        dialogCreateBatch.close

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    dialogCreateBatch = QtWidgets.QDialog()
    ui = Ui_dialogCreateBatch()
    ui.setupUi(dialogCreateBatch)
    dialogCreateBatch.show()
    sys.exit(app.exec_())