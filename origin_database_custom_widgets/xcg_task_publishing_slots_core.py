import sys
from PySide2 import QtWidgets
from origin_data_base import xcg_db_connection as xcon
from origin_config import xcg_validation as xval
from origin_config import xcg_slot_methods as xslop
from origin_data_base import xcg_db_actions as xac
from origin_database_custom_widgets.xcg_task_publishing_slots_UI import PublishSlotsWidgetUI

class PublishSlotsWidgetCore(PublishSlotsWidgetUI):
    def __init__(self, show_name='',
                 branch_name='',
                 category_name='',
                 entry_name='',
                 task_name='',
                 parent=None):
        super(PublishSlotsWidgetCore, self).__init__(parent)

        self.show_name = show_name
        self.branch_name = branch_name
        self.category_name = category_name
        self.entry_name = entry_name
        self.task_name = task_name

        self.create_connections()
        self.populate_main_widget()

    def create_connections(self):
        self.delete_list_item_btn.clicked.connect(self.remove_pub_slot)
        self.save_btn.clicked.connect(self.db_commit)
        self.refresh_btn.clicked.connect(self.populate_main_widget)
        self.add_pub_slot_btn.clicked.connect(self.add_to_pub_list)

# PublishSlotsWidget -- START
    def get_properties(self):
        pub_slots = xac.get_pub_slots(self.show_name,
                                      self.branch_name,
                                      self.category_name,
                                      self.entry_name,
                                      self.task_name)
        return pub_slots

    def populate_main_widget(self):
        properties = self.get_properties()
        if not properties == None:
            rows_cnt = len(properties)
            self.publish_slots_wdg.setRowCount(rows_cnt)
            cnt = 0
            for name in properties:
                self.create_pub_slots(name, cnt)
                cnt += 1
        return properties

    def get_entry_tasks(self):
        tasks = xac.get_tasks(self.show_name,
                              self.branch_name,
                              self.category_name,
                              self.entry_name)
        return tasks

    def create_pub_slots(self, name, row):
        item = QtWidgets.QTableWidgetItem(name)
        self.publish_slots_wdg.setItem(row, 0, item)

        self.set_type_cb = QtWidgets.QComboBox()
        self.set_type_cb.addItems(xval.SLOTS_TYPES)
        self.set_method_cb = QtWidgets.QComboBox()
        self.set_method_cb.addItems(list(xslop.SLOTS_METHODS.values()))

        self.set_source_cb = QtWidgets.QComboBox()
        self.set_source_cb.addItems(self.get_current_pub_slots())

        self.set_reviewable_ckb = QtWidgets.QCheckBox()
        self.set_active_ckb = QtWidgets.QCheckBox()

        try:
            self.set_type_cb.setCurrentText(self.get_db_pub_type(name))
            self.set_method_cb.setCurrentText(self.get_db_pub_method(name))
            self.set_source_cb.setCurrentText(str(self.get_db_pub_source(name)))
            self.set_reviewable_ckb.setChecked(bool(self.get_db_pub_reviewable(name)))
            self.set_active_ckb.setChecked(self.get_db_pub_active(name))
        except:
            pass

        self.publish_slots_wdg.setCellWidget(row, 1, self.set_type_cb)
        self.publish_slots_wdg.setCellWidget(row, 2, self.set_method_cb)
        self.publish_slots_wdg.setCellWidget(row, 3, self.set_source_cb)
        self.publish_slots_wdg.setCellWidget(row, 4, self.set_reviewable_ckb)
        self.publish_slots_wdg.setCellWidget(row, 5, self.set_active_ckb)

    def get_db_pub_type(self, slot):
        properties = self.get_properties()
        pub_type = properties[slot]['type']
        return pub_type

    def get_db_pub_method(self, slot):
        properties = self.get_properties()
        pub_method = properties[slot]['method']
        return pub_method

    def get_db_pub_source(self, slot):
        properties = self.get_properties()
        pub_source = properties[slot]['source']
        return pub_source

    def get_db_pub_reviewable(self, slot):
        properties = self.get_properties()
        pub_is_reviewable = properties[slot]['reviewable']
        return pub_is_reviewable

    def get_db_pub_active(self, slot):
        properties = self.get_properties()
        pub_is_active = properties[slot]['active']
        return pub_is_active

    def get_slot_name(self, row, column):
        slot_name = self.publish_slots_wdg.item(row, column)
        return slot_name.text()

    def get_slot_type(self, row, column):
        slot_type = self.publish_slots_wdg.cellWidget(row, column)
        return slot_type.currentText()

    def get_pub_method(self, row, column):
        slot_method = self.publish_slots_wdg.cellWidget(row, column)
        return slot_method.currentText()

    def get_pub_source(self, row, column):
        slot_method = self.publish_slots_wdg.cellWidget(row, column)
        return slot_method.currentText()

    def reviewable_is_checked(self, row, column):
        rev_checked = self.publish_slots_wdg.cellWidget(row, column)
        return rev_checked.isChecked()

    def active_is_checked(self, row, column):
        act_is_checked = self.publish_slots_wdg.cellWidget(row, column)
        return act_is_checked.isChecked()

    def get_pub_buffer_content(self):
        items = []
        rows = self.publish_slots_wdg.rowCount()

        for r in range(rows):
            get_slot_name = self.get_slot_name(r, 0)
            get_existing_properties = self.get_properties()
            if get_slot_name in get_existing_properties:
                get_used_by = self.get_db_slot_used_by(get_slot_name)
            else:
                get_used_by = []

            dictionary_build = {self.get_slot_name(r, 0):{'type':self.get_slot_type(r, 1),
                                                          'method':self.get_pub_method(r, 2),
                                                          'used_by':get_used_by,
                                                          'source':self.get_pub_source(r, 3),
                                                          'reviewable':self.reviewable_is_checked(r, 4),
                                                          'active':self.active_is_checked(r, 5)}}

            items.append(dictionary_build)



        return items

    def get_db_slot_used_by(self, slot):
        properties = self.get_properties()
        pub_is_used_by = properties[slot]['used_by']
        return pub_is_used_by

    def get_first_cell(self):
        clickme = QtWidgets.QApplication.focusWidget()
        index = self.publish_slots_wdg.indexAt(clickme.pos())
        if index.isValid():
            get_name_cell = (index.column()-3)
            slot_name = self.publish_slots_wdg.item(index.row(), get_name_cell)
            print ('Open Menu for {0}'.format (slot_name.text()))
            return slot_name.text()

    def get_current_pub_slots(self):
        complete_list = list()
        pub_slots = xac.get_task_pub_slots(self.show_name,
                                           self.branch_name,
                                           self.category_name,
                                           self.entry_name,
                                           self.task_name)
        if pub_slots:
            complete_list.append('root')
            for each in pub_slots:
                complete_list.append(each)

        return complete_list

    def insert_pub_slot_row(self, name):
        self.publish_slots_wdg.insertRow(0)
        self.create_pub_slots(name, 0)

    def remove_pub_slot(self):
        listItems = self.publish_slots_wdg.currentItem()
        selected_index = self.publish_slots_wdg.indexFromItem(listItems)
        self.publish_slots_wdg.removeRow(selected_index.row())

    def db_commit(self):
        get_wdg_content = self.get_pub_buffer_content()

        xac.remove_all_task_pub_slots(self.show_name,
                                      self.branch_name,
                                      self.category_name,
                                      self.entry_name,
                                      self.task_name)


        xac.update_task_pub_slot_dict(self.show_name,
                                      self.branch_name,
                                      self.category_name,
                                      self.entry_name,
                                      self.task_name,
                                      pub_slot=get_wdg_content)

# PublishSlotsWidget -- END

    def add_to_pub_list(self):
        if self.add_pub_slot_le.text():
            self.insert_pub_slot_row(self.add_pub_slot_le.text())
            self.add_pub_slot_le.clear()
        else:
            return

if __name__ == "__main__":

    db = xcon.server.exchange
    test_position = db.show_name
    test = test_position.find({}, {"_id": 1, "show_name": 1})

    app = QtWidgets.QApplication(sys.argv)

    test_dialog = PublishSlotsWidgetCore()
    test_dialog.show_name = 'Test'
    test_dialog.branch_name = 'origin_library'
    test_dialog.category_name = 'airplanes'
    test_dialog.entry_name = '707'
    test_dialog.task_name = 'modeling'
    test_dialog.populate_main_widget()
    test_dialog.show()
    sys.exit(app.exec_())