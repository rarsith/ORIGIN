import sys
import pprint
from PySide2 import QtWidgets, QtCore, QtGui
from xcg_data_base import xcg_db_connection as xcon
from xcg_config import xcg_validation as xval
from xcg_config import xcg_slot_methods as xslop


from xcg_data_base import xcg_db_actions as xac




db = xcon.server.exchange
test_position = db.show_name
test = test_position.find({}, {"_id":1, "show_name":1})


class PublishSlotsWidget(QtWidgets.QTableWidget):
    def __init__(self, parent=None):
        super(PublishSlotsWidget, self).__init__(parent)

        self.show_sel = ''
        self.branch = ''
        self.category = ''
        self.entry = ''
        self.task = ''


        self.widget_build()

    def widget_build(self):
        self.setDisabled(False)
        self.setMinimumWidth(465)
        self.setColumnCount(6)
        self.setHorizontalHeaderLabels(["Slot_Name", "Type", "Method", "Source","R", "A"])
        self.setShowGrid(False)
        self.setAlternatingRowColors(True)
        header = self.verticalHeader()
        header.hide()
        self.setColumnWidth(0, 100)
        self.setColumnWidth(1, 80)
        self.setColumnWidth(2, 95)
        self.setColumnWidth(3, 80)
        self.setColumnWidth(4, 20)
        self.setColumnWidth(5, 20)

    def get_properties(self):
        pub_slots = xac.get_pub_slots(self.show_sel,
                                      self.branch,
                                      self.category,
                                      self.entry,
                                      self.task)
        return pub_slots

    def populate_pub_slots(self):
        properties = self.get_properties()
        if not properties == None:
            rows_cnt = len(properties)
            self.setRowCount(rows_cnt)
            cnt = 0
            for name in properties:
                self.create_pub_slots(name, cnt)
                cnt += 1
        return properties

    def get_entry_tasks(self):
        tasks = xac.get_tasks(self.show_sel,
                              self.branch,
                              self.category,
                              self.entry)
        return tasks

    def create_pub_slots(self, name, row):
        item = QtWidgets.QTableWidgetItem(name)
        self.setItem(row, 0, item)

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

        self.setCellWidget(row, 1, self.set_type_cb)
        self.setCellWidget(row, 2, self.set_method_cb)
        self.setCellWidget(row, 3, self.set_source_cb)
        self.setCellWidget(row, 4, self.set_reviewable_ckb)
        self.setCellWidget(row, 5, self.set_active_ckb)

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
        slot_name = self.item(row, column)
        return slot_name.text()

    def get_slot_type(self, row, column):
        slot_type = self.cellWidget(row, column)
        return slot_type.currentText()

    def get_pub_method(self, row, column):
        slot_method = self.cellWidget(row, column)
        return slot_method.currentText()

    def get_pub_source(self, row, column):
        slot_method = self.cellWidget(row, column)
        return slot_method.currentText()

    def reviewable_is_checked(self, row, column):
        rev_checked = self.cellWidget(row, column)
        return rev_checked.isChecked()

    def active_is_checked(self, row, column):
        act_is_checked = self.cellWidget(row, column)
        return act_is_checked.isChecked()

    def get_pub_buffer_content(self):
        items = []
        propp = self.get_properties()
        print(propp)
        rows = self.rowCount()

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
        index = self.indexAt(clickme.pos())
        if index.isValid():
            get_name_cell = (index.column()-3)
            slot_name = self.item(index.row(), get_name_cell)
            print ('Open Menu for {0}'.format (slot_name.text()))
            return slot_name.text()

    def get_current_pub_slots(self):
        complete_list = list()
        pub_slots = xac.get_task_pub_slots(self.show_sel,
                                           self.branch,
                                           self.category,
                                           self.entry,
                                           self.task)
        if pub_slots:
            complete_list.append('root')
            for each in pub_slots:
                complete_list.append(each)

        return complete_list

    def insert_pub_slot_row(self, name):
        self.insertRow(0)
        self.create_pub_slots(name, 0)

    def remove_pub_slot(self):
        listItems = self.currentItem()
        selected_index = self.indexFromItem(listItems)
        self.removeRow(selected_index.row())

    def db_commit(self):
        get_wdg_content = self.get_pub_buffer_content()

        xac.remove_all_task_pub_slots(self.show_sel,
                                      self.branch,
                                      self.category,
                                      self.entry,
                                      self.task)


        xac.update_task_pub_slot_dict(self.show_sel,
                                      self.branch,
                                      self.category,
                                      self.entry,
                                      self.task,
                                      pub_slot=get_wdg_content)



