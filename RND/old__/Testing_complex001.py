import sys
from PySide2 import QtWidgets, QtCore, QtGui



class stackedExample(QtWidgets.QWidget):

    def __init__(self):
        super(stackedExample, self).__init__()
        self.leftlist = QtWidgets.QListWidget()

        self.leftlist.insertItem(0, 'Contact')
        self.leftlist.insertItem(1, 'Personal')
        self.leftlist.insertItem(2, 'Educational')

        self.task_import_from = QtWidgets.QLineEdit()
        self.task_pub_slots = QtWidgets.QLineEdit()
        self.task_user = QtWidgets.QLineEdit()

        self.stack1 = QtWidgets.QWidget()
        self.stack2 = QtWidgets.QWidget()
        self.stack3 = QtWidgets.QWidget()

        self.stack1UI()
        self.stack2UI()
        self.stack3UI()

        self.Stack = QtWidgets.QStackedWidget(self)
        self.Stack.addWidget(self.stack1)
        self.Stack.addWidget(self.stack2)
        self.Stack.addWidget(self.stack3)

        hbox = QtWidgets.QHBoxLayout(self)
        hbox.addWidget(self.leftlist)
        hbox.addWidget(self.Stack)

        self.setLayout(hbox)
        self.leftlist.currentRowChanged.connect(self.display)
        self.setGeometry(300, 50, 10, 10)
        self.setWindowTitle('StackedWidget demo')
        self.show()


    def stack1UI(self):
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.task_import_from)
        layout.addWidget(self.task_pub_slots)
        layout.addWidget(self.task_user)
        # self.setTabText(0,"Contact Details")
        self.stack1.setLayout(layout)


    def stack2UI(self):
        layout = QtWidgets.QFormLayout()
        sex = QtWidgets.QHBoxLayout()
        sex.addWidget(QtWidgets.QRadioButton("Male"))
        sex.addWidget(QtWidgets.QRadioButton("Female"))
        layout.addRow(QtWidgets.QLabel("Sex"), sex)
        layout.addRow("Date of Birth", QtWidgets.QLineEdit())

        self.stack2.setLayout(layout)


    def stack3UI(self):
        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(QtWidgets.QLabel("subjects"))
        layout.addWidget(QtWidgets.QCheckBox("Physics"))
        layout.addWidget(QtWidgets.QCheckBox("Maths"))
        self.stack3.setLayout(layout)


    def display(self, i):
        self.Stack.setCurrentIndex(i)


def main():
    app = QtWidgets.QApplication(sys.argv)
    ex = stackedExample()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()