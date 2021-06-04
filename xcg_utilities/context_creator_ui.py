import sys
import os
from PySide2 import QtWidgets
from xcg_data_base import xcg_db_actions as xac


class SetContextUI(QtWidgets.QDialog):

    def __init__(self, parent=None):
        super(SetContextUI, self).__init__(parent)

        self.setWindowTitle("Set Context")
        self.setMinimumSize(370, 300)


        self.create_widgets()
        self.create_layout()
        self.create_connections()

    def create_widgets(self):
        self.show_name_cb = QtWidgets.QComboBox()
        self.show_name_cb.addItems(self.get_shows())

        self.branch_cb = QtWidgets.QComboBox()
        self.branch_cb.addItems(['assets', 'sequences'])

        self.category_cb = QtWidgets.QComboBox()
        self.category_cb.addItems(self.get_shows_seq())

        self.entry_cb = QtWidgets.QComboBox()
        # self.entry_cb.addItems(self.get_entries())

        self.set_btn = QtWidgets.QPushButton("Set")
        self.set_and_close_btn = QtWidgets.QPushButton("Set and Close")
        self.cancel_btn = QtWidgets.QPushButton("Cancel")

    def create_layout(self):
        form_layout = QtWidgets.QFormLayout()
        form_layout.addRow("Show_name: ", self.show_name_cb)
        form_layout.addRow("Branch: ", self.branch_cb)
        form_layout.addRow("Category", self.category_cb)
        form_layout.addRow("Entry", self.entry_cb)

        buttons_layout = QtWidgets.QHBoxLayout()
        buttons_layout.addStretch()
        buttons_layout.addWidget(self.set_btn)
        buttons_layout.addWidget(self.set_and_close_btn)
        buttons_layout.addWidget(self.cancel_btn)

        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.addLayout(form_layout)
        main_layout.addLayout(buttons_layout)

    def create_connections(self):
        self.show_name_cb.activated.connect(self.comboBox_shows)
        self.show_name_cb.activated.connect(self.refresh_combo)
        # self.branch_cb.activated.connect()
        self.category_cb.activated.connect(self.comboBox_seq)
        self.set_btn.clicked.connect(self.db_commit)
        self.set_and_close_btn.clicked.connect(self.db_commit_close)
        self.cancel_btn.clicked.connect(self.close)

    def comboBox_shows(self):
        text = self.show_name_cb.currentText()
        return text

    def comboBox_seq(self):
        seq_text = self.category_cb.currentText()
        return seq_text




    def refresh_combo(self):
        self.category_cb.clear()
        self.category_cb.addItems(self.get_shows_seq())

    def db_commit_close(self):
        self.db_commit()
        self.close()

    def db_commit(self):
        xac.create_shot(self.show_name_cb.currentText(),
                        self.category_cb.currentText(),
                        self.shot_name_le.text(),
                        self.frame_in_le.text(),
                        self.frame_out_le.text(),
                        self.preroll_le.text(),
                        self.handles_head_le.text(),
                        self.handles_tail_le.text(),
                        self.shot_status_cb.currentText(),
                        self.shot_render_res_x_le.text(),
                        self.shot_render_res_y_le.text(),
                        self.retime_cb.isChecked(),
                        self.repo_cb.isChecked())

    def get_shows(self):
        store_shows = []
        shows = xac.db_query("show", "show_name", show_type="vfx")
        for show in shows:
            store_shows.append(show)
        return store_shows

    def get_shows_seq(self):
        store_shows_seq = []
        sequences = xac.db_query("sequences", "seq_name", show_name=self.comboBox_shows())
        for seq in sequences:
            store_shows_seq.append(seq)
        return store_shows_seq

    def get_shows_asset_categories(self):
        store_assets_cat = []
        categories = xac.db_query("assets", "asset_category", show_name=self.comboBox_shows())
        for cat in categories:
            store_assets_cat.append(cat)
        return store_assets_cat

    def get_shows_assets(self):
        store_assets = []
        assets = xac.db_query("assets", "asset_name", show_name=self.comboBox_shows())
        for asset in assets:
            store_assets.append(asset)
        return store_assets

    def get_entries(self):
        pass





if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    try:
        create_shot.close()
        create_shot.deleteLater()
    except:
        pass
    create_shot = SetContextUI()
    create_shot.show()
    sys.exit(app.exec_())