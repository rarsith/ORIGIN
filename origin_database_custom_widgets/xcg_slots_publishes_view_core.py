import sys
from bson import ObjectId
from PySide2 import QtWidgets, QtGui, QtCore
from origin_data_base import xcg_db_connection as xcon
from origin_config import xcg_validation as xval
from origin_config import xcg_slot_methods as xslop
from origin_data_base import xcg_db_actions as xac
from origin_database_custom_widgets.xcg_slots_publishes_view_UI import SlotsPublishesViewUI

from origin_icons import *

img_path = "../origin_icons/play_icon_vsmall.png"

class SetReviewableComponent(QtWidgets.QPushButton):
    def __init__(self, parent=None):
        super(SetReviewableComponent, self).__init__(parent)
        pic_video = QtGui.QPixmap(img_path)
        self.setIcon(pic_video)


class SlotPublishesViewCore(SlotsPublishesViewUI):

    def __init__(self,
                 show_name = '',
                 branch_name = '',
                 category_name = '',
                 entry_name = '',
                 task_name = '',
                 main_pub_id = '',
                 parent=None):
        super(SlotPublishesViewCore, self).__init__(parent)

        self.show_name = show_name
        self.branch_name = branch_name
        self.category_name = category_name
        self.entry_name = entry_name
        self.task_name = task_name
        self.main_pub_id = main_pub_id

        self.return_pub_id()
        self.get_published_slots_ids()
        self.populate_main_widget()


    def show_name(self):
        return

    def return_pub_id(self):
        return (self.main_pub_id)

    def get_published_slots_ids(self):
        slot_pub_ids = xac.get_db_referenced_attr('publishes', self.main_pub_id, 'publishing_slots', '_id')
        return slot_pub_ids

    def get_selection_id(self):
        if self.slot_publish_view_tw.selectedItems():
            cell_name = self.slot_publish_view_tw.selectedItems()[7]
            return cell_name.text()

    def get_selection_collection(self):
        if self.slot_publish_view_tw.selectedItems():
            cell_name = self.slot_publish_view_tw.selectedItems()[8]
            return cell_name.text()

    def connect_to_slot(self, slot_func):
        cell_name = self.slot_publish_view_tw.selectionModel().selectionChanged.connect(slot_func)
        return cell_name


    def populate_main_widget(self):

        self.slot_publish_view_tw.setRowCount(0)
        get_publish_id = xac.get_db_referenced_attr('publishes', self.main_pub_id, 'publishing_slots', '_id')
        if not get_publish_id == None:
            rows_cnt = len(get_publish_id)
            self.slot_publish_view_tw.setRowCount(rows_cnt)
            cnt = 0
            for name in get_publish_id:
                self.populate_publishes(str(name), cnt)
                cnt += 1
            return get_publish_id

    def populate_publishes(self, name, row):
        item = QtWidgets.QTableWidgetItem(name)

        self.slot_publish_view_tw.setItem(row, 1, item)

        self.status_cb = QtWidgets.QComboBox()
        self.status_cb.addItems(xval.VALID_TASK_STATUSES)
        get_publish_collection = xac.get_db_referenced_attr('publishes', self.main_pub_id, 'publishing_slots',
                                                            'parent_collection')
        self.get_publish_collection = xac.get_db_values(get_publish_collection[0], name, "parent_collection")
        self.get_publish_id = xac.get_db_values(get_publish_collection[0], name, "_id")
        self.get_publish_name = xac.get_db_values(get_publish_collection[0], name, "display_name")
        self.get_publish_version = xac.get_db_values(get_publish_collection[0], name, "version")
        self.get_publish_version_origin = xac.get_db_values(get_publish_collection[0], name, "version_origin")
        self.get_publish_task = xac.get_db_values(get_publish_collection[0], name, "task_name")
        self.get_publish_user = xac.get_db_values(get_publish_collection[0], name, "artist")
        self.get_publish_status = xac.get_db_values(get_publish_collection[0], name, "status")
        self.get_publish_date = xac.get_db_values(get_publish_collection[0], name, "date")
        self.get_publish_time = xac.get_db_values(get_publish_collection[0], name, "time")

        try:
            self.status_cb.setCurrentText(self.get_publish_status)
        except:
            pass

        self.slot_publish_view_tw.setCellWidget(row, 0, SetReviewableComponent(self))
        self.slot_publish_view_tw.setItem(row, 1, QtWidgets.QTableWidgetItem(self.get_publish_name))
        self.slot_publish_view_tw.setItem(row, 2, QtWidgets.QTableWidgetItem(self.get_publish_version))
        self.slot_publish_view_tw.setItem(row, 3, QtWidgets.QTableWidgetItem(self.get_publish_task))
        self.slot_publish_view_tw.setCellWidget(row, 4, self.status_cb)
        self.slot_publish_view_tw.setItem(row, 5, QtWidgets.QTableWidgetItem(self.get_publish_version_origin))
        self.slot_publish_view_tw.setItem(row, 6, QtWidgets.QTableWidgetItem(self.get_publish_user))
        self.slot_publish_view_tw.setItem(row, 7, QtWidgets.QTableWidgetItem(str(self.get_publish_date)))
        self.slot_publish_view_tw.setItem(row, 8, QtWidgets.QTableWidgetItem(str(self.get_publish_time)))
        self.slot_publish_view_tw.setItem(row, 9, QtWidgets.QTableWidgetItem(str(self.get_publish_id)))
        self.slot_publish_view_tw.setItem(row, 10, QtWidgets.QTableWidgetItem(str(self.get_publish_collection)))




if __name__ == "__main__":

    # db = xcon.server.exchange
    # test_position = db.show_name
    # test = test_position.find({}, {"_id": 1, "show_name": 1})

    app = QtWidgets.QApplication(sys.argv)
    show_name = 'Test'
    branch_name = 'assets'
    category_name = 'characters'
    entry_name = 'greenHulk'
    task_name = 'modeling'
    # pub_id = '60b7cabbca7fdd099e5d32c9'
    test_dialog = SlotPublishesViewCore(main_pub_id=pub_id)




    # test_dialog.populate_main_widget()
    test_dialog.show()
    sys.exit(app.exec_())