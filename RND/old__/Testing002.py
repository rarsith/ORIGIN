import sys
from PySide2 import QtWidgets

from xcg_data_base import xcg_db_actions as xac
from xcg_config import xcg_validation as xval

class CreateShotUI(QtWidgets.QDialog):

    CREATE_ELEMENTS = {u'Test01:':u'False', u'Test02:':u'GG', 'Test03:':'ZZ', 'Test04:':'QQ', 'Test05:':'DD', 'Test06:':'dde', 'Test07:':'DEW'}

    def __init__(self, parent=None):
        super(CreateShotUI, self).__init__(parent)

        self.setWindowTitle("Properties")
        self.setMinimumSize(370, 300)


        self.create_widgets()
        self.create_layout()
        self.create_connections()

    def create_widgets(self):
        self.show_name_cb = QtWidgets.QComboBox()
        self.show_name_cb.addItems(self.get_shows())

        # self.properties_values_lb = QtWidgets.QLabel("")


        self.parent_seq_cb = QtWidgets.QComboBox()
        self.parent_seq_cb.addItems(self.get_shows_seq())

        self.shot_name_le = QtWidgets.QLineEdit()
        self.frame_in_le = QtWidgets.QLineEdit("1001")
        self.frame_out_le = QtWidgets.QLineEdit("1001")
        self.preroll_le = QtWidgets.QLineEdit("10")
        self.handles_head_le = QtWidgets.QLineEdit("8")
        self.handles_tail_le = QtWidgets.QLineEdit("8")

        self.shot_status_cb = QtWidgets.QComboBox()
        self.shot_status_cb.addItems(xval.VALID_TASK_STATUSES)

        self.shot_render_res_x_le = QtWidgets.QLineEdit("default_x")
        self.shot_render_res_y_le = QtWidgets.QLineEdit("default_y")

        self.retime_ckb = QtWidgets.QCheckBox()
        self.repo_ckb = QtWidgets.QCheckBox()

        self.create_btn = QtWidgets.QPushButton("Create")
        self.create_and_close_btn = QtWidgets.QPushButton("Create and Close")
        self.cancel_btn = QtWidgets.QPushButton("Cancel")

    def create_layout(self):
        form_layout = QtWidgets.QFormLayout()
        form_layout.addRow("Show_name: ", self.show_name_cb)



        form_layout.addRow("Parent Seq", self.parent_seq_cb)
        form_layout.addRow("Shot Name: ", self.shot_name_le)
        form_layout.addRow("Shot Status: ", self.shot_status_cb)

        form_layout.addRow("Frame In: ", self.frame_in_le)
        form_layout.addRow("Frame Out: ", self.frame_out_le)
        form_layout.addRow("Preroll: ", self.preroll_le)
        form_layout.addRow("Handles Head: ", self.handles_head_le)
        form_layout.addRow("Handles Tail: ", self.handles_tail_le)

        resolution_layout = QtWidgets.QHBoxLayout()
        resolution_layout.addWidget(self.shot_render_res_x_le)
        resolution_layout.addWidget(self.shot_render_res_y_le)

        form_layout.addRow("Render Resolution: ", resolution_layout)
        form_layout.addRow("Retime: ", self.retime_ckb)
        form_layout.addRow("Repo: ", self.repo_ckb)

        buttons_layout = QtWidgets.QHBoxLayout()
        buttons_layout.addStretch()
        buttons_layout.addWidget(self.create_btn)
        buttons_layout.addWidget(self.create_and_close_btn)
        buttons_layout.addWidget(self.cancel_btn)

        self.top_layout = QtWidgets.QVBoxLayout()

        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.addLayout(self.top_layout)
        main_layout.addLayout(form_layout)

        main_layout.addLayout(buttons_layout)

        for k, v in self.CREATE_ELEMENTS.iteritems():
            print k
            self.create_label = QtWidgets.QLabel(k)
            self.create_content = QtWidgets.QLabel(v)
            self.top_layout.addWidget(self.create_label)
            self.top_layout.addWidget(self.create_content)




    def create_connections(self):
        self.show_name_cb.activated.connect(self.comboBox_shows)
        self.show_name_cb.activated.connect(self.refresh_combo)
        # self.show_name_cb.activated.connect(self.comboBox_seq)
        # self.parent_seq_cb.activated.connect(self.comboBox_seq)
        self.create_btn.clicked.connect(self.db_commit)
        self.create_and_close_btn.clicked.connect(self.db_commit_close)
        self.cancel_btn.clicked.connect(self.close)

    def comboBox_shows(self):
        text = self.show_name_cb.currentText()
        return text

    def comboBox_seq(self):
        seq_text = self.parent_seq_cb.currentText()
        return seq_text

    def refresh_combo(self):
        self.parent_seq_cb.clear()
        self.parent_seq_cb.addItems(self.get_shows_seq())

    def db_commit_close(self):
        self.db_commit()
        self.close()

    def db_commit(self):
        xac.create_shot(self.show_name_cb.currentText(),
                        self.parent_seq_cb.currentText(),
                        self.shot_name_le.text(),
                        self.frame_in_le.text(),
                        self.frame_out_le.text(),
                        self.preroll_le.text(),
                        self.handles_head_le.text(),
                        self.handles_tail_le.text(),
                        self.shot_status_cb.currentText(),
                        self.shot_render_res_x_le.text(),
                        self.shot_render_res_y_le.text(),
                        self.retime_ckb.isChecked(),
                        self.repo_ckb.isChecked())

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