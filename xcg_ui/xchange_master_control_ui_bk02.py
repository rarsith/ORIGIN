import sys
from PySide2 import QtWidgets, QtCore, QtGui
from xcg_data_base import xcg_db_connection as xcon
from xcg_data_base import xcg_db_helpers as xhlp
from xcg_data_base import xcg_db_actions as xac
from xcg_config import xcg_validation as xval
from xcg_config import xcg_slot_methods as xslop
from xcg_utilities import xcg_utils as xutil
from xcg_ui import xcg_create_show_ui
from xcg_ui import xcg_create_seq_ui
from xcg_ui import xcg_create_asset_ui
from xcg_ui import xcg_create_shot_ui
from xcg_ui import xcg_create_asset_category_ui
from xcg_ui import xcg_create_show_category_ui
from xcg_ui import xcg_create_task_ui
from xcg_ui import xcg_edit_task_pub_slot_ui
from xcg_ui import xcg_edit_task_imports_from_ui
from xcg_ui import xcg_edit_entry_definition_ui
from xcg_database_custom_widgets.xcg_task_imports_from_core import TasksImportFromCore
from xcg_database_custom_widgets.xcg_task_publishing_slots_core import PublishSlotsWidgetCore



db = xcon.server.exchange
test_position = db.show_name
test = test_position.find({}, {"_id":1, "show_name":1})


class ProjectTreeViewWidget(QtWidgets.QTreeWidget):
    def __init__(self, parent=None):
        super(ProjectTreeViewWidget, self).__init__(parent)

        self.widget_build()

    def widget_build(self):
        self.setMinimumWidth(180)
        self.setMaximumWidth(190)
        self.setHeaderHidden(True)

        self.expandAll()
        self.setSelectionMode(QtWidgets.QListWidget.ExtendedSelection)
        self.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)


class TasksViewWidget(QtWidgets.QListWidget):
    def __init__(self, parent=None):
        super(TasksViewWidget, self).__init__(parent)

        self.widget_build()

    def widget_build(self):
        self.setMinimumWidth(150)
        self.setMaximumWidth(160)
        self.setSelectionMode(QtWidgets.QListWidget.ExtendedSelection)
        self.sortItems(QtCore.Qt.AscendingOrder)
        self.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)


class BundleViewListWidget(QtWidgets.QListWidget):
    def __init__(self, parent=None):
        super(BundleViewListWidget, self).__init__(parent)

        self.widget_build()

    def widget_build(self):
        self.sortItems(QtCore.Qt.AscendingOrder)
        self.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)


class PublishesViewWidget(QtWidgets.QTableWidget):
    def __init__(self, parent=None):
        super(PublishesViewWidget, self).__init__(parent)

        self.widget_build()

    def widget_build(self):
        self.setColumnCount(10)
        self.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.setRowCount(50)
        self.setColumnWidth(0, 30)
        self.setColumnWidth(1, 60)
        self.setColumnWidth(2, 120)
        self.setColumnWidth(3, 50)
        self.setColumnWidth(7, 50)
        self.setColumnWidth(8, 80)
        self.setColumnWidth(9, 119)
        for row in range(self.rowCount()):
            self.setRowHeight(row, 10)

        self.setAlternatingRowColors(True)
        self.setMinimumWidth(850)
        self.setHorizontalHeaderLabels(['...', '',
                                        'publish_name',
                                        'version',
                                        'task',
                                        'published_by',
                                        'published',
                                        'bundle',
                                        'status',
                                        'user notes'])


class BundleViewWidget(QtWidgets.QTableWidget):
    def __init__(self, parent=None):
        super(BundleViewWidget, self).__init__(parent)

        self.widget_build()

    def widget_build(self):

        self.setColumnCount(9)
        self.setRowCount(50)
        self.setColumnWidth(0, 30)
        self.setColumnWidth(1, 60)
        for row in range(self.rowCount()):
            self.setRowHeight(row, 20)
        self.setAlternatingRowColors(True)
        self.setMinimumWidth(850)
        self.setHorizontalHeaderLabels(['', '',
                                        'task01',
                                        'task02',
                                        'task03',
                                        'task04',
                                        'task05',
                                        'task06',
                                        'task07'])


class PropertiesViewWidget(QtWidgets.QTableWidget):
    def __init__(self, parent=None):
        super(PropertiesViewWidget, self).__init__(parent)

        self.widget_build()

    def widget_build(self):
        self.setColumnCount(2)
        # self.setColumnWidth(0, 250)
        # self.setColumnWidth(1, 120)
        # self.setMaximumHeight(410)

        self.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        # self.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.verticalScrollBar().setVisible(False)
        self.horizontalScrollBar().setVisible(False)

        self.setShowGrid(False)
        vertical_header = self.verticalHeader()

        for row in range(self.rowCount()):
            self.setRowHeight(row, 10)

        self.setAlternatingRowColors(True)

        header = self.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)

        vertical_header.setDefaultSectionSize(2)
        vertical_header.hide()
        horizontal_header = self.horizontalHeader()
        horizontal_header.setMinimumHeight(2)
        horizontal_header.setMaximumHeight(3)
        horizontal_header.hide()


    def create_properties(self, properties):
        try:
            self.setRowCount(0)
            store_attributes_names = (list(properties.keys()))
            write_attrib_nice = xutil.write_nice_names(store_attributes_names)

            for i in range(len(properties)):
                get_properties_names = write_attrib_nice[i]
                get_properties_values = list(properties.values())[i]
                self.insertRow(i)
                self.insert_item(i, 0, str(get_properties_names))
                self.insert_item(i, 1, str(get_properties_values))
        except:
            pass

    def insert_item(self, row, column, text):
        item = QtWidgets.QTableWidgetItem(text)
        self.setItem(row, column, item)


