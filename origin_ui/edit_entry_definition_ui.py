
import sys
from PySide2 import QtWidgets, QtCore

from origin_data_base import xcg_db_actions as xac
from origin_config import xcg_validation as xval

class EditEntryDefinitionsUI(QtWidgets.QDialog):

    def __init__(self, parent=None):
        super(EditEntryDefinitionsUI, self).__init__(parent)

        self.setWindowTitle("Edit Entry Definitions")
        self.setMinimumSize(550, 650)
        self.setMaximumSize(550, 650)

        self.setMinimumHeight(900)
        self.setMaximumHeight(900)


        self.create_widgets()
        self.create_layout()
        self.create_connections()

        self.shot_definition_UI()
        self.asset_definition_UI()

    def create_widgets(self):
        self.show_name_cb = QtWidgets.QComboBox()
        self.show_name_cb.addItems(self.get_shows())
        self.show_branch_cb = QtWidgets.QComboBox()
        self.show_branch_cb.addItems(self.get_show_branches())
        self.category_cb = QtWidgets.QComboBox()
        self.category_cb.addItems(self.get_categories())
        self.entry_name_cb = QtWidgets.QComboBox()
        self.entry_name_cb.addItems(self.get_entries())

        # Building the Stack menu
        # Adding an empty stack....might have to remove

        # Build the Asset Definition menu
        self.assets_definition_properties_stack = QtWidgets.QWidget()
        self.asset_lod_le = QtWidgets.QLineEdit()
        self.asset_assembly_ckb = QtWidgets.QCheckBox()

        # Build the Shot Definition menu
        self.shots_definition_properties_stack = QtWidgets.QWidget()
        self.shot_type_cb = QtWidgets.QComboBox()
        self.shot_type_cb.addItems(xval.VALID_SHOTS_TYPES)
        self.preroll_le = QtWidgets.QLineEdit("0")
        self.frame_in_le = QtWidgets.QLineEdit("0")
        self.frame_out_le = QtWidgets.QLineEdit("0")
        self.full_range_in_lb = QtWidgets.QLabel("0")
        self.full_range_out_lb = QtWidgets.QLabel("0")
        self.handles_head_le = QtWidgets.QLineEdit("0")
        self.handles_tail_le = QtWidgets.QLineEdit("0")
        self.edit_cut_in_lb = QtWidgets.QLabel("0")
        self.edit_cut_out_lb = QtWidgets.QLabel("0")
        self.frame_rate_le = QtWidgets.QLineEdit("0")
        self.motion_blur_high_le = QtWidgets.QLineEdit()
        self.motion_blur_low_le = QtWidgets.QLineEdit()
        self.render_resolution_x_le = QtWidgets.QLineEdit()
        self.render_resolution_y_le = QtWidgets.QLineEdit()

        self.stacked_properties_wdg = QtWidgets.QStackedWidget()
        self.stacked_properties_wdg.addWidget(self.assets_definition_properties_stack)
        self.stacked_properties_wdg.addWidget(self.shots_definition_properties_stack)

        self.separator_top_lb = QtWidgets.QLabel("")
        self.entry_definition_lb =  QtWidgets.QLabel("-- Definition --")
        self.separator_bottom_lb = QtWidgets.QLabel("")

        self.switch_stack()
        self.populate_shot_definitions()
        self.populate_asset_definitions()

        self.shot_commit_btn = QtWidgets.QPushButton("Commit")
        self.shot_commit_and_close_btn = QtWidgets.QPushButton("Commit and Close")

        self.asset_commit_btn = QtWidgets.QPushButton("Commit")
        self.asset_commit_and_close_btn = QtWidgets.QPushButton("Commit and Close")

        self.cancel_btn = QtWidgets.QPushButton("Close")

    def create_layout(self):
        form_layout = QtWidgets.QFormLayout()
        form_layout.addRow("Show_name ", self.show_name_cb)
        form_layout.addRow("Show Branch", self.show_branch_cb)
        form_layout.addRow("Category", self.category_cb)
        form_layout.addRow("Entry Name", self.entry_name_cb)
        form_layout.setSpacing(5)
        form_layout.setFormAlignment(QtCore.Qt.AlignLeft)
        form_layout.setLabelAlignment(QtCore.Qt.AlignRight)

        separators_layout = QtWidgets.QFormLayout()
        separators_layout.addWidget(self.separator_top_lb)
        separators_layout.addWidget(self.entry_definition_lb)
        separators_layout.addWidget(self.separator_bottom_lb)

        definition_stack_layout = QtWidgets.QHBoxLayout()
        definition_stack_layout.addWidget(self.stacked_properties_wdg)

        buttons_layout = QtWidgets.QHBoxLayout()
        buttons_layout.addStretch()
        buttons_layout.addWidget(self.cancel_btn)

        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.addLayout(form_layout)
        main_layout.addLayout(separators_layout)
        main_layout.addLayout(definition_stack_layout)
        main_layout.addStretch()
        main_layout.addLayout(buttons_layout)

    def create_connections(self):
        self.show_name_cb.currentIndexChanged.connect(self.comboBox_shows)
        self.show_name_cb.currentIndexChanged.connect(self.refresh_combo)
        self.show_name_cb.currentIndexChanged.connect(self.populate_show_branches)
        self.show_name_cb.currentIndexChanged.connect(self.populate_categories)
        self.show_name_cb.currentIndexChanged.connect(self.populate_entries)

        self.show_branch_cb.currentIndexChanged.connect(self.comboBox_show_branches)
        self.show_branch_cb.currentIndexChanged.connect(self.populate_categories)
        self.show_branch_cb.currentIndexChanged.connect(self.populate_entries)
        self.show_branch_cb.currentIndexChanged.connect(self.switch_stack)
        self.show_branch_cb.currentIndexChanged.connect(self.populate_shot_definitions)
        self.show_branch_cb.currentIndexChanged.connect(self.populate_asset_definitions)

        self.category_cb.currentIndexChanged.connect(self.comboBox_categories)
        self.category_cb.currentIndexChanged.connect(self.populate_entries)
        self.category_cb.currentIndexChanged.connect(self.switch_stack)
        self.category_cb.currentIndexChanged.connect(self.populate_shot_definitions)
        self.category_cb.currentIndexChanged.connect(self.populate_asset_definitions)

        self.entry_name_cb.currentIndexChanged.connect(self.comboBox_entries)
        self.entry_name_cb.currentIndexChanged.connect(self.switch_stack)
        self.entry_name_cb.currentIndexChanged.connect(self.populate_shot_definitions)
        self.entry_name_cb.currentIndexChanged.connect(self.populate_asset_definitions)

        self.frame_in_le.textChanged[str].connect(self.compute_cut_in_le)
        self.handles_head_le.textChanged[str].connect(self.compute_cut_in_le)

        self.frame_out_le.textChanged[str].connect(self.compute_cut_out_le)
        self.handles_tail_le.textChanged[str].connect(self.compute_cut_out_le)


        self.shot_commit_btn.clicked.connect(self.db_commit)
        self.shot_commit_and_close_btn.clicked.connect(self.db_commit_close)

        self.asset_commit_btn.clicked.connect(self.db_asset_commit)
        self.asset_commit_and_close_btn.clicked.connect(self.db_asset_commit_close)

        self.cancel_btn.clicked.connect(self.close)

    def comboBox_shows(self):
        text = self.show_name_cb.currentText()
        return text

    def comboBox_show_branches(self):
        show_branch_text = self.show_branch_cb.currentText()
        return show_branch_text

    def comboBox_categories(self):
        category_text = self.category_cb.currentText()
        return category_text

    def comboBox_entries(self):
        entry_text = self.entry_name_cb.currentText()
        return entry_text

    def get_show_branches(self):
        show_branches = xac.get_show_branches_structure(self.show_name_cb.currentText())
        return show_branches

    def get_categories(self):
        sequences = xac.get_sub_branches(self.show_name_cb.currentText(), self.show_branch_cb.currentText())
        print (sequences)
        return sequences

    def get_entries(self):
        entries = xac.get_sub_branches_content(self.show_name_cb.currentText(), self.show_branch_cb.currentText(), self.category_cb.currentText())
        print (entries)
        return entries

    def refresh_combo(self):
        self.parent_seq_cb.clear()
        self.parent_seq_cb.addItems(self.get_shows_seq())

    def populate_show_branches(self):
        self.show_branch_cb.clear()
        self.show_branch_cb.addItems(self.get_show_branches())

    def populate_categories(self):
        self.category_cb.clear()
        self.category_cb.addItems(self.get_categories())

    def populate_entries(self):
        self.entry_name_cb.clear()
        self.entry_name_cb.addItems(self.get_entries())

    def populate_shot_definitions(self):
        self.shot_type_cb.setCurrentText(xac.get_definition_element(self.show_name_cb.currentText(), self.show_branch_cb.currentText(), self.category_cb.currentText(), self.entry_name_cb.currentText(), "shot_type"))
        self.preroll_le.setText(xac.get_definition_element(self.show_name_cb.currentText(), self.show_branch_cb.currentText(), self.category_cb.currentText(), self.entry_name_cb.currentText(), "preroll"))
        self.frame_in_le.setText(xac.get_definition_element(self.show_name_cb.currentText(), self.show_branch_cb.currentText(), self.category_cb.currentText(), self.entry_name_cb.currentText(), "frame_in"))
        self.frame_out_le.setText(xac.get_definition_element(self.show_name_cb.currentText(), self.show_branch_cb.currentText(), self.category_cb.currentText(), self.entry_name_cb.currentText(), "frame_out"))
        self.handles_head_le.setText(xac.get_definition_element(self.show_name_cb.currentText(), self.show_branch_cb.currentText(), self.category_cb.currentText(), self.entry_name_cb.currentText(), "handles_head"))
        self.handles_tail_le.setText(xac.get_definition_element(self.show_name_cb.currentText(), self.show_branch_cb.currentText(), self.category_cb.currentText(), self.entry_name_cb.currentText(), "handles_tail"))
        self.full_range_in_lb.setText(xac.get_definition_element(self.show_name_cb.currentText(), self.show_branch_cb.currentText(), self.category_cb.currentText(), self.entry_name_cb.currentText(), "full_range_in"))
        self.full_range_out_lb.setText(xac.get_definition_element(self.show_name_cb.currentText(), self.show_branch_cb.currentText(), self.category_cb.currentText(), self.entry_name_cb.currentText(), "full_range_out"))
        self.edit_cut_in_lb.setText(xac.get_definition_element(self.show_name_cb.currentText(), self.show_branch_cb.currentText(), self.category_cb.currentText(), self.entry_name_cb.currentText(), "cut_in"))
        self.edit_cut_out_lb.setText(xac.get_definition_element(self.show_name_cb.currentText(), self.show_branch_cb.currentText(), self.category_cb.currentText(), self.entry_name_cb.currentText(), "cut_out"))
        self.frame_rate_le.setText(xac.get_definition_element(self.show_name_cb.currentText(), self.show_branch_cb.currentText(), self.category_cb.currentText(), self.entry_name_cb.currentText(), "frame_rate"))
        self.motion_blur_high_le.setText(str(xac.get_definition_element(self.show_name_cb.currentText(), self.show_branch_cb.currentText(), self.category_cb.currentText(), self.entry_name_cb.currentText(), "motion_blur_high")))
        self.motion_blur_low_le.setText(str(xac.get_definition_element(self.show_name_cb.currentText(), self.show_branch_cb.currentText(), self.category_cb.currentText(), self.entry_name_cb.currentText(), "motion_blur_low")))
        self.render_resolution_x_le.setText(xac.get_definition_element(self.show_name_cb.currentText(), self.show_branch_cb.currentText(), self.category_cb.currentText(), self.entry_name_cb.currentText(), "res_x"))
        self.render_resolution_y_le.setText(xac.get_definition_element(self.show_name_cb.currentText(), self.show_branch_cb.currentText(), self.category_cb.currentText(), self.entry_name_cb.currentText(), "res_y"))

    def populate_asset_definitions(self):
        self.asset_lod_le.setText(xac.get_definition_element(self.show_name_cb.currentText(), self.show_branch_cb.currentText(), self.category_cb.currentText(), self.entry_name_cb.currentText(), "asset_lod"))
        self.asset_assembly_ckb.setChecked(bool(xac.get_definition_element(self.show_name_cb.currentText(), self.show_branch_cb.currentText(), self.category_cb.currentText(), self.entry_name_cb.currentText(), "assembly")))

    def compute_cut_in_le(self):
        try:
            get_frame_in = self.frame_in_le.text()
            get_handles_head = self.handles_head_le.text()
            calculate_cut_in = int(get_frame_in) + int(get_handles_head)
            self.edit_cut_in_lb.setText(str(calculate_cut_in))
        except:
            pass

    def compute_cut_out_le(self):
        try:
            get_frame_out = self.frame_out_le.text()
            get_handles_tail = self.handles_tail_le.text()
            calculate_cut_out = int(get_frame_out) - int(get_handles_tail)
            self.edit_cut_out_lb.setText(str(calculate_cut_out))
        except:
            pass

    def compute_shot_definition(self):
        shot_definition = { 'full_range_in':self.full_range_in_lb.text(),
                            'full_range_out':self.full_range_out_lb.text(),
                            'frame_in': self.frame_in_le.text(),
                            'frame_out': self.frame_out_le.text(),
                            'handles_head': self.handles_head_le.text(),
                            'handles_tail': self.handles_tail_le.text(),
                            'preroll': self.preroll_le.text(),
                            'shot_type': self.shot_type_cb.currentText(),
                            'cut_in':self.edit_cut_in_lb.text(),
                            'cut_out':self.edit_cut_out_lb.text(),
                            'frame_rate': self.frame_rate_le.text(),
                            'motion_blur_high': self.motion_blur_high_le.text(),
                            'motion_blur_low': self.motion_blur_low_le.text(),
                            'res_x': self.render_resolution_x_le.text(),
                            'res_y': self.render_resolution_y_le.text()}

        return shot_definition

    def compute_asset_definition(self):
        asset_definition = {"asset_lod":self.asset_lod_le.text(),
                            "assembly":self.asset_assembly_ckb.isChecked()}

        return asset_definition

    def db_commit_close(self):
        self.db_commit()
        self.close()

    def db_commit(self):
        xac.update_entry_definition(self.show_name_cb.currentText(),
                                    self.show_branch_cb.currentText(),
                                    self.category_cb.currentText(),
                                    self.entry_name_cb.currentText(),
                                    definition=self.compute_shot_definition())

    def db_asset_commit_close(self):
        self.db_asset_commit()
        self.close()

    def db_asset_commit(self):
        xac.update_entry_definition(self.show_name_cb.currentText(),
                                    self.show_branch_cb.currentText(),
                                    self.category_cb.currentText(),
                                    self.entry_name_cb.currentText(),
                                    definition=self.compute_asset_definition())

    def get_shows(self):
        shows = xac.get_all_active_shows()
        return shows

    def get_shows_seq(self):
        sequences = xac.get_show_sequences(self.comboBox_shows())
        return sequences

    def asset_definition_UI(self):
        buttons_layout = QtWidgets.QHBoxLayout()
        buttons_layout.addWidget(self.asset_commit_btn)
        buttons_layout.addWidget(self.asset_commit_and_close_btn)

        labels_layout = QtWidgets.QFormLayout()
        labels_layout.addRow("Asset LOD ", self.asset_lod_le)
        labels_layout.addRow("Assembly ", self.asset_assembly_ckb)
        labels_layout.setFormAlignment(QtCore.Qt.AlignLeft)
        labels_layout.setLabelAlignment(QtCore.Qt.AlignLeft)
        labels_layout.setSpacing(5)


        main_layout = QtWidgets.QVBoxLayout()
        main_layout.addLayout(labels_layout)
        main_layout.addLayout(buttons_layout)
        main_layout.setSpacing(20)

        self.assets_definition_properties_stack.setLayout(main_layout)

    def shot_definition_UI(self):

        buttons_layout = QtWidgets.QHBoxLayout()
        buttons_layout.addWidget(self.shot_commit_btn)
        buttons_layout.addWidget(self.shot_commit_and_close_btn)


        render_resolution_layout = QtWidgets.QHBoxLayout()
        render_resolution_layout.addWidget(self.render_resolution_x_le)
        render_resolution_layout.addWidget(self.render_resolution_y_le)

        labels_layout = QtWidgets.QFormLayout()
        labels_layout.addRow("Shot Type ", self.shot_type_cb)
        labels_layout.addRow("Preroll", self.preroll_le)
        labels_layout.addRow("Frame In ", self.frame_in_le)
        labels_layout.addRow("Frame Out ", self.frame_out_le)
        labels_layout.addRow("Handles Head ", self.handles_head_le)
        labels_layout.addRow("Handles Tail ", self.handles_tail_le)
        labels_layout.addRow("Full Range In ", self.full_range_in_lb)
        labels_layout.addRow("Full Range Out ", self.full_range_out_lb)
        labels_layout.addRow("Edit Cut In ", self.edit_cut_in_lb)
        labels_layout.addRow("Edit Cut Out ", self.edit_cut_out_lb)
        labels_layout.addRow("Frame rate ", self.frame_rate_le)
        labels_layout.addRow("Motion Blur High ", self.motion_blur_high_le)
        labels_layout.addRow("Motion Blur Low ", self.motion_blur_low_le)
        labels_layout.addRow("Render Resolution ", render_resolution_layout)

        labels_layout.setFormAlignment(QtCore.Qt.AlignLeft)
        labels_layout.setLabelAlignment(QtCore.Qt.AlignLeft)
        labels_layout.setSpacing(5)

        main_layout = QtWidgets.QVBoxLayout()
        main_layout.addLayout(labels_layout)
        main_layout.addLayout(buttons_layout)
        main_layout.setSpacing(20)

        self.shots_definition_properties_stack.setLayout(main_layout)

    def switch_stack(self):
        switch_index = self.show_branch_cb.currentText()
        if switch_index == "assets":
            self.stacked_properties_wdg.setCurrentIndex(0)
        elif switch_index == "sequences":
            self.stacked_properties_wdg.setCurrentIndex(1)
        else:
            pass


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    create_shot = EditEntryDefinitionsUI()
    create_shot.show()
    sys.exit(app.exec_())