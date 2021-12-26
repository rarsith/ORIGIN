import sys

from PySide2 import QtWidgets, QtGui
from origin_data_base import xcg_db_connection as xcon
from origin_config import xcg_validation as xval
from origin_data_base import xcg_db_actions as xac
from origin_database_custom_widgets.xcg_main_publishes_view_UI import MainPublishesViewUI

from origin_icons import *


img_path = "F:\\Radu_Work\\Pycharm_Projects\\Xchange\\origin_icons\\play_icon_vsmall.png"

class SetReviewableComponent(QtWidgets.QPushButton):
    def __init__(self, parent=None):
        super(SetReviewableComponent, self).__init__(parent)
        pic_video = QtGui.QPixmap(img_path)
        self.setIcon(pic_video)


class MainPublishesViewCore(MainPublishesViewUI):
    def __init__(self,show_name = '',
                 branch_name = '',
                 category_name = '',
                 entry_name = '',
                 task_name = '',
                 parent=None):
        super(MainPublishesViewCore, self).__init__(parent)

        self.show_name = show_name
        self.branch_name = branch_name
        self.category_name = category_name
        self.entry_name = entry_name
        self.task_name = task_name

        self.populate_main_widget()
        self.create_connections()

    def create_connections(self):
        self.refresh_btn.clicked.connect(self.populate_main_widget)

    def connect_to_slot(self, slot_func):
        cell_name = self.publish_view_tw.selectionModel().selectionChanged.connect(slot_func)
        return cell_name

    def get_selection_id(self):
        if self.publish_view_tw.selectedItems():
            cell_name = self.publish_view_tw.selectedItems()[6]
            return cell_name.text()


# PublishSlotsWidget -- START
    def get_value_of(self, slot):
        publishes = xac.get_db_publishes_ids("publishes",
                                             self.show_name,
                                             self.branch_name,
                                             self.category_name,
                                             self.entry_name,
                                             self.task_name )
        return publishes

    def populate_main_widget(self):
        self.publish_view_tw.setRowCount(0)
        get_publish_id = xac.get_db_publishes_ids("publishes",
                                             self.show_name,
                                             self.branch_name,
                                             self.category_name,
                                             self.entry_name,
                                             self.task_name )
        if not get_publish_id == None:
            rows_cnt = len(get_publish_id)
            self.publish_view_tw.setRowCount(rows_cnt)
            cnt = 0
            for name in get_publish_id:
                self.populate_publishes(name, cnt)
                cnt += 1
            return get_publish_id

    def populate_publishes(self, name, row):
        item = QtWidgets.QTableWidgetItem(name)

        self.publish_view_tw.setItem(row, 2, item)

        self.status_cb = QtWidgets.QComboBox()
        self.status_cb.addItems(xval.VALID_TASK_STATUSES)
        self.status_cb.setStyleSheet('font-size: 8px;' 'font-family: "Rubik";')

        self.get_id = xac.get_db_values("publishes", name, "_id")
        self.get_publish_name = xac.get_db_values("publishes", name, "display_name")
        self.get_publish_version = xac.get_db_values("publishes", name, "version")
        self.get_publish_task = xac.get_db_values("publishes", name, "task_name")
        self.get_publish_user = xac.get_db_values("publishes", name, "artist")
        self.get_publish_status = xac.get_db_values("publishes", name, "status")
        self.get_publish_date = xac.get_db_values("publishes", name, "date")
        self.get_publish_time = xac.get_db_values("publishes", name, "time")

        try:
            self.status_cb.setCurrentText(self.get_publish_status)
        except:
            pass

        self.publish_view_tw.setItem(row, 0, QtWidgets.QTableWidgetItem(self.get_publish_name))
        self.publish_view_tw.setItem(row, 1, QtWidgets.QTableWidgetItem(self.get_publish_version))
        self.publish_view_tw.setItem(row, 2, QtWidgets.QTableWidgetItem(self.get_publish_task))
        self.publish_view_tw.setCellWidget(row, 3, self.status_cb)
        self.publish_view_tw.setItem(row, 4, QtWidgets.QTableWidgetItem(self.get_publish_user))
        self.publish_view_tw.setItem(row, 5, QtWidgets.QTableWidgetItem(str(self.get_publish_date)))
        self.publish_view_tw.setItem(row, 6, QtWidgets.QTableWidgetItem(str(self.get_publish_time)))
        self.publish_view_tw.setItem(row, 7, QtWidgets.QTableWidgetItem(str(self.get_id)))


    def insert_item(self, row, column, text):
        item = QtWidgets.QTableWidgetItem(text)
        self.setItem(row, column, item)

    def get_published_status(self):
        version_status = self.get_value_of("status")
        return version_status



if __name__ == "__main__":

    db = xcon.server.exchange
    test_position = db.show_name
    test = test_position.find({}, {"_id": 1, "show_name": 1})

    app = QtWidgets.QApplication(sys.argv)
    show_name = 'Test'
    # branch_name = 'assets'
    # category_name = 'characters'
    # entry_name = 'hulkGreen'
    # task_name = 'surfacing'
    test_dialog = MainPublishesViewCore(show_name)
    test_dialog.populate_main_widget()
    test_dialog.show()
    sys.exit(app.exec_())