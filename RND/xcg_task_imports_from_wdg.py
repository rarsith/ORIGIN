import sys
import pprint
from PySide2 import QtWidgets, QtCore, QtGui
from origin_data_base import xcg_db_connection as xcon
from origin_data_base import xcg_db_actions as xac




db = xcon.server.exchange
test_position = db.show_name
test = test_position.find({}, {"_id":1, "show_name":1})


class ImportsFromWidget(QtWidgets.QTreeWidget):
    def __init__(self, parent=None):
        super(ImportsFromWidget, self).__init__(parent)

        self.show_name = ''
        self.branch_name = ''
        self.category_name = ''
        self.entry_name = ''
        self.task_name = ''

        self.connect_to_database()
        self.widget_build()

    def connect_to_database(self):
        db = xcon.server.exchange

    def widget_build(self):
        self.setAlternatingRowColors(True)
        self.setHeaderLabels(['task', 'Preview'])
        self.setMinimumWidth(310)
        self.setMaximumWidth(310)
        self.setMinimumHeight(300)
        self.setColumnWidth(0, 170)
        self.setColumnWidth(1, 80)

    def populate_task_import_schema(self):
        # self.get_path()
        get_schema = self.get_saved_import_schema()
        get_active_tasks = []
        self.clear()
        for task in get_schema:
            is_active = xac.get_task_is_active(self.show_name,
                                               self.branch_name,
                                               self.category_name,
                                               self.entry_name,
                                               task)
            if is_active[0] == True:
                get_active_tasks.append(task)
        self.add_items_to_list(get_active_tasks)

    def add_items_to_list(self, items):

        for active_task in items:

            imp_from_pub_slots_Schema = self.get_pub_imports(active_task)
            item = QtWidgets.QTreeWidgetItem([active_task])

            self.review_btn = QtWidgets.QPushButton('-->')
            self.addTopLevelItem(item)
            self.setItemWidget(item, 1, self.review_btn)
            self.review_btn.clicked.connect(self.show_curr_item)

            slot_used_by = self.get_pub_used_by(imp_from_pub_slots_Schema, self.task_name)

            try:
                for k, v in imp_from_pub_slots_Schema.items():
                    self.x = QtWidgets.QTreeWidgetItem([k])
                    self.go_to_btn = QtWidgets.QPushButton('go to')
                    item.addChild(self.x)

                    if self.x.text(0) in slot_used_by:
                        self.x.setCheckState(0, QtCore.Qt.Checked)
                    else:
                        self.x.setCheckState(0, QtCore.Qt.Unchecked)

                    self.setItemWidget(self.x, 1, self.go_to_btn)
                    self.go_to_btn.clicked.connect(self.show_curr_item)
                # self.expandAll()
            except:
                pass

    def show_curr_item(self):
        item = self.currentItem()
        item_index = self.currentIndex()

        if item_index.isValid():
            try:
                parent = item.parent()
                print ('Open Menu for {0} >>> Parent >>>> {1}'.format(item.text(0), parent.text(0)))
            except:
                pass

    def handle_item_changed(self, item, column):
        item_parent = item.parent()
        try:
            if item.checkState(column) == QtCore.Qt.Checked:
                print('{0} Item Checked, with {1} Parent'.format(item.text(0), item_parent.text(0)))
            elif item.checkState(column) == QtCore.Qt.Unchecked:
                print('{0} Item Unchecked, with {1} Parent'.format(item.text(0), item_parent.text(0)))
        except:
            pass

    def get_saved_import_schema(self):
        existing_imports_from = xac.get_task_imports_from (self.show_name,
                                                           self.branch_name,
                                                           self.category_name,
                                                           self.entry_name,
                                                           self.task_name)
        if existing_imports_from == None:
            return []
        else:
            return existing_imports_from

    def get_pub_imports(self, import_tasks):
        pub_imports = xac.get_pub_slots(self.show_name,
                                        self.branch_name,
                                        self.category_name,
                                        self.entry_name,
                                        import_tasks)

        return pub_imports

    def get_pub_used_by(self, extract, task):
        rel_task = xac.get_pub_used_by_task(extract, task)
        return rel_task

    def get_wdg_top_level_items_list(self):
        list_all = []
        nnn = self.topLevelItemCount()
        ccc = self.invisibleRootItem()
        for each_item in (range(nnn)):
            sel = ccc.child(each_item)
            list_all.append(sel.text(0))
        return list_all

    def get_all_items(self):
        checked = dict()
        root = self.invisibleRootItem()
        signal_count = root.childCount()

        for i in range(signal_count):
            signal = root.child(i)
            checked_sweeps = list()
            num_children = signal.childCount()

            for n in range(num_children):
                child = signal.child(n)
                checked_sweeps.append(child.text(0))
                checked[signal.text(0)] = checked_sweeps

        return checked

    def get_wdg_checked_items(self):
        checked = dict()
        root = self.invisibleRootItem()
        signal_count = root.childCount()

        for i in range(signal_count):
            signal = root.child(i)
            checked_sweeps = list()
            num_children = signal.childCount()

            for n in range(num_children):
                child = signal.child(n)

                if child.checkState(0) == QtCore.Qt.Checked:
                    checked_sweeps.append(child.text(0))

            checked[signal.text(0)] = checked_sweeps
        return checked

    def get_wdg_unchecked_items(self):
        unchecked = dict()
        root = self.invisibleRootItem()
        signal_count = root.childCount()

        for i in range(signal_count):
            signal = root.child(i)
            checked_sweeps = list()
            num_children = signal.childCount()

            for n in range(num_children):
                child = signal.child(n)

                if child.checkState(0) == QtCore.Qt.Unchecked:
                    checked_sweeps.append(child.text(0))

            unchecked[signal.text(0)] = checked_sweeps

        return unchecked

    def write_wdg_checked_items(self):
        checked_items = self.get_wdg_checked_items()
        unchecked_items = self.get_wdg_unchecked_items()
        for k, v in checked_items.items():
            for each in v:
                xac.update_task_pub_used_by(self.show_name,
                                            self.branch_name,
                                            self.category_name,
                                            self.entry_name,
                                            k,
                                            each,
                                            self.task_name
                                            )
        for k, v in unchecked_items.items():
            for each in v:
                xac.update_task_pub_used_by(self.show_name,
                                            self.branch_name,
                                            self.category_name,
                                            self.entry_name,
                                            k,
                                            each,
                                            self.task_name,
                                            remove_action=True)

    def clean_wdg(self, sel_item):
        checked = dict()
        signal_count = sel_item.childCount()
        checked_sweeps = list()
        for i in range(signal_count):
            signal = sel_item.child(i)
            if signal.checkState(0) == QtCore.Qt.Checked:
                checked_sweeps.append(signal.text(0))
            checked[sel_item.text(0)] = checked_sweeps

        for k, v in checked.items():
            for each in v:
                xac.update_task_pub_used_by(self.show_name,
                                            self.branch_name,
                                            self.category_name,
                                            self.entry_name,
                                            k,
                                            each,
                                            self.task_name,
                                            remove_action=True)

    def remove_import_task_slot(self):
        listItems = self.currentItem()
        self.clean_wdg(listItems)
        selected_index = self.indexFromItem(listItems)
        remove_it = selected_index.row()
        self.takeTopLevelItem(remove_it)

    def save_to_database(self):

        self.write_wdg_checked_items()

        xac.remove_all_task_import_slots(self.show_name,
                                         self.branch_name,
                                         self.category_name,
                                         self.entry_name,
                                         self.task_name)

        xac.update_task_imports_from(self.show_name,
                                     self.branch_name,
                                     self.category_name,
                                     self.entry_name,
                                     self.task_name,
                                     imports_from=self.get_wdg_top_level_items_list())


