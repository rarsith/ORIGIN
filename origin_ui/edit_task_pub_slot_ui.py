import sys
from PySide2 import QtWidgets, QtCore

from origin_data_base import xcg_db_actions as xac
from RND import xcg_task_publishing_slots_wdg


class CreateTaskPubSlotsUI(QtWidgets.QDialog):

    def __init__(self, parent=None):
        super(CreateTaskPubSlotsUI, self).__init__(parent)

        self.setWindowTitle("Edit Task Publish Slots")
        self.setMinimumSize(550, 650)
        self.setMaximumSize(550, 650)

        self.setMinimumHeight(900)
        self.setMaximumHeight(900)

        self.create_widgets()
        self.create_layout()
        self.create_connections()

    def create_widgets(self):
        self.show_name_cb = QtWidgets.QComboBox()
        self.show_name_cb.addItems(self.get_shows())

        self.show_branch_cb = QtWidgets.QComboBox()
        self.show_branch_cb.addItems(self.get_show_branches())

        self.category_cb = QtWidgets.QComboBox()
        self.category_cb.addItems(self.get_categories())

        self.entry_name_cb = QtWidgets.QComboBox()
        self.entry_name_cb.addItems(self.get_entries())

        self.task_name_cb = QtWidgets.QComboBox()
        self.task_name_cb.addItems(self.get_all_tasks())

        self.publish_slots_lb = QtWidgets.QLabel("Publish Slots")
        self.publish_slots_le = QtWidgets.QLineEdit()

        self.add_btn = QtWidgets.QPushButton("Add Slot")
        self.refresh_list_btn = QtWidgets.QPushButton("Refresh")
        self.delete_list_item_btn = QtWidgets.QPushButton("Remove")

        self.task_pub_slots_wdg = xcg_task_publishing_slots_wdg.PublishSlotsWidget()
        self.task_pub_slots_wdg.setMinimumWidth(410)
        self.task_pub_slots_wdg.setColumnCount(6)
        self.task_pub_slots_wdg.setColumnWidth(0, 100)
        self.task_pub_slots_wdg.setColumnWidth(1, 80)
        self.task_pub_slots_wdg.setColumnWidth(2, 100)
        self.task_pub_slots_wdg.setColumnWidth(3, 80)
        self.task_pub_slots_wdg.setColumnWidth(4, 20)
        self.task_pub_slots_wdg.setColumnWidth(5, 20)

        self.populate_pub_slots()

        self.create_btn = QtWidgets.QPushButton("Apply")
        self.create_and_close_btn = QtWidgets.QPushButton("Apply and Close")
        self.cancel_btn = QtWidgets.QPushButton("Cancel")

    def create_layout(self):
        form_layout = QtWidgets.QFormLayout()
        form_layout.addRow("Show_name ", self.show_name_cb)
        form_layout.addRow("Show Branch", self.show_branch_cb)
        form_layout.addRow("Category", self.category_cb)
        form_layout.addRow("Entry Name", self.entry_name_cb)
        form_layout.addRow("Task Name", self.task_name_cb)
        form_layout.setSpacing(5)
        form_layout.setFormAlignment(QtCore.Qt.AlignLeft)
        form_layout.setLabelAlignment(QtCore.Qt.AlignRight)

        add_button_layout = QtWidgets.QHBoxLayout()
        add_button_layout.addWidget(self.publish_slots_le)
        add_button_layout.addWidget(self.add_btn)

        main_list_buttons_layout = QtWidgets.QVBoxLayout()
        main_list_buttons_layout.addWidget(self.refresh_list_btn)
        main_list_buttons_layout.addWidget(self.delete_list_item_btn)
        main_list_buttons_layout.addStretch()

        pub_slots_main_layout = QtWidgets.QHBoxLayout()
        pub_slots_main_layout.addWidget(self.task_pub_slots_wdg)
        pub_slots_main_layout.addLayout(main_list_buttons_layout)

        pub_slots_layout = QtWidgets.QVBoxLayout()
        pub_slots_layout.addWidget(self.publish_slots_lb)
        pub_slots_layout.addLayout(add_button_layout)

        buttons_layout = QtWidgets.QHBoxLayout()
        buttons_layout.addStretch()
        buttons_layout.addWidget(self.create_btn)
        buttons_layout.addWidget(self.create_and_close_btn)
        buttons_layout.addWidget(self.cancel_btn)

        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.addLayout(form_layout)
        main_layout.addSpacing(30)
        main_layout.addLayout(pub_slots_layout)
        main_layout.addLayout(pub_slots_main_layout)
        main_layout.addLayout(buttons_layout)

    def create_connections(self):
        self.show_name_cb.currentIndexChanged.connect(self.comboBox_shows)
        self.show_name_cb.currentIndexChanged.connect(self.populate_show_branches)
        self.show_name_cb.currentIndexChanged.connect(self.populate_categories)
        self.show_name_cb.currentIndexChanged.connect(self.populate_entries)
        self.show_name_cb.currentIndexChanged.connect(self.populate_tasks)
        self.show_name_cb.currentIndexChanged.connect(self.populate_pub_slots)

        self.show_branch_cb.currentIndexChanged.connect(self.comboBox_show_branches)
        self.show_branch_cb.currentIndexChanged.connect(self.populate_categories)
        self.show_branch_cb.currentIndexChanged.connect(self.populate_entries)
        self.show_branch_cb.currentIndexChanged.connect(self.populate_tasks)
        self.show_branch_cb.currentIndexChanged.connect(self.populate_pub_slots)

        self.category_cb.currentIndexChanged.connect(self.comboBox_categories)
        self.category_cb.currentIndexChanged.connect(self.populate_entries)
        self.category_cb.currentIndexChanged.connect(self.populate_tasks)
        self.category_cb.currentIndexChanged.connect(self.populate_pub_slots)

        self.entry_name_cb.currentIndexChanged.connect(self.comboBox_entries)
        self.entry_name_cb.currentIndexChanged.connect(self.populate_tasks)
        self.entry_name_cb.currentIndexChanged.connect(self.populate_pub_slots)

        self.task_name_cb.currentIndexChanged.connect(self.comboBox_tasks)
        self.task_name_cb.currentIndexChanged.connect(self.populate_pub_slots)

        self.refresh_list_btn.clicked.connect(self.populate_pub_slots)
        self.delete_list_item_btn.clicked.connect(self.task_pub_slots_wdg.remove_pub_slot)
        self.add_btn.clicked.connect(self.add_to_pub_list)

        self.create_btn.clicked.connect(self.db_commit)
        self.create_and_close_btn.clicked.connect(self.db_commit_close)
        self.cancel_btn.clicked.connect(self.close)

    def comboBox_shows(self):
        text = self.show_name_cb.currentText()
        return text

    def comboBox_show_branches(self):
        show_branch_text = self.show_branch_cb.currentText()
        return show_branch_text

    def comboBox_categories(self):
        category_text = self.category_cb.currentText()
        return category_text

    def comboBox_entries(self):
        entry_text = self.entry_name_cb.currentText()
        return entry_text

    def comboBox_tasks(self):
        task_text = self.task_name_cb.currentText()
        return task_text

    def populate_show_branches(self):
        self.show_branch_cb.clear()
        self.show_branch_cb.addItems(self.get_show_branches())

    def populate_categories(self):
        self.category_cb.clear()
        self.category_cb.addItems(self.get_categories())

    def populate_entries(self):
        self.entry_name_cb.clear()
        self.entry_name_cb.addItems(self.get_entries())

    def populate_tasks(self):
        self.task_name_cb.clear()
        all_tasks = self.get_all_tasks()
        if all_tasks == None:
            return[]
        else:
            self.task_name_cb.addItems(self.get_all_tasks())

    def get_current_path(self):
        self.task_pub_slots_wdg.show_sel = self.show_name_cb.currentText()
        self.task_pub_slots_wdg.branch = self.show_branch_cb.currentText()
        self.task_pub_slots_wdg.category = self.category_cb.currentText()
        self.task_pub_slots_wdg.entry = self.entry_name_cb.currentText()
        self.task_pub_slots_wdg.task = self.task_name_cb.currentText()

    def populate_pub_slots(self):
        self.get_current_path()
        self.task_pub_slots_wdg.populate_pub_slots()

    def insert_pub_slot_row(self, name):
        self.task_pub_slots_wdg.insertRow(0)
        self.task_pub_slots_wdg.create_pub_slots(name, 0)

    def get_shows(self):
        shows = xac.get_all_active_shows()
        return shows

    def get_show_branches(self):
        show_branches = xac.get_show_branches_structure(self.show_name_cb.currentText())
        return show_branches

    def get_categories(self):
        sequences = xac.get_sub_branches(self.show_name_cb.currentText(), self.show_branch_cb.currentText())
        return sequences

    def get_entries(self):
        entries = xac.get_sub_branches_content(self.show_name_cb.currentText(), self.show_branch_cb.currentText(), self.category_cb.currentText())
        return  entries

    def get_all_tasks(self):
        tasks = xac.get_tasks(self.show_name_cb.currentText(), self.show_branch_cb.currentText(),
                              self.category_cb.currentText(), self.entry_name_cb.currentText())
        j = ["--empty--"]

        if tasks != None:
            self.entry_name_cb.setDisabled(False)
            return tasks
        elif tasks == None:
            self.entry_name_cb.setDisabled(True)
            return j


    def add_to_pub_list(self):
        if self.publish_slots_le.text():
            self.insert_pub_slot_row(self.publish_slots_le.text())
            self.publish_slots_le.clear()
        else:
            return

    def db_commit_close(self):
        self.db_commit()
        self.close()

    def db_commit(self):
        self.task_pub_slots_wdg.db_commit()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    create_shot = CreateTaskPubSlotsUI()
    create_shot.show()
    sys.exit(app.exec_())