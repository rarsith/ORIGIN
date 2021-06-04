import sys
from PySide2 import QtWidgets, QtCore

from xcg_data_base import xcg_db_actions as xac
from xcg_config import xcg_slot_methods as xmeth
from xcg_config import xcg_validation as xval
from xcg_ui.xcg_edit_task_pub_slot_ui import CreateTaskPubSlotsUI

class CreateTaskUI(QtWidgets.QDialog):

    def __init__(self, parent=None):
        super(CreateTaskUI, self).__init__(parent)

        self.setWindowTitle("Create Task")
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
        # self.entry_name_cb.addItems(self.get_entries())


        self.task_name_le = QtWidgets.QLineEdit()

        self.imports_from_lwd = QtWidgets.QListWidget()
        self.imports_from_lwd.setAlternatingRowColors(True)
        self.imports_from_lwd.setSelectionMode(QtWidgets.QListWidget.ExtendedSelection)

        self.existing_tasks_lwd = QtWidgets.QListWidget()
        self.existing_tasks_lwd.setAlternatingRowColors(True)
        self.existing_tasks_lwd.setSelectionMode(QtWidgets.QListWidget.ExtendedSelection)
        self.populate_existing_tasks()

        self.existing_tasks_lb = QtWidgets.QLabel("Existing Tasks")
        self.imports_from_lb = QtWidgets.QLabel("Imports From")


        self.task_status_cb = QtWidgets.QComboBox()
        self.task_status_cb.addItems(xval.VALID_TASK_STATUSES)

        # _______
        self.publish_slots_lb = QtWidgets.QLabel("Publish Slots")
        self.publish_slots_le = QtWidgets.QLineEdit()


        # _______

        self.tsk_pub_slot_wdg = QtWidgets.QTableWidget()
        self.initialize_pub_slots()

        self.add_btn = QtWidgets.QPushButton("Add Slot")
        self.refresh_list_btn = QtWidgets.QPushButton("Refresh")
        self.delete_list_item_btn = QtWidgets.QPushButton("Remove")

        self.move_right_btn = QtWidgets.QPushButton(">")
        self.move_right_btn.setMaximumWidth(40)
        self.reset_btn = QtWidgets.QPushButton("Reset")
        self.create_btn = QtWidgets.QPushButton("Create")
        self.create_and_close_btn = QtWidgets.QPushButton("Create and Close")
        self.cancel_btn = QtWidgets.QPushButton("Cancel")

    def create_layout(self):
        form_layout = QtWidgets.QFormLayout()
        form_layout.addRow("Show_name  ", self.show_name_cb)
        form_layout.addRow("Show Branch  ", self.show_branch_cb)
        form_layout.addRow("Category  ", self.category_cb)
        form_layout.addRow("Entry Name  ", self.entry_name_cb)
        form_layout.addRow("Task Name  ", self.task_name_le)
        form_layout.addRow("Task Status  ", self.task_status_cb)
        form_layout.setFormAlignment(QtCore.Qt.AlignLeft)
        form_layout.setLabelAlignment(QtCore.Qt.AlignRight)

        form_main_layout = QtWidgets.QHBoxLayout()
        form_main_layout.addLayout(form_layout)
        form_main_layout.setSpacing(5)

        existing_tasks_layout = QtWidgets.QVBoxLayout()
        existing_tasks_layout.addWidget(self.existing_tasks_lb)
        existing_tasks_layout.addWidget(self.existing_tasks_lwd)

        imports_from_layout = QtWidgets.QVBoxLayout()
        imports_from_layout.addWidget(self.imports_from_lb)
        imports_from_layout.addWidget(self.imports_from_lwd)

        imports_from_buttons_layout = QtWidgets.QVBoxLayout()
        imports_from_buttons_layout.addWidget(self.reset_btn)

        tasks_details_layout = QtWidgets.QHBoxLayout()
        tasks_details_layout.addLayout(existing_tasks_layout)
        tasks_details_layout.addWidget(self.move_right_btn)
        tasks_details_layout.addLayout(imports_from_layout)
        tasks_details_layout.addLayout(imports_from_buttons_layout)

        add_button_layout = QtWidgets.QHBoxLayout()
        add_button_layout.addWidget(self.publish_slots_le)
        add_button_layout.addWidget(self.add_btn)

        pub_slots_top_layout = QtWidgets.QVBoxLayout()
        pub_slots_top_layout.addWidget(self.publish_slots_lb)
        pub_slots_top_layout.addLayout(add_button_layout)

        main_list_buttons_layout = QtWidgets.QVBoxLayout()
        main_list_buttons_layout.addWidget(self.refresh_list_btn)
        main_list_buttons_layout.addWidget(self.delete_list_item_btn)
        main_list_buttons_layout.addStretch()

        pub_slots_tw_layout = QtWidgets.QHBoxLayout()
        pub_slots_tw_layout.addWidget(self.tsk_pub_slot_wdg)
        pub_slots_tw_layout.addLayout(main_list_buttons_layout)

        pub_slots_all_layout = QtWidgets.QVBoxLayout()
        pub_slots_all_layout.addLayout(pub_slots_top_layout)
        pub_slots_all_layout.addLayout(pub_slots_tw_layout)
        pub_slots_all_layout.setSpacing(5)

        buttons_layout = QtWidgets.QHBoxLayout()
        buttons_layout.addStretch()
        buttons_layout.addWidget(self.create_btn)
        buttons_layout.addWidget(self.create_and_close_btn)
        buttons_layout.addWidget(self.cancel_btn)

        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.addLayout(form_main_layout)
        main_layout.addSpacing(20)
        main_layout.addLayout(tasks_details_layout)
        main_layout.addLayout(pub_slots_all_layout)
        main_layout.addLayout(buttons_layout)

    def create_connections(self):
        self.show_name_cb.activated.connect(self.comboBox_shows)
        self.show_name_cb.activated.connect(self.populate_show_branches)
        self.show_name_cb.activated.connect(self.populate_categories)
        self.show_name_cb.activated.connect(self.populate_entries)
        self.show_name_cb.activated.connect(self.populate_existing_tasks)

        self.show_branch_cb.activated.connect(self.comboBox_show_branches)
        self.show_branch_cb.activated.connect(self.populate_categories)
        self.show_branch_cb.activated.connect(self.populate_entries)
        self.show_branch_cb.activated.connect(self.populate_existing_tasks)

        self.category_cb.activated.connect(self.comboBox_categories)
        self.category_cb.activated.connect(self.populate_entries)
        self.category_cb.activated.connect(self.populate_existing_tasks)

        self.entry_name_cb.activated.connect(self.comboBox_entries)
        self.entry_name_cb.activated.connect(self.populate_existing_tasks)


        self.add_btn.clicked.connect(self.add_to_pub_list)
        self.add_btn.setAutoDefault(True)

        self.move_right_btn.clicked.connect(self.move_selection_to_right)
        self.move_right_btn.clicked.connect(self.get_imports_from)

        self.reset_btn.clicked.connect(self.get_imports_from_list)
        self.reset_btn.clicked.connect(self.clear_list)
        self.reset_btn.clicked.connect(self.populate_existing_tasks)


        self.delete_list_item_btn.clicked.connect(self.remove_pub_slot)

        self.create_btn.clicked.connect(self.db_commit)
        self.create_and_close_btn.clicked.connect(self.db_commit_close)
        self.cancel_btn.clicked.connect(self.close)

    def initialize_pub_slots(self):
        self.tsk_pub_slot_wdg.setColumnCount(5)
        self.tsk_pub_slot_wdg.setHorizontalHeaderLabels(["Slot_Name", "Type", "Method", "R", "A", "S"])
        self.tsk_pub_slot_wdg.setShowGrid(False)
        self.tsk_pub_slot_wdg.setAlternatingRowColors(True)
        header = self.tsk_pub_slot_wdg.verticalHeader()
        header.hide()
        self.tsk_pub_slot_wdg.setColumnWidth(0, 150)
        self.tsk_pub_slot_wdg.setColumnWidth(1, 120)
        self.tsk_pub_slot_wdg.setColumnWidth(2, 100)
        self.tsk_pub_slot_wdg.setColumnWidth(3, 20)
        self.tsk_pub_slot_wdg.setColumnWidth(4, 20)

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

    def populate_show_branches(self):
        self.show_branch_cb.clear()
        self.show_branch_cb.addItems(self.get_show_branches())

    def populate_categories(self):
        self.category_cb.clear()
        self.category_cb.addItems(self.get_categories())

    def populate_entries(self):
        self.entry_name_cb.clear()
        self.entry_name_cb.addItems(self.get_entries())

    def populate_existing_tasks(self):
        self.existing_tasks_lwd.clear()
        self.existing_tasks_lwd.addItems(self.get_all_tasks())

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
        print (entries)
        return  entries

    def get_all_tasks(self):
        tasks = xac.get_tasks(self.show_name_cb.currentText(), self.show_branch_cb.currentText(),
                              self.category_cb.currentText(), self.entry_name_cb.currentText())
        return tasks

    def move_selection_to_right(self):
        text = self.existing_tasks_lwd.selectedItems()


        existing_items = self.get_imports_from()
        for item in text:
            if item.text() in existing_items:
                return
            else:
                self.imports_from_lwd.addItem(item.text())
                self.existing_tasks_lwd.takeItem(self.existing_tasks_lwd.row(item))

    def get_imports_from(self):
        list_all = []
        self.imports_from_lwd.selectAll()
        text = self.imports_from_lwd.selectedItems()
        for item in text:
            list_all.append(item.text())
        self.imports_from_lwd.clearSelection()
        return list_all

    def get_imports_from_list(self):
        list_all = []
        for item in range(self.imports_from_lwd.count()):
            list_all.append(self.imports_from_lwd.item(item).text())
        return list_all

    def clear_list(self):
        self.imports_from_lwd.clear()

    def create_pub_slots(self, name, row):
        item = QtWidgets.QTableWidgetItem(name)
        self.tsk_pub_slot_wdg.setItem(row, 0, item)

        self.set_type_cb = QtWidgets.QComboBox()
        self.set_type_cb.addItems(xval.SLOTS_TYPES)
        self.set_method_cb = QtWidgets.QComboBox()
        self.set_method_cb.addItems(list(xval.SLOTS_METHODS.values()))
        self.set_reviewable_ckb = QtWidgets.QCheckBox()
        self.set_active_ckb = QtWidgets.QCheckBox()

        # try:
        #     self.set_type_cb.setCurrentText(self.get_db_pub_type(name))
        #     self.set_reviewable_ckb.setChecked(self.get_db_pub_reviewable(name))
        #     self.set_active_ckb.setChecked(self.get_db_pub_active(name))
        #     # self.set_select_ckb.setChecked(self.get_db_pub_selected(name))
        # except:
        #     pass

        self.tsk_pub_slot_wdg.setCellWidget(row, 1, self.set_type_cb)
        self.tsk_pub_slot_wdg.setCellWidget(row, 2, self.set_method_cb)
        self.tsk_pub_slot_wdg.setCellWidget(row, 3, self.set_reviewable_ckb)
        self.tsk_pub_slot_wdg.setCellWidget(row, 4, self.set_active_ckb)

    def insert_pub_slot_row(self, name):
        self.tsk_pub_slot_wdg.insertRow(0)
        self.create_pub_slots(name, 0)

    def remove_pub_slot(self):
        listItems = self.tsk_pub_slot_wdg.currentItem()
        selected_index = self.tsk_pub_slot_wdg.indexFromItem(listItems)
        self.tsk_pub_slot_wdg.removeRow(selected_index.row())

    def get_slot_name(self, row, column):
        slot_name = self.tsk_pub_slot_wdg.item(row, column)
        return slot_name.text()

    def get_slot_type(self, row, column):
        slot_type = self.tsk_pub_slot_wdg.cellWidget(row, column)
        return slot_type.currentText()

    def get_slot_method(self, row, column):
        slot_method = self.tsk_pub_slot_wdg.cellWidget(row, column)
        return slot_method.currentText()

    def reviewable_is_checked(self, row, column):
        rev_checked = self.tsk_pub_slot_wdg.cellWidget(row, column)
        return rev_checked.isChecked()

    def active_is_checked(self, row, column):
        act_is_checked = self.tsk_pub_slot_wdg.cellWidget(row, column)
        return act_is_checked.isChecked()

    def get_pub_buffer_content(self):
        items = []
        rows = self.tsk_pub_slot_wdg.rowCount()
        for r in range(rows):
            dictionary_build = {self.get_slot_name(r, 0):{'type':self.get_slot_type(r, 1),'method':self.get_slot_method(r, 2) ,'reviewable':self.reviewable_is_checked(r, 3), 'active':self.active_is_checked(r, 4)}}
            items.append(dictionary_build)
        return items

    def get_db_pub_reviewable(self, slot):
        state = xac.get_pub_is_reviewable(self.show_name_cb.currentText(),
                              self.show_branch_cb.currentText(),
                              self.category_cb.currentText(),
                              self.entry_name_cb.currentText(),
                              self.task_name_cb.currentText(),
                                 slot)
        return state[0]

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
        xac.create_task(self.show_name_cb.currentText(),
                        self.show_branch_cb.currentText(),
                        self.category_cb.currentText(),
                        self.entry_name_cb.currentText(),
                        self.task_name_le.text())



        xac.update_task_pub_slot_dict(self.show_name_cb.currentText(),
                                      self.show_branch_cb.currentText(),
                                      self.category_cb.currentText(),
                                      self.entry_name_cb.currentText(),
                                      self.task_name_le.text(),
                                      pub_slot=self.get_pub_buffer_content())

        xac.update_task_imports_from(self.show_name_cb.currentText(),
                                     self.show_branch_cb.currentText(),
                                     self.category_cb.currentText(),
                                     self.entry_name_cb.currentText(),
                                     self.task_name_le.text(),
                                     imports_from = self.get_imports_from_list())

        self.task_name_le.clear()
        self.populate_existing_tasks()
        self.imports_from_lwd.clear()
        self.tsk_pub_slot_wdg.clear()
        self.tsk_pub_slot_wdg.setRowCount(0)
        self.initialize_pub_slots()



if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    create_shot = CreateTaskUI()
    create_shot.show()
    sys.exit(app.exec_())