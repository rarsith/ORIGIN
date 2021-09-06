from PySide2 import QtWidgets, QtCore, QtGui
from origin_data_base import xcg_db_actions as xac
from origin_ui import create_task_ui
from origin_database_custom_widgets.xcg_task_viewer_UI import TaskViewerUI


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
        self.add_btn.clicked.connect(self.add_to_task_list)


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

    def insert_task_row(self, name):
        self.task_viewer_wdg.insertItem(0, name)
        xac.create_task(self.show_name,
                        self.branch_name,
                        self.category_name,
                        self.entry_name,
                        self.add_task_le.text())

    def add_to_task_list(self):
        if self.add_task_le.text()and self.entry_name:
            self.insert_task_row(self.add_task_le.text())
            self.add_task_le.clear()
            self.populate_tasks()

        else:
            return

    #context Menu for the task viewer
    def create_tasks_actions(self):
        self.omit_task_action = QtWidgets.QAction("Omit and Hide...", self)
        self.show_hide_omitted_action = QtWidgets.QAction("Show/Hide Omitted...", self)
        self.split_task_action = QtWidgets.QAction("Split...", self)
        self.add_user_to_task_action = QtWidgets.QAction("User Assign...", self)

    def context_menu(self):
        self.task_viewer_wdg.customContextMenuRequested.connect(self.tasks_con_menu)

    def tasks_con_menu(self, point):
        selected = self.get_selected_task()
        tasks_context_menu = QtWidgets.QMenu()

        if selected:
            tasks_context_menu.addAction(self.omit_task_action)
            tasks_context_menu.addAction(self.show_hide_omitted_action)
            tasks_context_menu.addAction(self.split_task_action)
            tasks_context_menu.addAction(self.add_user_to_task_action)
            tasks_context_menu.exec_(self.mapToGlobal(point))


if __name__ == '__main__':
    import sys

    app = QtWidgets.QApplication(sys.argv)
    font = app.instance().setFont(QtGui.QFont())

    test_dialog = TaskViewerCore('Test', 'assets', 'characters', 'hulkGreen')
    test_dialog.populate_tasks()

    test_dialog.show()
    sys.exit(app.exec_())