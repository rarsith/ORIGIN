import sys
from PySide2 import QtWidgets

from xcg_data_base import xcg_db_actions as xac
from xcg_config import xcg_validation as xval

class CreateShotUI(QtWidgets.QDialog):

    def __init__(self, parent=None):
        super(CreateShotUI, self).__init__(parent)

        self.setWindowTitle("Create Shot")
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

        self.parent_seq_cb = QtWidgets.QComboBox()
        self.parent_seq_cb.addItems(self.get_shows_seq())

        self.shot_status_cb = QtWidgets.QComboBox()
        self.shot_status_cb.addItems(xval.VALID_TASK_STATUSES)

        self.shot_name_le = QtWidgets.QLineEdit()

        self.shot_definition_lb = QtWidgets.QLabel("-- Definition --")

        self.create_btn = QtWidgets.QPushButton("Create")
        self.create_and_close_btn = QtWidgets.QPushButton("Create and Close")
        self.cancel_btn = QtWidgets.QPushButton("Cancel")

    def create_layout(self):
        form_layout = QtWidgets.QFormLayout()
        form_layout.addRow("Show Name: ", self.show_name_cb)
        form_layout.addRow("Parent Seq", self.parent_seq_cb)
        form_layout.addRow("Shot Name: ", self.shot_name_le)
        form_layout.addRow("Shot Status: ", self.shot_status_cb)

        read_def = self.get_some()
        form_definition_layout = QtWidgets.QVBoxLayout()
        cnt = 0
        for each, val in sorted(read_def.items(), reverse=True):
            pair_attrib = QtWidgets.QHBoxLayout()
            pair_attrib.addWidget(QtWidgets.QLabel(str(each)))
            pair_attrib.addWidget(QtWidgets.QLabel(str(val)))
            form_definition_layout.addLayout(pair_attrib)
            cnt += 1



        form_def_layout = QtWidgets.QHBoxLayout()
        form_def_layout.addLayout(form_definition_layout)
        form_def_layout.addSpacing(120)


        buttons_layout = QtWidgets.QHBoxLayout()
        buttons_layout.addStretch()
        buttons_layout.addWidget(self.create_btn)
        buttons_layout.addWidget(self.create_and_close_btn)
        buttons_layout.addWidget(self.cancel_btn)

        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.addLayout(form_layout)
        main_layout.addSpacing(20)
        main_layout.addWidget(self.shot_definition_lb)
        main_layout.addLayout(form_def_layout)
        main_layout.addStretch()

        main_layout.addLayout(buttons_layout)

    def get_some(self):
        get = xac.get_entry_definition("Test", "sequences",  "VVV", '0150')
        return get


    def create_connections(self):
        self.show_name_cb.activated.connect(self.comboBox_shows)
        self.show_name_cb.activated.connect(self.refresh_combo)
        # self.show_name_cb.activated.connect(self.comboBox_seq)
        # self.parent_seq_cb.activated.connect(self.comboBox_seq)
        self.create_btn.clicked.connect(self.db_commit)
        self.create_and_close_btn.clicked.connect(self.db_commit_close)
        self.cancel_btn.clicked.connect(self.close)

    def get_default_definition(self):
        defaults = xval.DEFAULT_SHOT_DEFINITION
        return defaults

    def comboBox_shows(self):
        text = self.show_name_cb.currentText()
        return text

    def comboBox_seq(self):
        seq_text = self.parent_seq_cb.currentText()
        return seq_text

    def refresh_combo(self):
        self.parent_seq_cb.clear()
        self.parent_seq_cb.addItems(self.get_shows_seq())

    def get_cut_in_le(self):
        print ("need to do this")
        return "need to do this"

    def get_cut_out_le(self):
        print ("need to do this")
        return "need to do this"

    def get_res_x(self):
        print ("need to do this")
        return "need to do this"

    def get_res_y(self):
        print ("need to do this")
        return "need to do this"

    def get_full_range_out(self):
        print ("need to do this")
        return "need to do this"

    def get_full_range_in(self):
        print ("need to do this")
        return "need to do this"

    def db_commit_close(self):
        self.db_commit()
        self.close()

    def db_commit(self):
        xac.create_shot(self.show_name_cb.currentText(),
                        self.parent_seq_cb.currentText(),
                        self.shot_name_le.text(),
                        self.scene_frame_in_le.text(),
                        self.scene_frame_out_le.text(),
                        self.preroll_le.text(),
                        self.handles_head_le.text(),
                        self.handles_tail_le.text(),
                        self.shot_status_cb.currentText(),
                        self.shot_render_res_x_le.text(),
                        self.shot_render_res_y_le.text(),
                        self.retime_ckb.isChecked(),
                        self.repo_ckb.isChecked())
        self.shot_name_le.clear()

    def get_shows(self):
        shows = xac.get_all_active_shows()
        return shows

    def get_shows_seq(self):
        sequences = xac.get_show_sequences(self.comboBox_shows())
        return sequences






if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    try:
        create_shot.close()
        create_shot.deleteLater()
    except:
        pass
    create_shot = CreateShotUI()
    create_shot.show()
    sys.exit(app.exec_())