import sys
from PySide2 import QtWidgets, QtCore

from origin_data_base import xcg_db_actions as xac
from origin_config import xcg_validation as xval

class SetTaskImportsFromUI(QtWidgets.QDialog):

    def __init__(self, parent=None):
        super(SetTaskImportsFromUI, self).__init__(parent)

        self.setWindowTitle("Task Imports From")
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

        self.imports_from_lwd = QtWidgets.QListWidget()
        self.imports_from_lwd.setAlternatingRowColors(True)
        self.imports_from_lwd.setSelectionMode(QtWidgets.QListWidget.ExtendedSelection)
        self.imports_from_lwd.addItems(self.get_saved_import_schema())

        self.existing_tasks_lwd = QtWidgets.QListWidget()
        self.existing_tasks_lwd.setAlternatingRowColors(True)
        self.existing_tasks_lwd.setSelectionMode(QtWidgets.QListWidget.ExtendedSelection)
        self.populate_existing_tasks_list()
        self.remove_self_task()
        self.remove_already_assigned()

        self.existing_tasks_lb = QtWidgets.QLabel("Existing Tasks")
        self.imports_from_lb = QtWidgets.QLabel("Imports From")

        self.move_right_btn = QtWidgets.QPushButton(">")
        self.move_right_btn.setMaximumWidth(40)
        self.reset_btn = QtWidgets.QPushButton("Reset")
        self.refresh_btn = QtWidgets.QPushButton("Refresh")
        self.create_btn = QtWidgets.QPushButton("Create")
        self.create_and_close_btn = QtWidgets.QPushButton("Create and Close")
        self.cancel_btn = QtWidgets.QPushButton("Cancel")

    def create_layout(self):
        form_layout = QtWidgets.QFormLayout()
        form_layout.addRow("Show_name ", self.show_name_cb)
        form_layout.addRow("Show Branch", self.show_branch_cb)
        form_layout.addRow("Category", self.category_cb)
        form_layout.addRow("Entry Name", self.entry_name_cb)
        form_layout.addRow("Task Name", self.task_name_cb)
        form_layout.setFormAlignment(QtCore.Qt.AlignLeft)
        form_layout.setLabelAlignment(QtCore.Qt.AlignLeft)

        existing_tasks_label_layout = QtWidgets.QVBoxLayout()
        existing_tasks_label_layout.addWidget(self.existing_tasks_lb)
        existing_tasks_label_layout.addWidget(self.existing_tasks_lwd)

        imports_from_label_layout = QtWidgets.QVBoxLayout()
        imports_from_label_layout.addWidget(self.imports_from_lb)
        imports_from_label_layout.addWidget(self.imports_from_lwd)

        imports_from_buttons_layout = QtWidgets.QVBoxLayout()
        imports_from_buttons_layout.addWidget(self.refresh_btn)
        imports_from_buttons_layout.addWidget(self.reset_btn)
        imports_from_buttons_layout.addStretch()

        imports_from_layout = QtWidgets.QHBoxLayout()
        imports_from_layout.addLayout(existing_tasks_label_layout)
        imports_from_layout.addWidget(self.move_right_btn)
        imports_from_layout.addLayout(imports_from_label_layout)
        imports_from_layout.addLayout(imports_from_buttons_layout)

        buttons_layout = QtWidgets.QHBoxLayout()
        buttons_layout.addStretch()
        buttons_layout.addWidget(self.create_btn)
        buttons_layout.addWidget(self.create_and_close_btn)
        buttons_layout.addWidget(self.cancel_btn)

        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.addLayout(form_layout)
        main_layout.addSpacing(30)
        main_layout.addLayout(imports_from_layout)
        main_layout.addLayout(buttons_layout)

    def create_connections(self):
        self.show_name_cb.currentIndexChanged.connect(self.comboBox_shows)
        self.show_name_cb.currentIndexChanged.connect(self.populate_show_branches)
        self.show_name_cb.currentIndexChanged.connect(self.populate_categories)
        self.show_name_cb.currentIndexChanged.connect(self.populate_entries)
        self.show_name_cb.currentIndexChanged.connect(self.clear_list)
        self.show_name_cb.currentIndexChanged.connect(self.populate_existing_assignments)
        self.show_name_cb.currentIndexChanged.connect(self.remove_already_assigned)

        self.show_name_cb.currentIndexChanged.connect(self.populate_existing_tasks_cb)
        self.show_name_cb.currentIndexChanged.connect(self.populate_existing_tasks_list)
        self.show_name_cb.currentIndexChanged.connect(self.remove_self_task)
        self.show_name_cb.currentIndexChanged.connect(self.populate_existing_assignments)
        self.show_name_cb.currentIndexChanged.connect(self.remove_already_assigned)


        self.show_branch_cb.currentIndexChanged.connect(self.comboBox_show_branches)
        self.show_branch_cb.currentIndexChanged.connect(self.populate_categories)
        self.show_branch_cb.currentIndexChanged.connect(self.populate_entries)
        self.show_branch_cb.currentIndexChanged.connect(self.clear_list)
        self.show_branch_cb.currentIndexChanged.connect(self.populate_existing_assignments)
        self.show_branch_cb.currentIndexChanged.connect(self.remove_already_assigned)


        self.show_branch_cb.currentIndexChanged.connect(self.populate_existing_tasks_cb)
        self.show_branch_cb.currentIndexChanged.connect(self.populate_existing_tasks_list)
        self.show_branch_cb.currentIndexChanged.connect(self.remove_self_task)
        self.show_branch_cb.currentIndexChanged.connect(self.populate_existing_assignments)
        self.show_branch_cb.currentIndexChanged.connect(self.remove_already_assigned)


        self.category_cb.currentIndexChanged.connect(self.comboBox_categories)
        self.category_cb.currentIndexChanged.connect(self.populate_entries)
        self.category_cb.currentIndexChanged.connect(self.clear_list)
        self.category_cb.currentIndexChanged.connect(self.populate_existing_tasks_cb)
        self.category_cb.currentIndexChanged.connect(self.populate_existing_tasks_list)
        self.category_cb.currentIndexChanged.connect(self.remove_self_task)
        self.category_cb.currentIndexChanged.connect(self.populate_existing_assignments)
        self.category_cb.currentIndexChanged.connect(self.remove_already_assigned)


        self.entry_name_cb.currentIndexChanged.connect(self.comboBox_entries)
        self.entry_name_cb.currentIndexChanged.connect(self.clear_list)
        self.entry_name_cb.currentIndexChanged.connect(self.populate_existing_tasks_list)
        self.entry_name_cb.currentIndexChanged.connect(self.populate_existing_tasks_cb)
        self.entry_name_cb.currentIndexChanged.connect(self.remove_self_task)
        self.entry_name_cb.currentIndexChanged.connect(self.populate_existing_assignments)
        self.entry_name_cb.currentIndexChanged.connect(self.remove_already_assigned)


        self.task_name_cb.currentIndexChanged.connect(self.clear_list)
        self.task_name_cb.currentIndexChanged.connect(self.populate_existing_tasks_list)
        self.task_name_cb.currentIndexChanged.connect(self.remove_self_task)
        self.task_name_cb.currentIndexChanged.connect(self.populate_existing_assignments)
        self.task_name_cb.currentIndexChanged.connect(self.remove_already_assigned)


        self.move_right_btn.clicked.connect(self.move_selection_to_right)
        self.move_right_btn.clicked.connect(self.get_imports_from)

        self.reset_btn.clicked.connect(self.get_imports_from_list)
        self.reset_btn.clicked.connect(self.clear_list)
        self.reset_btn.clicked.connect(self.populate_existing_tasks_list)
        self.reset_btn.clicked.connect(self.remove_self_task)

        self.refresh_btn.clicked.connect(self.populate_existing_tasks_list)
        self.refresh_btn.clicked.connect(self.populate_existing_assignments)
        self.refresh_btn.clicked.connect(self.remove_self_task)
        self.refresh_btn.clicked.connect(self.remove_already_assigned)



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

    def combobox_tasks(self):
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

    def populate_existing_tasks_list(self):
        self.existing_tasks_lwd.clear()
        all_tasks = self.get_all_tasks()
        if all_tasks == None:
            return []

        else:
            for i in all_tasks:
                QtWidgets.QListWidgetItem(i, self.existing_tasks_lwd)

    def populate_existing_tasks_cb(self):
        self.task_name_cb.clear()
        all_tasks = self.get_all_tasks()
        if all_tasks == None:
            return []
        else:
            self.task_name_cb.addItems(self.get_all_tasks())

    def populate_existing_assignments(self):
        self.imports_from_lwd.clear()
        self.imports_from_lwd.addItems(self.get_saved_import_schema())

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
        if entries != None:
            return entries
        else:
            return ["--empty category--"]

    def get_all_tasks(self):
        tasks = xac.get_tasks(self.show_name_cb.currentText(), self.show_branch_cb.currentText(),
                              self.category_cb.currentText(), self.entry_name_cb.currentText())
        if tasks != None:
            return tasks
        else:
            return ["-- no tasks --"]

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

    def get_saved_import_schema(self):
        existing_imports_from = xac.get_task_imports_from(self.show_name_cb.currentText(),
                                                          self.show_branch_cb.currentText(),
                                                          self.category_cb.currentText(),
                                                          self.entry_name_cb.currentText(),
                                                          self.task_name_cb.currentText())
        if existing_imports_from == None:
            return []
        else:
            return existing_imports_from

    def clear_list(self):
        self.imports_from_lwd.clear()

    def remove_self_task(self):
        entries = self.task_name_cb.findText(self.task_name_cb.currentText(), QtCore.Qt.MatchFixedString)
        if entries >= 0:
            self.existing_tasks_lwd.takeItem(entries)

    def remove_already_assigned(self):
        existing_assignments = self.get_imports_from()
        for task_name in existing_assignments:
            entries = self.existing_tasks_lwd.findItems(task_name, QtCore.Qt.MatchFixedString)
            for entry in entries:
                indexes = self.existing_tasks_lwd.indexFromItem(entry)
                self.existing_tasks_lwd.takeItem(indexes.row())

    def db_commit_close(self):
        self.db_commit()
        self.close()

    def db_commit(self):
        xac.remove_all_task_import_slots(self.show_name_cb.currentText(),
                                  self.show_branch_cb.currentText(),
                                  self.category_cb.currentText(),
                                  self.entry_name_cb.currentText(),
                                  self.task_name_cb.currentText())


        xac.update_task_imports_from(self.show_name_cb.currentText(),
                                     self.show_branch_cb.currentText(),
                                     self.category_cb.currentText(),
                                     self.entry_name_cb.currentText(),
                                     self.task_name_cb.currentText(),
                                     imports_from = self.get_imports_from_list())

        self.populate_existing_tasks_list()
        self.populate_existing_assignments()
        self.remove_self_task()

        self.remove_already_assigned()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    create_shot = SetTaskImportsFromUI()
    create_shot.show()
    sys.exit(app.exec_())