class ContentViewWidget(QtWidgets.QTableWidget):
    def __init__(self, parent=None):
        super(ContentViewWidget, self).__init__(parent)

        self.widget_build()

    def widget_build(self):
        self.setMaximumWidth(437)
        self.setColumnCount(4)
        self.setHorizontalHeaderLabels(["Asset Name", "Category", "status", "health"])
        self.setShowGrid(True)
        self.setRowCount(20)
        self.setAlternatingRowColors(True)
        # header = self.shot_content_twd.verticalHeader()
        # header.hide()
        self.setColumnWidth(0, 135)
        self.setColumnWidth(1, 135)
        self.setColumnWidth(2, 80)
        self.setColumnWidth(3, 67)
        for row in range(self.rowCount()):
            self.setRowHeight(row, 5)


class ButtonsWidget(QtWidgets.QWidget):

    def __init__(self, parent=None):
        super(ButtonsWidget, self).__init__(parent)

        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(QtWidgets.QPushButton("Button 01"))
        layout.addWidget(QtWidgets.QPushButton("Button 02"))
        layout.addWidget(QtWidgets.QPushButton("Button 03"))
        layout.addWidget(QtWidgets.QPushButton("Button 04"))


class OthersWidget(QtWidgets.QWidget):

    def __init__(self, parent=None):
        super(OthersWidget, self).__init__(parent)

        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(QtWidgets.QLabel("Label"))
        layout.addWidget(QtWidgets.QPushButton("Button"))
        layout.addWidget(QtWidgets.QCheckBox("Check Box"))
        layout.addWidget(QtWidgets.QLineEdit())


