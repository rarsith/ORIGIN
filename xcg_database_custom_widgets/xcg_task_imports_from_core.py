import sys
from PySide2 import QtWidgets, QtCore
from xcg_data_base import xcg_db_connection as xcon
from xcg_data_base import xcg_db_actions as xac
from xcg_database_custom_widgets.xcg_task_imports_from_UI import TasksImportFromUI


class TasksImportFromCore(TasksImportFromUI):
    def __init__(self, show_name='',
                         branch_name='',
                         category_name='',
                         entry_name='',
                         task_name='',
                         parent=None):
        super(TasksImportFromCore, self).__init__(parent)

        self.show_name = show_name
        self.branch_name = branch_name
        self.category_name = category_name
        self.entry_name = entry_name
        self.task_name = task_name

        self.create_connections()

        self.populate_main_widget()

    def create_connections(self):
        self.save_btn.clicked.connect(self.save_to_database)
        self.rem_sel_item_btn.clicked.connect(self.remove_import_task_slot)
        self.refresh_btn.clicked.connect(self.populate_main_widget)
        self.move_to_right_btn.clicked.connect(self.move_selection_to_right)

    def populate_main_widget(self):
        self.populate_existing_tasks()
        self.populate_task_import_schema()
        self.remove_already_assigned()
        self.remove_self_task()

# ImportsFromWidget -- START
    def populate_task_import_schema(self):
        # self.get_path()
        get_schema = self.get_saved_import_schema()
        get_active_tasks = []
        self.imports_from_wdg.clear()
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

            # self.review_btn = QtWidgets.QPushButton('-->')
            self.imports_from_wdg.addTopLevelItem(item)
            # self.imports_from_wdg.setItemWidget(item, 1, self.review_btn)
            # self.review_btn.clicked.connect(self.show_curr_item)

            slot_used_by = self.get_pub_used_by(imp_from_pub_slots_Schema, self.task_name)

            try:
                for k, v in imp_from_pub_slots_Schema.items():
                    self.x = QtWidgets.QTreeWidgetItem([k])
                    # self.go_to_btn = QtWidgets.QPushButton('go to')
                    item.addChild(self.x)

                    if self.x.text(0) in slot_used_by:
                        self.x.setCheckState(0, QtCore.Qt.Checked)
                    else:
                        self.x.setCheckState(0, QtCore.Qt.Unchecked)

                    # self.imports_from_wdg.setItemWidget(self.x, 1, self.go_to_btn)
                    # self.go_to_btn.clicked.connect(self.show_curr_item)
                # self.expandAll()
            except:
                pass

    # def show_curr_item(self):
    #     item = self.imports_from_wdg.currentItem()
    #     item_index = self.imports_from_wdg.currentIndex()
    #
    #     if item_index.isValid():
    #         try:
    #             parent = item.parent()
    #             print('Open Menu for {0} >>> Parent >>>> {1}'.format(item.text(0), parent.text(0)))
    #         except:
    #             pass

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
        existing_imports_from = xac.get_task_imports_from(self.show_name,
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
        nnn = self.imports_from_wdg.topLevelItemCount()
        ccc = self.imports_from_wdg.invisibleRootItem()
        for each_item in (range(nnn)):
            sel = ccc.child(each_item)
            list_all.append(sel.text(0))
        return list_all

    def get_all_items(self):
        checked = dict()
        root = self.imports_from_wdg.invisibleRootItem()
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
        root = self.imports_from_wdg.invisibleRootItem()
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
        root = self.imports_from_wdg.invisibleRootItem()
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
        listItems = self.imports_from_wdg.currentItem()
        self.clean_wdg(listItems)
        selected_index = self.imports_from_wdg.indexFromItem(listItems)
        remove_it = selected_index.row()
        self.imports_from_wdg.takeTopLevelItem(remove_it)

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

# ImportsFromWidget -- END

# ListEntryTasks -- START

    def populate_existing_tasks(self):
        self.existing_tasks_lwd.clear()
        all_tasks = self.get_all_tasks()
        if all_tasks == None:
            return []

        else:
            for i in all_tasks:
                QtWidgets.QListWidgetItem(i, self.existing_tasks_lwd)

    def get_all_tasks(self):
        tasks = xac.get_tasks(self.show_name, self.branch_name, self.category_name, self.entry_name)
        if tasks != None:
            return tasks
        else:
            return ["-- no tasks --"]

    def remove_self_task(self):
        get_task = self.task_name
        entries = self.existing_tasks_lwd.findItems(get_task, QtCore.Qt.MatchFixedString)
        for entry in entries:
            indexes = self.existing_tasks_lwd.indexFromItem(entry)
            self.existing_tasks_lwd.takeItem(indexes.row())

# ListEntryTasks -- START

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
            self.add_items_to_list([item.text()])
            print ("{0} item added to schema".format (item.text()))
            self.existing_tasks_lwd.takeItem(self.existing_tasks_lwd.row(item))
            # self.imports_from_wdg.collapseAll()


if __name__ == "__main__":

    db = xcon.server.exchange
    test_position = db.show_name
    test = test_position.find({}, {"_id": 1, "show_name": 1})

    app = QtWidgets.QApplication(sys.argv)
    test_dialog = TasksImportFromCore()
    test_dialog.show_name = 'Test'
    test_dialog.branch_name = 'assets'
    test_dialog.category_name = 'characters'
    test_dialog.entry_name = 'hulkGreen'
    test_dialog.task_name = 'modeling'
    test_dialog.populate_main_widget()
    test_dialog.show()
    sys.exit(app.exec_())