class PublishSlotsWidgetUI(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(PublishSlotsWidgetUI, self).__init__(parent)


        self.create_widgets()
        self.create_layout()
        self.create_connections()
        self.populate()
        self.dialog.populate_pub_slots()

    def create_widgets(self):
        self.tasks_pub_slots_properties_lb = QtWidgets.QLabel("Publishing Slots")

        self.add_pub_slot_le = QtWidgets.QLineEdit()
        self.add_pub_slot_le.setPlaceholderText('New Slot Name!')
        self.add_pub_slot_btn = QtWidgets.QPushButton('Add')

        self.dialog = PublishSlotsWidget()
        self.delete_list_item_btn = QtWidgets.QPushButton("Remove Selected")
        self.save_btn = QtWidgets.QPushButton("Commit")
        self.refresh_btn = QtWidgets.QPushButton("Refresh")

    def create_layout(self):
        top_layout = QtWidgets.QHBoxLayout()
        top_layout.addWidget(self.add_pub_slot_le)
        top_layout.addWidget(self.add_pub_slot_btn)

        layout = QtWidgets.QVBoxLayout()
        layout.addLayout(top_layout)
        layout.addWidget(self.dialog)
        layout.addWidget(self.delete_list_item_btn)
        layout.addWidget(self.save_btn)
        layout.addWidget(self.refresh_btn)

        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.addWidget(self.tasks_pub_slots_properties_lb)
        main_layout.addLayout(layout)

    def create_connections(self):
        self.delete_list_item_btn.clicked.connect(self.dialog.remove_pub_slot)
        self.save_btn.clicked.connect(self.dialog.db_commit)
        self.refresh_btn.clicked.connect(self.populate)
        self.add_pub_slot_btn.clicked.connect(self.add_to_pub_list)


    def add_to_pub_list(self):
        if self.add_pub_slot_le.text():
            self.dialog.insert_pub_slot_row(self.add_pub_slot_le.text())
            self.add_pub_slot_le.clear()
        else:
            return


    def populate(self):
        self.dialog.populate_pub_slots()



if __name__ == "__main__":

    # huhu = {'full_range_in': 'ingest plate', 'full_range_out': 'ingest plate', 'frame_in': '1001', 'frame_out': '1200', 'handles_head': '8', 'handles_tail': '8', 'preroll': '10', 'shot_type': 'vfx', 'cut_in': '1009', 'cut_out': '1192', 'frame_rate': '24', 'motion_blur_high': '0.25', 'motion_blur_low': '-0.25', 'res_x': 'from plate', 'res_y': 'from plate'}
    # huhu2 = {'full_range_in': 'ingest XXXlXXXteXX'}
    app = QtWidgets.QApplication(sys.argv)
    test_dialog = PublishSlotsWidgetUI()

    test_dialog.dialog.show_sel = 'Test'
    test_dialog.dialog.branch = 'sequences'
    test_dialog.dialog.category = 'TST'
    test_dialog.dialog.entry = '0100'
    test_dialog.dialog.task = 'animation'
    test_dialog.dialog.populate_pub_slots()


    test_dialog.show()
    sys.exit(app.exec_())