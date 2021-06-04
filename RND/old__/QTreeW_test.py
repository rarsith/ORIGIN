# import sys
# from PySide2.QtWidgets import *
# from PySide2.QtWidgets import QApplication, QWidget, QVBoxLayout, QTreeWidget, QTreeWidgetItem
#
# my_app = QApplication(sys.argv)
# my_window = QWidget()
# my_layout = QVBoxLayout(my_window)
#
# my_tree = QTreeWidget()
# my_tree.setHeaderLabels(['Name', 'Area(kmp)'])
# my_item_root = QTreeWidgetItem(my_tree, ['Romania', '238,397 kmp'])
# my_item_raw = QTreeWidgetItem(my_item_root, ['Black Sea', '436,402 kmp'])
#
# my_layout.addWidget(my_tree)
# my_window.show()
# sys.exit(my_app.exec_())


# import sys
# from PySide2.QtWidgets import QTreeWidget, QTreeWidgetItem, QApplication, QWidget
#
# if __name__ == '__main__':
#     # create a empty my_app application
#     my_app = ''
#     # test this my_app to create instance
#     if QApplication.instance() != None:
#         my_app = QApplication.instance()
#     else:
#         my_app = QApplication(sys.argv)
#     # create a QTreeWidgetItem with three columns
#     my_tree= QTreeWidgetItem(["Column A", "Column B", "Column C"])
#     # add data using a for loop
#     for i in range(6):
#         list_item_row = QTreeWidgetItem(["Child A-" + str(i), "Child B-" + str(i), "Child C-" + str(i)])
#         my_tree.addChild(list_item_row)
#     # create my_widget widget
#     my_widget = QWidget()
#     my_widget.resize(640, 180)
#     # create a QTreeWidget named my_tree_widget
#     my_tree_widget = QTreeWidget(my_widget)
#     # set the size
#     my_tree_widget.resize(640, 180)
#     # set the number of columns
#     my_tree_widget.setColumnCount(3)
#     # add labels for each column
#     my_tree_widget.setHeaderLabels(["Column A label", "Column B label", "Column C label"])
#     # add my_tree using addTopLevelItem
#     my_tree_widget.addTopLevelItem(my_tree)
#     # show the widget
#     my_widget.show()
#     # the exit of my_app
#     sys.exit(my_app.exec_())


from PySide2.QtWidgets import (QTreeWidget, QTreeWidgetItem, QPushButton, QLabel, QDialog, QVBoxLayout, QApplication, QLineEdit)
from PySide2.QtCore import Slot
import sys
class TreeWidgetWithWidgetItems(QDialog):
    def __init__(self):
        super(TreeWidgetWithWidgetItems, self).__init__()
        self.init_ui()
    def init_ui(self):
        # Creating the required widgets
        self.vboxLayout = QVBoxLayout()
        self.treeWidget = QTreeWidget()
        self.label = QLabel("I'm going to inform you about the buttons")
        # Adding the widgets
        self.vboxLayout.addWidget(self.treeWidget)
        self.vboxLayout.addWidget(self.label)
        self.treeWidget.setHeaderLabel("TreeWidget with Buttons")
        self.topLevelItem = QTreeWidgetItem()
        # Creating top level and child widgets
        self.topLevelButton = QPushButton("Top Level Button")
        self.childButton_1 = QPushButton("Child 1")
        self.childButton_2 = QPushButton("Child 2")
        self.childButton_3 = QPushButton("Child 3")
        self.childLineEdit = QLineEdit()
        self.childLineEdit.setPlaceholderText("Add Text Here")
        # .................(contd) .... part-1
#Nothing much to explain, created a QTreeWidget, a QVBoxLayout to put every widget in an organized way, some QPushButton(s) and a QLineEdit.
        # ..................(contd) ... from part-1
        # Adding the child to the top level item
        self.childItems = []
        for i in range(4):
            self.childItems.append(QTreeWidgetItem())
            self.topLevelItem.addChild(self.childItems[i])
        self.treeWidget.addTopLevelItem(self.topLevelItem)
        self.treeWidget.setItemWidget(self.topLevelItem, 0, self.topLevelButton)
        # Replacing the child items with widgets
        self.treeWidget.setItemWidget(self.childItems[0], 0, self.childButton_1)
        self.treeWidget.setItemWidget(self.childItems[1], 0, self.childButton_2)
        self.treeWidget.setItemWidget(self.childItems[2], 0, self.childButton_3)
        self.treeWidget.setItemWidget(self.childItems[3], 0, self.childLineEdit)
        # Connecting the widgets with corresponding slots
        self.topLevelButton.clicked.connect(self.top_button_clicked)
        self.childButton_1.clicked.connect(self.child_button_1_clicked)
        self.childButton_2.clicked.connect(self.child_button_2_clicked)
        self.childButton_3.clicked.connect(self.child_button_3_clicked)
        self.childLineEdit.textEdited.connect(self.child_lineedit_edited)
        # Setting the layout
        self.setWindowTitle("QTreeWidget with Button Example")
        self.setLayout(self.vboxLayout)
    # ............. (contd) ....... part-2
#Every QTreeWidgetItem created within the loop will be the children of the top level item. As before, I am calling the ‘setItemWidget’ function to add the widgets.
#Then I connected the widget with the slots which will be shown later on. Then I set the ‘vboxLayout’ as the main layout of the dialog.
    # ........... (contd) ........... from part-2
    # @Slot(bool)
    def top_button_clicked(self, clicked):
        self.label.setText("Top Level Button was Clicked")
    # @Slot(bool)
    def child_button_1_clicked(self, clicked):
        self.label.setText("Child button 1 was clicked")
    # @Slot(bool)
    def child_button_2_clicked(self, clicked):
        self.label.setText("Child button 2 was clicked")
    # @Slot(bool)
    def child_button_3_clicked(self, clicked):
        self.label.setText("Child button 3 was clicked")
    # @Slot('QString')
    def child_lineedit_edited(self, edited_text):
        self.label.setText(str(edited_text))
if __name__ == '__main__':
    app = QApplication(sys.argv)
    treeWidgetDialog = TreeWidgetWithWidgetItems()
    treeWidgetDialog.show()
    sys.exit(app.exec_())