class ListEntryTasks(QtWidgets.QListWidget):
    def __init__(self, parent=None):
        super(ListEntryTasks, self).__init__(parent)

        self.show_name = ''
        self.branch_name = ''
        self.category_name = ''
        self.entry_name = ''
        self.task_name = ''


        self.widget_build()
        self.populate()

    def widget_build(self):
        self.setMaximumWidth(200)
        self.setAlternatingRowColors(True)
        self.setSelectionMode(QtWidgets.QListWidget.ExtendedSelection)

    def populate(self):
        self.clear()
        all_tasks = self.get_all_tasks()
        if all_tasks == None:
            return []

        else:
            for i in all_tasks:
                QtWidgets.QListWidgetItem(i, self)

    def get_all_tasks(self):
        tasks = xac.get_tasks(self.show_name, self.branch_name, self.category_name, self.entry_name)

        if tasks != None:
            return tasks
        else:
            return ["-- no tasks --"]

    def remove_self_task(self):
        get_task = self.task_name
        entries = self.findItems(get_task, QtCore.Qt.MatchFixedString)
        for entry in entries:
            indexes = self.indexFromItem(entry)
            self.takeItem(indexes.row())


class TasksImportFromUI(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(TasksImportFromUI, self).__init__(parent)


        self.create_widgets()
        self.create_layout()
        self.create_connections()

        self.populate()
        self.remove_already_assigned()
        self.existing_tasks_lwd.remove_self_task()

    def create_widgets(self):
        self.imports_from_wdg = ImportsFromWidget()
        self.existing_tasks_lwd = ListEntryTasks()

        self.tasks_existing_lb = QtWidgets.QLabel("Existing Tasks")
        self.tasks_imports_from_properties_lb = QtWidgets.QLabel("Imports From")

        self.remove_already_assigned()
        self.existing_tasks_lwd.remove_self_task()

        self.move_to_right_btn = QtWidgets.QPushButton(">")
        self.move_to_right_btn.setMinimumHeight(150)
        self.move_to_right_btn.setMinimumWidth(20)
        self.move_to_right_btn.setMaximumWidth(20)

        self.rem_sel_item_btn = QtWidgets.QPushButton("Remove Selected")
        self.save_btn = QtWidgets.QPushButton("Commit")
        self.refresh_btn = QtWidgets.QPushButton("Refresh")

    def create_layout(self):
        import_from_layout = QtWidgets.QVBoxLayout()
        import_from_layout.addWidget(self.tasks_imports_from_properties_lb)
        import_from_layout.addWidget(self.imports_from_wdg)

        widget_buttons_layout = QtWidgets.QVBoxLayout()
        widget_buttons_layout.addWidget(self.rem_sel_item_btn)
        widget_buttons_layout.addWidget(self.save_btn)
        widget_buttons_layout.addWidget(self.refresh_btn)

        move_button_layout = QtWidgets.QHBoxLayout()
        move_button_layout.addWidget(self.move_to_right_btn)

        existing_tasks_layout = QtWidgets.QVBoxLayout()
        existing_tasks_layout.addWidget(self.tasks_existing_lb)
        existing_tasks_layout.addWidget(self.existing_tasks_lwd)

        windows_layout = QtWidgets.QHBoxLayout()
        windows_layout.addLayout(existing_tasks_layout)
        windows_layout.addLayout(move_button_layout)
        windows_layout.addLayout(import_from_layout)

        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.addLayout(windows_layout)
        main_layout.addLayout(widget_buttons_layout)

    def create_connections(self):
        self.save_btn.clicked.connect(self.imports_from_wdg.save_to_database)
        self.rem_sel_item_btn.clicked.connect(self.imports_from_wdg.remove_import_task_slot)
        self.refresh_btn.clicked.connect(self.populate)
        self.move_to_right_btn.clicked.connect(self.move_selection_to_right)

    def populate(self):
        self.imports_from_wdg.populate_task_import_schema()
        self.existing_tasks_lwd.populate()
        self.existing_tasks_lwd.remove_self_task()
        self.remove_already_assigned()

    def get_imports_from(self):
        list_all = []
        nnn = self.imports_from_wdg.topLevelItemCount()
        ccc = self.imports_from_wdg.invisibleRootItem()
        for each_item in (range(nnn)):
            sel = ccc.child(each_item)
            list_all.append(sel.text(0))
        return list_all

    def remove_already_assigned(self):
        existing_assignments = self.get_imports_from()
        for task_name in existing_assignments:
            entries = self.existing_tasks_lwd.findItems(task_name, QtCore.Qt.MatchFixedString)
            for entry in entries:
                indexes = self.existing_tasks_lwd.indexFromItem(entry)
                self.existing_tasks_lwd.takeItem(indexes.row())

    def move_selection_to_right(self):
        text = self.existing_tasks_lwd.selectedItems()
        for item in text:
            self.imports_from_wdg.add_items_to_list([item.text()])
            print ("{0} item added to schema".format (item.text()))
            self.existing_tasks_lwd.takeItem(self.existing_tasks_lwd.row(item))
            self.imports_from_wdg.collapseAll()



if __name__ == "__main__":

    # huhu = {'full_range_in': 'ingest plate', 'full_range_out': 'ingest plate', 'frame_in': '1001', 'frame_out': '1200', 'handles_head': '8', 'handles_tail': '8', 'preroll': '10', 'shot_type': 'vfx', 'cut_in': '1009', 'cut_out': '1192', 'frame_rate': '24', 'motion_blur_high': '0.25', 'motion_blur_low': '-0.25', 'res_x': 'from plate', 'res_y': 'from plate'}
    # huhu2 = {'full_range_in': 'ingest XXXlXXXteXX'}

    app = QtWidgets.QApplication(sys.argv)
    test_dialog = TasksImportFromUI()

    test_dialog.existing_tasks_lwd.show_name = 'Test'
    test_dialog.existing_tasks_lwd.branch_name = 'sequences'
    test_dialog.existing_tasks_lwd.category_name = 'TST'
    test_dialog.existing_tasks_lwd.entry_name = '0100'
    test_dialog.existing_tasks_lwd.task_name = 'animation'

    test_dialog.imports_from_wdg.show_name = 'Test'
    test_dialog.imports_from_wdg.branch_name = 'sequences'
    test_dialog.imports_from_wdg.category_name = 'TST'
    test_dialog.imports_from_wdg.entry_name = '0100'
    test_dialog.imports_from_wdg.task_name = 'animation'

    test_dialog.populate()




    test_dialog.show()
    sys.exit(app.exec_())