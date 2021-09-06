import sys
from PySide2 import QtWidgets

from origin_data_base import xcg_db_actions as xac
from origin_config import xcg_validation as xval

class CreateAssetUI(QtWidgets.QDialog):

    def __init__(self, parent=None):
        super(CreateAssetUI, self).__init__(parent)

        self.setWindowTitle("Create Asset")
        self.setMinimumSize(550, 650)
        self.setMaximumSize(550, 650)

        self.setMinimumHeight(900)
        self.setMaximumHeight(900)


        self.create_widgets()
        self.create_layout()
        self.create_connections()

    def create_widgets(self):
        self.show_name_cb = QtWidgets.QComboBox()
        self.show_name_cb.addItems(self.get_shows())

        self.category_cb = QtWidgets.QComboBox()
        self.category_cb.addItems(self.get_asset_categories())


        self.asset_type_cb = QtWidgets.QComboBox()



        self.asset_name_le = QtWidgets.QLineEdit()

        self.shot_status_cb = QtWidgets.QComboBox()
        self.shot_status_cb.addItems(xval.VALID_TASK_STATUSES)

        self.retime_cb = QtWidgets.QCheckBox()
        self.repo_cb = QtWidgets.QCheckBox()

        self.create_btn = QtWidgets.QPushButton("Create")
        self.create_and_close_btn = QtWidgets.QPushButton("Create and Close")
        self.cancel_btn = QtWidgets.QPushButton("Cancel")

    def create_layout(self):
        form_layout = QtWidgets.QFormLayout()
        form_layout.addRow("Show_name: ", self.show_name_cb)
        form_layout.addRow("Category", self.category_cb)
        form_layout.addRow("Asset Type", self.asset_type_cb)
        form_layout.addRow("Asset Name:", self.asset_name_le)
        form_layout.addRow("Asset Status: ", self.shot_status_cb)

        buttons_layout = QtWidgets.QHBoxLayout()
        buttons_layout.addStretch()
        buttons_layout.addWidget(self.create_btn)
        buttons_layout.addWidget(self.create_and_close_btn)
        buttons_layout.addWidget(self.cancel_btn)

        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.addLayout(form_layout)
        main_layout.addLayout(buttons_layout)

    def create_connections(self):
        self.show_name_cb.activated.connect(self.comboBox_shows)
        self.show_name_cb.activated.connect(self.refresh_combo)

        self.category_cb.activated.connect(self.comboBox_seq)
        self.create_btn.clicked.connect(self.db_commit)
        self.create_and_close_btn.clicked.connect(self.db_commit_close)
        self.cancel_btn.clicked.connect(self.close)

    def comboBox_shows(self):
        text = self.show_name_cb.currentText()
        return text

    def comboBox_seq(self):
        seq_text = self.category_cb.currentText()
        return seq_text

    def refresh_combo(self):
        self.category_cb.clear()
        self.category_cb.addItems(self.get_asset_categories())

    def db_commit_close(self):
        self.db_commit()
        self.close()

    def db_commit(self):
        xac.create_asset(self.show_name_cb.currentText(),
                         self.category_cb.currentText(),
                         self.asset_name_le.text(),
                         self.shot_status_cb.currentText())
        self.asset_name_le.clear()

    def get_shows(self):
        shows = xac.get_all_active_shows()
        return shows

    def get_asset_categories(self):
        assets_cat = xac.get_show_assets_categories(self.show_name_cb.currentText())
        return assets_cat






if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    try:
        create_asset.close()
        create_asset.deleteLater()
    except:
        pass
    create_asset = CreateAssetUI()
    create_asset.show()
    sys.exit(app.exec_())