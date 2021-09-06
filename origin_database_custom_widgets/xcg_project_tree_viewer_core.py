from PySide2 import QtWidgets, QtCore, QtGui
from origin_database_custom_widgets.xcg_project_tree_viewer_UI import ProjectTreeViewerUI
from origin_data_base import xcg_db_helpers as xhlp
from origin_data_base import xcg_db_actions as xac
from origin_ui import create_show_ui
from origin_ui import create_seq_ui
from origin_ui import create_asset_ui
from origin_ui import create_shot_ui
from origin_ui import create_asset_category_ui
from origin_ui import create_show_category_ui



class ProjectTreeViewerCore(ProjectTreeViewerUI):

    def __init__(self, show_name='', parent=None):
        super(ProjectTreeViewerCore, self).__init__(parent)

        self.show_name = show_name
        self.create_show_actions()
        self.create_connections()
        self.set_show_to()
        self.populate_shows_cb()
        self.refresh_tree_widget()
        self.context_menu()

    def create_connections(self):
        self.show_select_cb.currentIndexChanged.connect(self.comboBox_shows)
        self.show_select_cb.currentIndexChanged.connect(self.refresh_tree_widget)

        self.project_tree_viewer_wdg.itemClicked.connect(self.get_selected_entry_name)
        self.project_tree_viewer_wdg.itemClicked.connect(self.get_sel_show_branch_category)
        self.project_tree_viewer_wdg.itemClicked.connect(self.get_selected_type)

        self.about_action.triggered.connect(self.about)
        self.create_show_action.triggered.connect(self.create_show_menu)
        self.create_show_branch_action.triggered.connect(self.create_show_branches_menu)

        self.create_seq_action.triggered.connect(self.create_seq_menu)
        self.create_shot_action.triggered.connect(self.create_shot_menu)
        self.create_asset_action.triggered.connect(self.create_asset_menu)
        self.create_asset_category_action.triggered.connect(self.create_asset_category_menu)
        self.remove_entry_action.triggered.connect(self.remove_entry_menu)

    def get_shows(self):
        get_versions = xac.get_all_active_shows()
        return sorted(get_versions)

    def refresh_shows(self):
        store = []
        current_selected_show = self.comboBox_shows()
        get_versions = xac.get_all_active_shows()
        for show in get_versions:
            store.append(show)

        self.show_select_cb.clear()
        self.show_select_cb.addItems(store)
        self.show_select_cb.setCurrentText(current_selected_show)
        return sorted(store)

    def comboBox_shows(self):
        text = self.show_select_cb.currentText()
        return text

    def populate_shows_cb(self):
        self.show_select_cb.addItems(self.get_shows())

    def set_show_to(self):
        self.show_select_cb.setCurrentText(self.show_name)

    def refresh_tree_widget(self):
        try:
            self.project_tree_viewer_wdg.clear()
            get_entity = self.get_show_structure()
            get_categories = xhlp.get_entity_root_structure(get_entity)
            for category in sorted(get_categories):
                item = self.show_tree_create_item(category)
                self.project_tree_viewer_wdg.addTopLevelItem(item)
            self.project_tree_viewer_wdg.expandAll()
        except:
            pass

    def get_selected_show(self):
        return self.show_select_cb.currentText()

    def get_selected_entry_name(self):
        names = []
        get_selected_objects = self.project_tree_viewer_wdg.selectedItems()
        if len(get_selected_objects) == 0:
            return []
        elif len(get_selected_objects) >= 1:
            for item in get_selected_objects:
                names.append(item.text(0))
            return names[0]

    def get_selected_entry(self):
        names = []
        get_selected_objects = self.project_tree_viewer_wdg.selectedItems()
        if len(get_selected_objects) == 0:
            return []
        elif len(get_selected_objects) >= 1:
            for item in get_selected_objects:
                names.append(item.text(0))
            return names[0]

    def get_selected_type(self):
        entry_selected = self.project_tree_viewer_wdg.hasFocus()
        if entry_selected:
            get_selected_objects_type = xac.get_entry_type(self.show_select_cb.currentText(),
                                                           self.get_sel_show_branch(),
                                                           self.get_sel_category(),
                                                           self.get_selected_entry_name())
            return get_selected_objects_type

    def get_sel_show_branch_category(self):
        get_selected_objects = self.project_tree_viewer_wdg.selectedItems()
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
        get_selected_objects = self.project_tree_viewer_wdg.selectedItems()
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

    def get_parent(self):
        get_selected_objects = self.project_tree_viewer_wdg.currentItem()
        parent = get_selected_objects.parent()
        if parent:
            return parent.text(0)

    def get_grandparent(self):
        get_selected_objects = self.project_tree_viewer_wdg.currentItem()
        parent = get_selected_objects.parent()
        try:
            grandparent = parent.parent()
            return grandparent.text(0)
        except:
            pass

    def get_sel_hierachy(self):
        branch = list()
        category = list()
        entry = list()
        get_selected_objects = self.project_tree_viewer_wdg.currentItem()
        get_selected_show = self.show_select_cb.currentText()


        if get_selected_objects is None:
            return[]

        else:

            parent = self.get_parent()
            grandparent = self.get_grandparent()

            if not parent:
                branch.append(get_selected_objects.text(0))


            elif not grandparent:
                branch.append(parent)
                category.append(get_selected_objects.text(0))

            else:
                branch.append(grandparent)
                category.append(parent)
                entry.append(get_selected_objects.text(0))

        return (''.join(get_selected_show)),(''.join(branch)), (''.join(category)), (''.join(entry))

    def get_sel_category(self):
        get_selected_objects = self.project_tree_viewer_wdg.selectedItems()

        if len(get_selected_objects) == 0:
            return []
        elif len(get_selected_objects) >= 1:
            for item in get_selected_objects:
                try:
                    parent = item.parent()
                    return parent.text(0)
                except:
                    pass

    def get_parent_path(self, item):
        def get_parent(item, outstring):
            if item.parent() is None:
                return outstring
            outstring = item.parent.text(0) + '.' + outstring
            return get_parent(item.parent, outstring)

        output = get_parent(item, item.text(0))

        return output

    def get_sel_entry_path(self):
        get_selected_entry_objects = self.project_tree_viewer_wdg.selectedItems()

        if len(get_selected_entry_objects) == 0:
            return []
        elif len(get_selected_entry_objects) >= 1:
            for item in get_selected_entry_objects:
                try:
                    parent = item.parent()
                    return parent.text(0)
                except:
                    pass

    def get_show_structure(self):
        try:
            entity = xac.get_show_base_structure(self.show_select_cb.currentText())
            return entity
        except:
            pass

    def show_tree_create_item(self, name):
        item = QtWidgets.QTreeWidgetItem([name])
        self.add_children(item)
        return item

    def add_children(self, item):
        get_children = xhlp.deep_values(item.text(0), self.get_show_structure())
        for children in get_children:
            for child in sorted(children):
                child_item = self.show_tree_create_item(child)
                item.addChild(child_item)

    def context_menu(self):
        self.project_tree_viewer_wdg.customContextMenuRequested.connect(self.show_tree_con_menu)

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
            context_menu.addAction(self.save_task_schema_action)

            context_menu.addSeparator()
            context_menu.addAction(self.remove_entry_action)
            context_menu.exec_(self.mapToGlobal(point))

    def create_show_actions(self):
        self.about_action = QtWidgets.QAction("About", self)
        self.create_show_action = QtWidgets.QAction("Create Show...", self)
        self.create_show_branch_action = QtWidgets.QAction("Create Show Branch...", self)
        self.create_seq_action = QtWidgets.QAction("Create Seq...", self)
        self.create_shot_action = QtWidgets.QAction("Create Shot...", self)
        self.create_asset_action = QtWidgets.QAction("Create Asset...", self)
        self.create_asset_category_action = QtWidgets.QAction("Create Asset Category...", self)
        self.remove_entry_action = QtWidgets.QAction("Remove Entry...", self)
        self.edit_entry_definition = QtWidgets.QAction("Edit Definition...", self)
        self.save_task_schema_action = QtWidgets.QAction("Task Schema...", self)
        self.edit_bundle = QtWidgets.QAction("Edit Bundle...", self)

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
            xac.remove_entry(self.show_select_cb.currentText(),
                             self.get_sel_show_branch(),
                             self.get_sel_category(),
                             self.get_selected_entry_name())
            self.refresh_tree_widget()
        else:
            print ("Just closed the damn window")
            custom_dialog.close()

    def create_show_menu(self):
        self.window = QtWidgets.QMainWindow()
        self.ui = create_show_ui.CreateShowUI()
        self.ui.show()

    def create_show_branches_menu(self):
        self.window = QtWidgets.QMainWindow()
        self.ui = create_show_category_ui.CreateShowCategoryUI()
        self.ui.show_name_cb.setDisabled(True)
        self.ui.show()

    def create_seq_menu(self):
        self.window = QtWidgets.QMainWindow()
        self.ui = create_seq_ui.CreateSeqUI()
        self.ui.show_name_cb.setDisabled(True)
        self.ui.show_name_cb.setCurrentText(self.show_select_cb.currentText())
        self.ui.show()

    def create_shot_menu(self):
        self.window = QtWidgets.QMainWindow()
        self.ui = create_shot_ui.CreateShotUI()
        self.ui.parent_seq_cb.setCurrentText(self.get_selected_entry_name())

        shows_index = self.ui.show_name_cb.findText(self.show_select_cb.currentText(), QtCore.Qt.MatchFixedString)
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
        self.ui = create_asset_ui.CreateAssetUI()

        shows_index = self.ui.show_name_cb.findText(self.show_select_cb.currentText(), QtCore.Qt.MatchFixedString)
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
        self.ui = create_asset_category_ui.CreateAssetCategoryUI()
        self.ui.show_name_cb.setCurrentText(self.show_select_cb.currentText())
        self.ui.show_name_cb.setDisabled(True)

        self.ui.show()



if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    font = app.instance().setFont(QtGui.QFont())

    test_dialog = ProjectTreeViewerCore('Test')
    # test_dialog.current_show()
    # test_dialog.comboBox_shows()
    # test_dialog.set_show_to()
    test_dialog.show()
    sys.exit(app.exec_())