import sys
from PySide2 import QtWidgets


class PublishSlotsWidgetBuild(QtWidgets.QTableWidget):
    def __init__(self, parent=None):
        super(PublishSlotsWidgetBuild, self).__init__(parent)

        self.show_sel = ''
        self.branch = ''
        self.category = ''
        self.entry = ''
        self.task = ''


        self.widget_build()

    def widget_build(self):
        self.setDisabled(False)
        self.setMinimumWidth(465)
        self.setColumnCount(6)
        self.setHorizontalHeaderLabels(["Slot_Name", "Type", "Method", "Source","R", "A"])
        self.setShowGrid(False)
        # self.setAlternatingRowColors(True)
        header = self.verticalHeader()
        header.hide()
        self.setColumnWidth(0, 100)
        self.setColumnWidth(1, 80)
        self.setColumnWidth(2, 95)
        self.setColumnWidth(3, 80)
        self.setColumnWidth(4, 20)
        self.setColumnWidth(5, 20)


class PublishSlotsWidgetUI(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(PublishSlotsWidgetUI, self).__init__(parent)


        self.create_widgets()
        self.create_layout()

    def create_widgets(self):
        self.tasks_pub_slots_properties_lb = QtWidgets.QLabel("Publishing Slots")

        self.add_pub_slot_le = QtWidgets.QLineEdit()
        self.add_pub_slot_le.setPlaceholderText('New Slot Name!')
        self.add_pub_slot_btn = QtWidgets.QPushButton('Add')

        self.publish_slots_wdg = PublishSlotsWidgetBuild()
        self.delete_list_item_btn = QtWidgets.QPushButton("Remove Selected")
        self.save_btn = QtWidgets.QPushButton("Commit")
        self.refresh_btn = QtWidgets.QPushButton("Refresh")

    def create_layout(self):
        top_layout = QtWidgets.QHBoxLayout()
        top_layout.addWidget(self.add_pub_slot_le)
        top_layout.addWidget(self.add_pub_slot_btn)

        layout = QtWidgets.QVBoxLayout()
        layout.addLayout(top_layout)
        layout.addWidget(self.publish_slots_wdg)
        layout.addWidget(self.delete_list_item_btn)
        layout.addWidget(self.save_btn)
        layout.addWidget(self.refresh_btn)

        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.addWidget(self.tasks_pub_slots_properties_lb)
        main_layout.addLayout(layout)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    test_dialog = PublishSlotsWidgetUI()
    test_dialog.show()
    sys.exit(app.exec_())