class XchangeControlCenterUI(QtWidgets.QWidget):

    WINDOW_TITLE = "Xchange_Control_Center"
    db = xcon.server.xchange
    cursor = db.show_name

    def __init__(self):
        super(XchangeControlCenterUI,self).__init__()

        self.setWindowTitle(self.WINDOW_TITLE)

        self.setMinimumHeight(700)
        self.setMinimumWidth(1900)

        self.create_show_actions()
        self.create_tasks_actions()

        self.create_widgets()

        self.create_layout()
        self.create_connections()
        self.task_properties_UI()
        self.shot_definition_UI()
        self.asset_definition_UI()

        self.refresh_tree_widget()

    def create_show_actions(self):
        self.about_action = QtWidgets.QAction("About", self)
        self.create_show_action = QtWidgets.QAction("Create Show...", self)
        self.create_show_branch_action = QtWidgets.QAction("Create Show Branch...", self)
        self.create_seq_action = QtWidgets.QAction("Create Seq...", self)
        self.create_shot_action = QtWidgets.QAction("Create Shot...", self)
        self.create_asset_action = QtWidgets.QAction("Create Asset...", self)
        self.create_asset_category_action = QtWidgets.QAction("Create Asset Category...", self)
        self.remove_entry_action = QtWidgets.QAction("Remove Entry...", self)

    def create_tasks_actions(self):
        self.about_action = QtWidgets.QAction("About", self)

        self.edit_entry_definition = QtWidgets.QAction("Edit Definition...", self)
        self.edit_bundle = QtWidgets.QAction("Edit Bundle...", self)
        self.create_task_action = QtWidgets.QAction("Add Task...", self)
        self.save_task_schema_action = QtWidgets.QAction("Save Task Schema...", self)
        self.omit_task_action = QtWidgets.QAction("Omit...", self)
        self.split_task_action = QtWidgets.QAction("Split...", self)
        self.add_user_to_task_action = QtWidgets.QAction("User Assign...", self)
        self.add_pub_slot_action = QtWidgets.QAction("Publish Slot...", self)
        self.set_task_imports_action = QtWidgets.QAction("Imports From...", self)

    def create_widgets(self):
        self.menu_bar = QtWidgets.QMenuBar()
        self.shows_lb = QtWidgets.QLabel("Select Show")
        self.show_settings_btn = QtWidgets.QPushButton("Show Settings")
        self.show_name_cb = QtWidgets.QComboBox()
        self.show_name_cb.addItems(self.get_shows())

        self.show_view_twd = ProjectTreeViewWidget()
        self.show_view_twd.customContextMenuRequested.connect(self.show_tree_con_menu)
        # ----------------------------------------------
        self.tasks_view_lwd = TasksViewWidget()
        self.tasks_view_lwd.customContextMenuRequested.connect(self.tasks_con_menu)

        self.empty_stack = QtWidgets.QWidget()
        self.entry_task_properties_stack = QtWidgets.QWidget()
        self.shots_definition_properties_stack = QtWidgets.QWidget()
        self.assets_definition_properties_stack = QtWidgets.QWidget()


        self.shot_bundle_view_lwd = BundleViewListWidget()
        self.shot_bundle_edit_btn = QtWidgets.QPushButton('Edit Bundle')
        self.asset_bundle_view_lwd = BundleViewListWidget()
        self.asset_bundle_edit_btn = QtWidgets.QPushButton('Edit Bundle')

        # ----------------------------------------------
        self.versions_view_tvw = PublishesViewWidget()
        self.bundle_view_tvw = BundleViewWidget()
        self.graph_view_lw = QtWidgets.QListWidget()

        self.stacked_properties_wdg = QtWidgets.QStackedWidget()
        self.stacked_properties_wdg.addWidget(self.empty_stack)
        self.stacked_properties_wdg.addWidget(self.entry_task_properties_stack)
        self.stacked_properties_wdg.addWidget(self.shots_definition_properties_stack)
        self.stacked_properties_wdg.addWidget(self.assets_definition_properties_stack)


        self.middle_tabmenu_tab = QtWidgets.QTabWidget()
        self.middle_tabmenu_tab.addTab(self.stacked_properties_wdg, "Properties")
        self.middle_tabmenu_tab.addTab(self.versions_view_tvw, "Publishes")
        self.middle_tabmenu_tab.addTab(self.bundle_view_tvw, "Bundle View")
        self.middle_tabmenu_tab.addTab(self.graph_view_lw, "Graph View")

        self.properties_wdg = PropertiesViewWidget()
        self.asset_properties_wdg = PropertiesViewWidget()

        # StackWidget for Entry Tasks Properties


        self.task_is_active_properties_ckb = QtWidgets.QCheckBox()
        self.task_status_properties_cb = QtWidgets.QComboBox()
        self.task_status_properties_cb.addItems(xval.VALID_TASK_STATUSES)

        self.task_edit_user_properties_btn = QtWidgets.QPushButton("Edit")
        self.tasks_pub_slots_edit_properties_btn = QtWidgets.QPushButton("Edit")
        self.task_user_properties_wdg = QtWidgets.QLineEdit()

        # Create the individual Widgets that will be part of the Layout

        self.tasks_imports_from_properties_wdg = TasksImportFromCore()
        self.tasks_imports_from_edit_properties_btn = QtWidgets.QPushButton("Edit")
        self.tasks_imports_from_commit_btn = QtWidgets.QPushButton('Commit')


        self.tasks_pub_slots_properties_wdg = PublishSlotsWidgetCore()

        # StackWidget for Asset definition
        # Create the individual Widgets that will be part of the Layout
        self.asset_lod_le = QtWidgets.QLabel()
        self.asset_assembly_chk = QtWidgets.QCheckBox()
        self.asset_assembly_chk.setDisabled(True)
        self.asset_edit_definition_btn = QtWidgets.QPushButton("Edit")

        # StackWidget for Shot definition

        # Create the individual Widgets that will be part of the Layout

        self.shot_edit_definitions_btn = QtWidgets.QPushButton("Edit")

        # widgets for Shot Content----START
        self.shot_content_lb = QtWidgets.QLabel("Content")
        self.shot_content_twd = ContentViewWidget()

        # widgets for Shot Content----END


        # Construct the Links Tab
        self.links_wdg = ButtonsWidget()

        # Construct the Notes Tab
        self.notes_wdg = OthersWidget()

        # Assembling the Right Side Tab Menu
        self.details_tabmenu_tab = QtWidgets.QTabWidget()
        self.details_tabmenu_tab.setTabPosition(QtWidgets.QTabWidget.North)
        # self.details_tabmenu_tab.addTab(self.stacked_properties_wdg, "Properties")
        # self.details_tabmenu_tab.addTab(self.properties_wdg, "Content")
        self.details_tabmenu_tab.addTab(self.links_wdg, "Links")
        self.details_tabmenu_tab.addTab(self.notes_wdg, "Notes")

        self.all_tab = QtWidgets.QTabWidget()
        self.all_tab.setTabPosition(QtWidgets.QTabWidget.West)

        self.refresh_btn = QtWidgets.QPushButton("Refresh")

    def create_layout(self):
        shows_cb_layout = QtWidgets.QHBoxLayout()
        shows_cb_layout.addWidget(self.shows_lb)
        shows_cb_layout.addWidget(self.show_name_cb)
        shows_cb_layout.addWidget(self.show_settings_btn)
        shows_cb_layout.addStretch()
        shows_cb_layout.addSpacing(100)

        task_bundle_layout = QtWidgets.QVBoxLayout()
        task_bundle_layout.addWidget(self.tasks_view_lwd)


        views_layout = QtWidgets.QHBoxLayout()
        views_layout.addWidget(self.show_view_twd)
        views_layout.addLayout(task_bundle_layout)
        views_layout.addWidget(self.middle_tabmenu_tab)
        views_layout.addWidget(self.details_tabmenu_tab)

        button_layout = QtWidgets.QVBoxLayout()
        button_layout.addWidget(self.refresh_btn)

        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.addLayout(shows_cb_layout)
        main_layout.addLayout(views_layout)
        main_layout.setContentsMargins(2, 2, 2, 2)
        main_layout.setSpacing(2)
        main_layout.addLayout(button_layout)

    def create_connections(self):
        self.about_action.triggered.connect(self.about)
        self.create_show_action.triggered.connect(self.create_show_menu)
        self.create_show_branch_action.triggered.connect(self.create_show_branches_menu)

        self.create_seq_action.triggered.connect(self.create_seq_menu)
        self.create_shot_action.triggered.connect(self.create_shot_menu)
        self.create_asset_action.triggered.connect(self.create_asset_menu)
        self.create_asset_category_action.triggered.connect(self.create_asset_category_menu)
        self.create_task_action.triggered.connect(self.create_task_menu)
        self.add_pub_slot_action.triggered.connect(self.create_task_pub_slot_menu)
        self.set_task_imports_action.triggered.connect(self.create_task_imports_from_menu)
        self.remove_entry_action.triggered.connect(self.remove_entry_menu)

        self.show_name_cb.currentIndexChanged.connect(self.comboBox_shows)
        self.show_name_cb.currentIndexChanged.connect(self.refresh_tree_widget)

        self.show_view_twd.itemClicked.connect(self.get_tasks)
        self.show_view_twd.itemClicked.connect(self.get_selected_entry_name)
        self.show_view_twd.itemClicked.connect(self.update_tasks_list)
        self.show_view_twd.itemClicked.connect(self.get_sel_show_branch_category)
        self.show_view_twd.itemClicked.connect(self.update_entry_properties_list)
        self.show_view_twd.itemClicked.connect(self.get_selected_type)
        self.show_view_twd.itemClicked.connect(self.switch_stack)

        self.tasks_view_lwd.itemSelectionChanged.connect(self.populate_task_import_schema)
        self.tasks_view_lwd.itemSelectionChanged.connect(self.populate_task_details)
        self.tasks_view_lwd.itemSelectionChanged.connect(self.populate_pub_slots)
        self.tasks_view_lwd.itemSelectionChanged.connect(self.get_selected_type)
        self.tasks_view_lwd.itemSelectionChanged.connect(self.switch_stack)

       # self.task_status_properties_cb.textActivated.connect(self.set_task_status)
        self.task_is_active_properties_ckb.clicked.connect(self.set_task_is_active)
        self.task_is_active_properties_ckb.clicked.connect(self.populate_task_details)

        # self.tasks_pub_slots_edit_properties_btn.clicked.connect(self.create_task_pub_slot_menu)
        # self.tasks_imports_from_edit_properties_btn.clicked.connect(self.create_task_imports_from_menu)
        # self.tasks_imports_from_commit_btn.clicked.connect(self.tasks_imports_from_properties_wdg.save_to_database)
        # self.tasks_imports_from_commit_btn.clicked.connect(self.tasks_imports_from_properties_wdg.populate_task_import_schema)

        self.shot_edit_definitions_btn.clicked.connect(self.create_entry_definition_menu)
        self.asset_edit_definition_btn.clicked.connect(self.create_entry_definition_menu)

        self.refresh_btn.clicked.connect(self.refresh_shows)
        self.refresh_btn.clicked.connect(self.refresh_tree_widget)

    def get_shows(self):
        get_versions = xac.get_all_active_shows()
        return get_versions

    def get_show_structure(self):
        try:
            entity = xac.get_show_base_structure(self.show_name_cb.currentText())
            return entity
        except:
            pass

    def refresh_shows(self):
        store = []
        current_selected_show = self.comboBox_shows()
        get_versions = xac.get_all_active_shows()
        for show in get_versions:
            store.append(show)

        self.show_name_cb.clear()
        self.show_name_cb.addItems(store)
        self.show_name_cb.setCurrentText(current_selected_show)
        return store

    def comboBox_shows(self):
        text = self.show_name_cb.currentText()
        return text

    def refresh_tree_widget(self):
        try:
            self.show_view_twd.clear()
            get_entity = self.get_show_structure()
            get_categories = xhlp.get_entity_root_structure(get_entity)
            for category in get_categories:
                item = self.show_tree_create_item(category)
                self.show_view_twd.addTopLevelItem(item)
            self.show_view_twd.expandAll()
        except:
            pass

    def show_tree_create_item(self, name):
        item = QtWidgets.QTreeWidgetItem([name])
        self.add_children(item)
        return item

    def add_children(self, item):
        get_children = xhlp.deep_values(item.text(0), self.get_show_structure())
        for children in get_children:
            for child in children:
                child_item = self.show_tree_create_item(child)
                item.addChild(child_item)

    def get_selected_entry_name(self):
        names = []
        get_selected_objects = self.show_view_twd.selectedItems()
        if len(get_selected_objects) == 0:
            return []
        elif len(get_selected_objects) >= 1:
            for item in get_selected_objects:
                names.append(item.text(0))
            return names[0]

    def get_selected_entry(self):
        names = []
        get_selected_objects = self.show_view_twd.selectedItems()
        if len(get_selected_objects) == 0:
            return []
        elif len(get_selected_objects) >= 1:
            for item in get_selected_objects:
                names.append(item.text(0))
            return names[0]

    def get_selected_type(self):
        entry_selected = self.show_view_twd.hasFocus()
        task_selected = self.tasks_view_lwd.hasFocus()
        if entry_selected:
            get_selected_objects_type = xac.get_entry_type(self.show_name_cb.currentText(),
                                                           self.get_sel_show_branch(),
                                                           self.get_sel_category(),
                                                           self.get_selected_entry_name())
            return get_selected_objects_type

        elif task_selected:
            task_type = self.get_task_type()
            return task_type

    def get_selected_task(self):
        names = []
        get_selected_objects = self.tasks_view_lwd.selectedItems()
        if len(get_selected_objects) == 0:
            return None
        elif len(get_selected_objects) >= 1:
            for item in get_selected_objects:
                names.append(item.text())
            return names[0]

    def get_task_type(self):
        task_name = self.get_selected_task()
        if task_name:
            task_type = "task"
            return task_type

    def set_task_status(self):
        read_selected_status = self.task_status_properties_cb.currentText()
        try:
            xac.update_task_status(self.show_name_cb.currentText(),
                                              self.get_sel_show_branch(),
                                              self.get_sel_category(),
                                              self.get_selected_entry_name(),
                                              self.get_selected_task(),
                                                 read_selected_status)

        except:
            pass
        print ('{} status changed to {}'.format(self.get_selected_task(), read_selected_status))

    def set_task_is_active(self):
        is_active = self.task_is_active_properties_ckb.isChecked()
        try:
            xac.update_task_is_active(self.show_name_cb.currentText(),
                                      self.get_sel_show_branch(),
                                      self.get_sel_category(),
                                      self.get_selected_entry_name(),
                                      self.get_selected_task(),
                                      is_active)

            self.populate_task_details()

        except:
            pass
        print ('{} status changed to {}'.format(self.get_selected_task(), is_active))

    def get_task_status(self):
        try:
            task_status = xac.get_task_status(self.show_name_cb.currentText(),
                                              self.get_sel_show_branch(),
                                              self.get_sel_category(),
                                              self.get_selected_entry_name(),
                                              self.get_selected_task())
            return task_status[0]
        except:
            pass

    def get_task_is_active(self):
        try:
            task_is_active = xac.get_task_is_active(self.show_name_cb.currentText(),
                                              self.get_sel_show_branch(),
                                              self.get_sel_category(),
                                              self.get_selected_entry_name(),
                                              self.get_selected_task())
            return task_is_active[0]
        except:
            pass

    def get_sel_show_branch_category(self):
        get_selected_objects = self.show_view_twd.selectedItems()
        if len(get_selected_objects) == 0:
            return []
        elif len(get_selected_objects) >= 1:
            for item in get_selected_objects:
                try:
                    parent = item.parent()
                    grand_parent = parent.parent()
                    return grand_parent.text(0)
                except:
                    pass

    def get_sel_show_branch(self):
        get_selected_objects = self.show_view_twd.selectedItems()
        if len(get_selected_objects) == 0:
            return
        elif len(get_selected_objects) >= 1:
            for item in get_selected_objects:
                try:
                    parent = item.parent()
                    grand_parent = parent.parent()
                    return grand_parent.text(0)
                except:
                    pass

    def get_sel_category(self):
        get_selected_objects = self.show_view_twd.selectedItems()

        if len(get_selected_objects) == 0:
            return []
        elif len(get_selected_objects) >= 1:
            for item in get_selected_objects:
                try:
                    parent = item.parent()
                    return parent.text(0)
                except:
                    pass

    def get_sel_entry_path(self):
        get_selected_entry_objects = self.show_view_twd.selectedItems()

        if len(get_selected_entry_objects) == 0:
            return []
        elif len(get_selected_entry_objects) >= 1:
            for item in get_selected_entry_objects:
                try:
                    parent = item.parent()
                    return parent.text(0)
                except:
                    pass

    def get_sel_task_path(self):
        get_selected_task_objects = self.tasks_view_lwd.selectedItems()
        if len(get_selected_task_objects) == 0:
            return
        elif len(get_selected_task_objects) >= 1:
            for item in get_selected_task_objects:
                try:
                    parent = item.parent()
                    return parent.text(0)
                except:
                    pass

    def update_tasks_list(self):
        self.tasks_view_lwd.clear()
        self.tasks_view_lwd.addItems(self.get_tasks())

    def populate_task_import_schema(self):
        self.tasks_imports_from_properties_wdg.show_name = (self.show_name_cb.currentText())
        self.tasks_imports_from_properties_wdg.branch_name = (self.get_sel_show_branch())
        self.tasks_imports_from_properties_wdg.category_name = (self.get_sel_category())
        self.tasks_imports_from_properties_wdg.entry_name = (self.get_selected_entry_name())
        self.tasks_imports_from_properties_wdg.task_name = (self.get_selected_task())

        self.tasks_imports_from_properties_wdg.populate_task_import_schema()
        self.tasks_imports_from_properties_wdg.populate_main_widget()
        self.tasks_imports_from_properties_wdg.remove_self_task()
        self.tasks_imports_from_properties_wdg.remove_already_assigned()

    def get_tasks(self):
        spare_it = []
        db_connection = self.get_sel_show_branch_category()
        tasks_list = xac.get_tasks(self.show_name_cb.currentText(),
                                   db_connection,
                                   self.get_sel_category(),
                                   self.get_selected_entry_name())
        if tasks_list == None:
            return spare_it
        else:
            try:
                if len(tasks_list) == 0:
                    return spare_it
                elif len(tasks_list) >= 1:
                    return tasks_list
            except:
                pass

    def update_entry_properties_list(self):
        properties = self.get_entry_properties()
        self.properties_wdg.create_properties(properties)
        self.asset_properties_wdg.create_properties(properties)

    def get_saved_import_schema(self):
        existing_imports_from = xac.get_task_imports_from (self.show_name_cb.currentText(),
                                                           self.get_sel_show_branch(),
                                                           self.get_sel_category(),
                                                           self.get_selected_entry_name(),
                                                           self.get_selected_task())
        if existing_imports_from == None:
            return []
        else:
            return existing_imports_from

    def get_entry_properties(self):
        spare_it = []
        db_connection = self.get_sel_show_branch_category()
        definitions_list = xac.get_entry_definition(self.show_name_cb.currentText(),
                                                    db_connection,
                                                    self.get_sel_category(),
                                                    self.get_selected_entry_name())
        if definitions_list == None:
            return spare_it
        else:
            try:
                if len(definitions_list) == 0:
                    return spare_it
                elif len(definitions_list) >= 1:
                    return definitions_list
            except:
                pass

    def get_definition_value(self, def_item):
        definition = xac.get_definition_element(self.show_name_cb.currentText(),
                                                self.get_sel_show_branch(),
                                                self.get_sel_category(),
                                                self.get_selected_entry_name(),
                                                def_item)
        return definition

    def get_task_list_current_selected(self):
        get_selected_task = self.tasks_view_lwd.selectedItems()
        for i in get_selected_task:
            return i.text()

    def get_task_properties(self):
        spare_it = []
        db_connection = self.get_sel_show_branch_category()
        definitions_list = xac.get_task_definition(self.show_name_cb.currentText(),
                                                   db_connection,
                                                   self.get_sel_category(),
                                                   self.get_selected_entry_name(),
                                                   self.get_task_list_current_selected())
        if definitions_list == None:
            return spare_it
        else:
            try:
                if len(definitions_list) == 0:
                    return spare_it
                elif len(definitions_list) >= 1:
                    return definitions_list
            except:
                pass

    def populate_task_details(self):
        task_status = self.get_task_status()
        task_is_active = self.get_task_is_active()
        if task_status or task_is_active != None:
            self.task_status_properties_cb.setCurrentText(task_status)
            self.task_is_active_properties_ckb.setChecked(task_is_active)

    def get_pub_imports(self, import_tasks):
        pub_imports =  xac.get_pub_slots(self.show_name_cb.currentText(),
                                              self.get_sel_show_branch(),
                                              self.get_sel_category(),
                                              self.get_selected_entry_name(),
                                              import_tasks)

        return pub_imports

    def populate_pub_slots(self):

        self.tasks_pub_slots_properties_wdg.show_name = self.show_name_cb.currentText()
        self.tasks_pub_slots_properties_wdg.branch_name = self.get_sel_show_branch()
        self.tasks_pub_slots_properties_wdg.category_name = self.get_sel_category()
        self.tasks_pub_slots_properties_wdg.entry_name = self.get_selected_entry_name()
        self.tasks_pub_slots_properties_wdg.task_name = self.get_selected_task()
        self.tasks_pub_slots_properties_wdg.populate_main_widget()

    def task_properties_UI(self):
        task_user_btn_layout = QtWidgets.QHBoxLayout()
        task_user_btn_layout.addWidget(self.task_user_properties_wdg)
        task_user_btn_layout.addWidget(self.task_edit_user_properties_btn)

        top_data_form = QtWidgets.QFormLayout()
        top_data_form.addRow("Active", self.task_is_active_properties_ckb)
        top_data_form.addRow("Status", self.task_status_properties_cb)
        top_data_form.addRow("User", task_user_btn_layout)
        top_data_form.setFormAlignment(QtCore.Qt.AlignLeft)
        top_data_form.setLabelAlignment(QtCore.Qt.AlignLeft)
        top_data_form.setSpacing(5)

        top_data_layout = QtWidgets.QVBoxLayout()
        top_data_layout.addLayout(top_data_form)


        imports_from_layout = QtWidgets.QVBoxLayout()
        imports_from_layout.addWidget(self.tasks_imports_from_properties_wdg)

        imports_from_layout.setSpacing(5)

        publishing_slots_layout = QtWidgets.QVBoxLayout()
        publishing_slots_layout.addWidget(self.tasks_pub_slots_properties_wdg)
        publishing_slots_layout.setSpacing(5)

        lists_layout = QtWidgets.QHBoxLayout()
        lists_layout.addLayout(imports_from_layout)
        lists_layout.addLayout(publishing_slots_layout)
        lists_layout.setAlignment(QtCore.Qt.AlignLeft)

        main_layout = QtWidgets.QVBoxLayout()
        main_layout.addLayout(top_data_layout)
        main_layout.addLayout(lists_layout)


        self.entry_task_properties_stack.setLayout(main_layout)

    def asset_definition_UI(self):

        bundle_layout = QtWidgets.QVBoxLayout()
        bundle_layout.addWidget(self.asset_bundle_view_lwd)
        bundle_layout.addWidget(self.asset_bundle_edit_btn)

        asset_def_new = QtWidgets.QVBoxLayout()
        asset_def_new.addWidget(self.asset_properties_wdg)
        asset_def_new.addWidget(self.asset_edit_definition_btn)

        shot_content_layout = QtWidgets.QVBoxLayout()
        shot_content_layout.addWidget(self.shot_content_lb)
        shot_content_layout.addWidget(self.shot_content_twd)

        main_layout = QtWidgets.QHBoxLayout()
        main_layout.addLayout(asset_def_new)
        main_layout.addLayout(bundle_layout)


        self.assets_definition_properties_stack.setLayout(main_layout)

    def shot_definition_UI(self):


        bundle_layout = QtWidgets.QVBoxLayout()
        bundle_layout.addWidget(self.shot_bundle_view_lwd)
        bundle_layout.addWidget(self.shot_bundle_edit_btn)

        shot_def_new = QtWidgets.QVBoxLayout()
        shot_def_new.addWidget(self.properties_wdg)
        shot_def_new.addWidget(self.shot_edit_definitions_btn)

        shot_content_layout = QtWidgets.QVBoxLayout()
        shot_content_layout.addWidget(self.shot_content_lb)
        shot_content_layout.addWidget(self.shot_content_twd)

        main_layout = QtWidgets.QHBoxLayout()
        main_layout.addLayout(shot_def_new)
        main_layout.addLayout(bundle_layout)

        self.shots_definition_properties_stack.setLayout(main_layout)

    def switch_stack(self):
        switch_index = self.properties_UI_switcher()
        if switch_index:
            self.stacked_properties_wdg.setCurrentIndex(switch_index)
        else:
            self.stacked_properties_wdg.setCurrentIndex(0)

    def properties_UI_switcher(self):
        current_selection_type = self.get_selected_type()

        if current_selection_type == "asset":
            assets_index = self.stacked_properties_wdg.indexOf(self.assets_definition_properties_stack)
            return assets_index

        elif current_selection_type == "shot":
            shots_index = self.stacked_properties_wdg.indexOf(self.shots_definition_properties_stack)
            return shots_index

        elif current_selection_type == "task":
            task_index = self.stacked_properties_wdg.indexOf(self.entry_task_properties_stack)
            return task_index

    #CONTEXT MENU
    def show_tree_con_menu(self, point):
        context_menu = QtWidgets.QMenu()
        context_parent = self.get_sel_entry_path()
        selected = self.get_selected_entry_name()

        if selected == []:
            context_menu.addAction(self.create_show_action)
            context_menu.addAction(self.create_show_branch_action)
            context_menu.exec_(self.mapToGlobal(point))

        elif selected == "sequences":
            context_menu.addAction(self.create_seq_action)
            context_menu.exec_(self.mapToGlobal(point))

        elif context_parent == "sequences":
            context_menu.addAction(self.create_shot_action)
            context_menu.exec_(self.mapToGlobal(point))

        elif context_parent == "assets":
            context_menu.addAction(self.create_asset_action)
            context_menu.exec_(self.mapToGlobal(point))

        elif selected == "assets":
            context_menu.addAction(self.create_asset_category_action)
            context_menu.exec_(self.mapToGlobal(point))

        elif context_parent != "sequences" or context_menu != "assets":
            context_menu.addAction(self.edit_entry_definition)
            context_menu.addAction(self.edit_bundle)
            context_menu.addSeparator()
            context_menu.addAction(self.create_task_action)
            context_menu.addAction(self.save_task_schema_action)

            context_menu.addSeparator()
            context_menu.addAction(self.remove_entry_action)
            context_menu.exec_(self.mapToGlobal(point))

    def tasks_con_menu(self, point):
        selected = self.get_selected_task()
        tasks_context_menu = QtWidgets.QMenu()

        if selected:
            tasks_context_menu.addAction(self.omit_task_action)
            tasks_context_menu.addAction(self.split_task_action)
            tasks_context_menu.addAction(self.add_user_to_task_action)
            tasks_context_menu.addAction(self.add_pub_slot_action)
            tasks_context_menu.addAction(self.set_task_imports_action)
            tasks_context_menu.exec_(self.mapToGlobal(point))

    def about(self):
        QtWidgets.QMessageBox.about(self, "About Simple Stuff", "Add ABout Text Here")

    def remove_entry_menu(self):
        custom_dialog = QtWidgets.QMessageBox()
        custom_dialog.setText("Operation is undoable!")
        custom_dialog.setInformativeText("Do you want to continue?")
        custom_dialog.setStandardButtons(custom_dialog.Yes | custom_dialog.Cancel)
        custom_dialog.setDefaultButton(custom_dialog.Save)
        btn_pressed = custom_dialog.exec_()

        if btn_pressed == custom_dialog.Yes:
            print ("This shit works")
            xac.remove_entry(self.show_name_cb.currentText(),
                             self.get_sel_show_branch(),
                             self.get_sel_category(),
                             self.get_selected_entry_name())
            self.refresh_tree_widget()
        else:
            print ("Just closed the damn window")
            custom_dialog.close()

    def create_show_menu(self):
        self.window = QtWidgets.QMainWindow()
        self.ui = xcg_create_show_ui.CreateShowUI()
        self.ui.show()

    def create_show_branches_menu(self):
        self.window = QtWidgets.QMainWindow()
        self.ui = xcg_create_show_category_ui.CreateShowCategoryUI()
        self.ui.show_name_cb.setDisabled(True)
        self.ui.show()

    def create_seq_menu(self):
        self.window = QtWidgets.QMainWindow()
        self.ui = xcg_create_seq_ui.CreateSeqUI()
        self.ui.show_name_cb.setDisabled(True)
        self.ui.show_name_cb.setCurrentText(self.show_name_cb.currentText())
        self.ui.show()

    def create_shot_menu(self):
        self.window = QtWidgets.QMainWindow()
        self.ui = xcg_create_shot_ui.CreateShotUI()
        self.ui.parent_seq_cb.setCurrentText(self.get_selected_entry_name())

        shows_index = self.ui.show_name_cb.findText(self.show_name_cb.currentText(), QtCore.Qt.MatchFixedString)
        if shows_index >= 0:
            self.ui.show_name_cb.setCurrentIndex(shows_index)
        self.ui.parent_seq_cb.addItems(self.ui.get_shows_seq())

        sequences_index = self.ui.parent_seq_cb.findText(self.get_selected_entry_name(), QtCore.Qt.MatchFixedString)
        if sequences_index >= 0:
            self.ui.parent_seq_cb.setCurrentIndex(sequences_index)

        self.ui.create_btn.clicked.connect(self.refresh_tree_widget)
        self.ui.create_and_close_btn.clicked.connect(self.refresh_tree_widget)

        self.ui.show_name_cb.setDisabled(True)
        self.ui.parent_seq_cb.setDisabled(True)

        self.ui.show()

    def create_asset_menu(self):
        self.window = QtWidgets.QMainWindow()
        self.ui = xcg_create_asset_ui.CreateAssetUI()

        shows_index = self.ui.show_name_cb.findText(self.show_name_cb.currentText(), QtCore.Qt.MatchFixedString)
        if shows_index >= 0:
            self.ui.show_name_cb.setCurrentIndex(shows_index)

        self.ui.category_cb.addItems(self.ui.get_asset_categories())
        assets_cat_index = self.ui.category_cb.findText(self.get_selected_entry_name(), QtCore.Qt.MatchFixedString)
        if assets_cat_index >= 0:
            self.ui.category_cb.setCurrentIndex(assets_cat_index)

        self.ui.create_btn.clicked.connect(self.refresh_tree_widget)
        self.ui.create_and_close_btn.clicked.connect(self.refresh_tree_widget)

        self.ui.show_name_cb.setDisabled(True)
        self.ui.category_cb.setDisabled(True)

        self.ui.show()

    def create_asset_category_menu(self):
        self.window = QtWidgets.QMainWindow()
        self.ui = xcg_create_asset_category_ui.CreateAssetCategoryUI()
        self.ui.show_name_cb.setCurrentText(self.show_name_cb.currentText())
        self.ui.show_name_cb.setDisabled(True)

        self.ui.show()

    def create_task_menu(self):
        self.window = QtWidgets.QMainWindow()
        self.ui = xcg_create_task_ui.CreateTaskUI()

        shows_index = self.ui.show_name_cb.findText(self.show_name_cb.currentText(), QtCore.Qt.MatchFixedString)
        if shows_index >= 0:
            self.ui.show_name_cb.setCurrentIndex(shows_index)

        self.ui.show_branch_cb.addItems(self.ui.get_show_branches())
        show_branches = self.ui.show_branch_cb.findText(self.get_sel_show_branch(), QtCore.Qt.MatchFixedString)
        if show_branches >= 0:
            self.ui.show_branch_cb.setCurrentIndex(show_branches)

        self.ui.category_cb.addItems(self.ui.get_categories())
        categories = self.ui.category_cb.findText(self.get_sel_category(), QtCore.Qt.MatchFixedString)
        if categories >= 0:
            self.ui.category_cb.setCurrentIndex(categories)

        self.ui.entry_name_cb.addItems(self.ui.get_entries())
        entries = self.ui.entry_name_cb.findText(self.get_selected_entry_name(), QtCore.Qt.MatchFixedString)
        if entries >= 0:
            self.ui.entry_name_cb.setCurrentIndex(entries)

        self.ui.populate_existing_tasks()

        self.ui.create_btn.clicked.connect(self.update_tasks_list)
        self.ui.create_and_close_btn.clicked.connect(self.update_tasks_list)

        self.ui.show_name_cb.setDisabled(True)
        self.ui.show_branch_cb.setDisabled(True)
        self.ui.category_cb.setDisabled(True)
        self.ui.entry_name_cb.setDisabled(True)

        self.ui.show()

    def create_task_pub_slot_menu(self):
        self.window = QtWidgets.QMainWindow()
        self.ui = xcg_edit_task_pub_slot_ui.CreateTaskPubSlotsUI()

        shows_index = self.ui.show_name_cb.findText(self.show_name_cb.currentText(), QtCore.Qt.MatchFixedString)
        if shows_index >= 0:
            self.ui.show_name_cb.setCurrentIndex(shows_index)

        self.ui.show_branch_cb.addItems(self.ui.get_show_branches())

        show_branches = self.ui.show_branch_cb.findText(self.get_sel_show_branch(), QtCore.Qt.MatchFixedString)
        if show_branches >= 0:
            self.ui.show_branch_cb.setCurrentIndex(show_branches)

        self.ui.category_cb.addItems(self.ui.get_categories())

        categories = self.ui.category_cb.findText(self.get_sel_category(), QtCore.Qt.MatchFixedString)
        if categories >= 0:
            self.ui.category_cb.setCurrentIndex(categories)

        self.ui.entry_name_cb.addItems(self.ui.get_entries())

        entries = self.ui.entry_name_cb.findText(self.get_selected_entry_name(), QtCore.Qt.MatchFixedString)
        if entries >= 0:
            self.ui.entry_name_cb.setCurrentIndex(entries)

        self.ui.task_name_cb.addItems(self.ui.get_all_tasks())

        entries = self.ui.task_name_cb.findText(self.get_selected_task(), QtCore.Qt.MatchFixedString)
        if entries >= 0:
            self.ui.task_name_cb.setCurrentIndex(entries)

        self.ui.create_btn.clicked.connect(self.populate_pub_slots)
        self.ui.create_and_close_btn.clicked.connect(self.populate_pub_slots)


        self.ui.populate_pub_slots()
        self.ui.show_name_cb.setDisabled(True)
        self.ui.show_branch_cb.setDisabled(True)
        self.ui.category_cb.setDisabled(True)
        self.ui.task_name_cb.setDisabled(True)
        self.ui.entry_name_cb.setDisabled(True)

        self.ui.show()

    def create_entry_definition_menu(self):
        self.window = QtWidgets.QMainWindow()
        self.ui = xcg_edit_entry_definition_ui.EditEntryDefinitionsUI()

        shows_index = self.ui.show_name_cb.findText(self.show_name_cb.currentText(), QtCore.Qt.MatchFixedString)
        if shows_index >= 0:
            self.ui.show_name_cb.setCurrentIndex(shows_index)

        self.ui.show_branch_cb.addItems(self.ui.get_show_branches())

        show_branches = self.ui.show_branch_cb.findText(self.get_sel_show_branch(), QtCore.Qt.MatchFixedString)
        if show_branches >= 0:
            self.ui.show_branch_cb.setCurrentIndex(show_branches)

        self.ui.category_cb.addItems(self.ui.get_categories())

        categories = self.ui.category_cb.findText(self.get_sel_category(), QtCore.Qt.MatchFixedString)
        if categories >= 0:
            self.ui.category_cb.setCurrentIndex(categories)

        self.ui.entry_name_cb.addItems(self.ui.get_entries())

        entries = self.ui.entry_name_cb.findText(self.get_selected_entry_name(), QtCore.Qt.MatchFixedString)
        if entries >= 0:
            self.ui.entry_name_cb.setCurrentIndex(entries)

        self.ui.show_name_cb.setDisabled(True)
        self.ui.show_branch_cb.setDisabled(True)
        self.ui.category_cb.setDisabled(True)
        self.ui.entry_name_cb.setDisabled(True)

        self.ui.shot_commit_btn.clicked.connect(self.update_entry_properties_list)
        self.ui.shot_commit_and_close_btn.clicked.connect(self.update_entry_properties_list)

        self.ui.asset_commit_btn.clicked.connect(self.update_entry_properties_list)
        self.ui.asset_commit_and_close_btn.clicked.connect(self.update_entry_properties_list)


        self.ui.show()

    def create_task_imports_from_menu(self):
        self.window = QtWidgets.QMainWindow()
        self.ui = xcg_edit_task_imports_from_ui.SetTaskImportsFromUI()

        shows_index = self.ui.show_name_cb.findText(self.show_name_cb.currentText(), QtCore.Qt.MatchFixedString)
        if shows_index >= 0:
            self.ui.show_name_cb.setCurrentIndex(shows_index)

        self.ui.show_branch_cb.addItems(self.ui.get_show_branches())
        show_branches = self.ui.show_branch_cb.findText(self.get_sel_show_branch(), QtCore.Qt.MatchFixedString)
        if show_branches >= 0:
            self.ui.show_branch_cb.setCurrentIndex(show_branches)

        self.ui.category_cb.addItems(self.ui.get_categories())
        categories = self.ui.category_cb.findText(self.get_sel_category(), QtCore.Qt.MatchFixedString)
        if categories >= 0:
            self.ui.category_cb.setCurrentIndex(categories)

        self.ui.entry_name_cb.addItems(self.ui.get_entries())
        entries = self.ui.entry_name_cb.findText(self.get_selected_entry_name(), QtCore.Qt.MatchFixedString)
        if entries >= 0:
            self.ui.entry_name_cb.setCurrentIndex(entries)

        self.ui.task_name_cb.addItems(self.ui.get_all_tasks())
        entries = self.ui.task_name_cb.findText(self.get_selected_task(), QtCore.Qt.MatchFixedString)
        if entries >= 0:
            self.ui.task_name_cb.setCurrentIndex(entries)

        self.ui.create_btn.clicked.connect(self.populate_task_import_schema)
        self.ui.create_and_close_btn.clicked.connect(self.populate_task_import_schema)

        self.ui.show_name_cb.setDisabled(True)
        self.ui.show_branch_cb.setDisabled(True)
        self.ui.category_cb.setDisabled(True)
        self.ui.entry_name_cb.setDisabled(True)
        self.ui.task_name_cb.setDisabled(True)
        self.ui.show()

    #TABS MENUS
    def show_properties_menu(self):
        print ("First Tab")


class MainUI(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(MainUI, self).__init__(parent)

        central_widget = XchangeControlCenterUI()
        self.setCentralWidget(central_widget)


if __name__ == "__main__":

    app = QtWidgets.QApplication(sys.argv)


    font = app.instance().setFont(QtGui.QFont())
    # huhu = {'full_range_in': 'ingest plate', 'full_range_out': 'ingest plate', 'frame_in': '1001', 'frame_out': '1200', 'handles_head': '8', 'handles_tail': '8', 'preroll': '10', 'shot_type': 'vfx', 'cut_in': '1009', 'cut_out': '1192', 'frame_rate': '24', 'motion_blur_high': '0.25', 'motion_blur_low': '-0.25', 'res_x': 'from plate', 'res_y': 'from plate'}
    # huhu2 = {'full_range_in': 'ingest XXXlXXXteXX'}
    test_dialog = MainUI()
    test_dialog.show()
    sys.exit(app.exec_())

