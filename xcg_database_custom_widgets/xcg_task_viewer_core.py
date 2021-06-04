from PySide2 import QtWidgets, QtCore, QtGui
from xcg_data_base import xcg_db_actions as xac
from xcg_ui import xcg_create_task_ui
from xcg_database_custom_widgets.xcg_task_viewer_UI import TaskViewerUI


class TaskViewerCore(TaskViewerUI):
    def __init__(self, show_name='',
                 branch_name='',
                 category_name='',
                 entry_name='',
                 parent=None):
        super(TaskViewerCore, self).__init__(parent)

        self.show_name = show_name
        self.branch_name = branch_name
        self.category_name = category_name
        self.entry_name = entry_name

        self.create_tasks_actions()
        self.create_connections()
        self.populate_tasks()
        self.context_menu()

    def create_connections(self):
        self.create_task_action.triggered.connect(self.create_task_menu)

    def populate_tasks(self):
        self.task_viewer_wdg.clear()
        self.task_viewer_wdg.addItems(self.get_tasks())

    def get_tasks(self):
        spare_it = []
        tasks_list = xac.get_tasks(self.show_name, self.branch_name, self.category_name, self.entry_name)

        if tasks_list == None:
            return spare_it
        else:
            try:
                if len(tasks_list) == 0:
                    return spare_it
                elif len(tasks_list) >= 1:
                    return sorted(tasks_list)
            except:
                pass

    def get_selected_task(self):
        names = []
        get_selected_objects = self.task_viewer_wdg.selectedItems()
        if len(get_selected_objects) == 0:
            return None
        elif len(get_selected_objects) >= 1:
            for item in get_selected_objects:
                names.append(item.text())
            return names[0]

    def get_task_list_current_selected(self):
        get_selected_task = self.task_viewer_wdg.selectedItems()
        for i in get_selected_task:
            return i.text()

    #context Menu for the task viewer
    def create_tasks_actions(self):
        self.create_task_action = QtWidgets.QAction("Add Task...", self)
        self.omit_task_action = QtWidgets.QAction("Omit...", self)
        self.split_task_action = QtWidgets.QAction("Split...", self)
        self.add_user_to_task_action = QtWidgets.QAction("User Assign...", self)

    def context_menu(self):
        self.task_viewer_wdg.customContextMenuRequested.connect(self.tasks_con_menu)

    def tasks_con_menu(self, point):
        selected = self.get_selected_task()
        tasks_context_menu = QtWidgets.QMenu()

        if selected == None:
            tasks_context_menu.addAction(self.create_task_action)
            tasks_context_menu.exec_(self.mapToGlobal(point))

        elif selected:
            tasks_context_menu.addAction(self.create_task_action)
            tasks_context_menu.addAction(self.omit_task_action)
            tasks_context_menu.addAction(self.split_task_action)
            tasks_context_menu.addAction(self.add_user_to_task_action)
            tasks_context_menu.exec_(self.mapToGlobal(point))

    def create_task_menu(self):
        self.window = QtWidgets.QMainWindow()
        self.ui = xcg_create_task_ui.CreateTaskUI()

        shows_index = self.ui.show_name_cb.findText(self.show_name, QtCore.Qt.MatchFixedString)
        if shows_index >= 0:
            self.ui.show_name_cb.setCurrentIndex(shows_index)

        self.ui.show_branch_cb.addItems(self.ui.get_show_branches())
        show_branches = self.ui.show_branch_cb.findText(self.branch_name, QtCore.Qt.MatchFixedString)
        if show_branches >= 0:
            self.ui.show_branch_cb.setCurrentIndex(show_branches)

        self.ui.category_cb.addItems(self.ui.get_categories())
        categories = self.ui.category_cb.findText(self.category_name, QtCore.Qt.MatchFixedString)
        if categories >= 0:
            self.ui.category_cb.setCurrentIndex(categories)

        self.ui.entry_name_cb.addItems(self.ui.get_entries())
        entries = self.ui.entry_name_cb.findText(self.entry_name, QtCore.Qt.MatchFixedString)
        if entries >= 0:
            self.ui.entry_name_cb.setCurrentIndex(entries)

        self.ui.populate_existing_tasks()

        self.ui.create_btn.clicked.connect(self.populate_tasks)
        self.ui.create_and_close_btn.clicked.connect(self.populate_tasks)

        self.ui.show_name_cb.setDisabled(True)
        self.ui.show_branch_cb.setDisabled(True)
        self.ui.category_cb.setDisabled(True)
        self.ui.entry_name_cb.setDisabled(True)

        self.ui.show()


if __name__ == '__main__':
    import sys

    app = QtWidgets.QApplication(sys.argv)
    font = app.instance().setFont(QtGui.QFont())

    test_dialog = TaskViewerCore('Test', 'assets', 'characters', 'hulkGreen')
    test_dialog.populate_tasks()

    test_dialog.show()
    sys.exit(app.exec_())