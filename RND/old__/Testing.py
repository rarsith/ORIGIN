import datetime
import json
import sys
from PySide2 import QtCore, QtGui, QtWidgets


class AssetViewer(QtWidgets.QWidget):
    ASSET_DIR_PATH = "/Users/arsithra/Downloads/python_in_production_project_files/12-python_in_production-a_practical_json_example_part_2"
    JSON_FILE_NAME = "assets.json"

    IMAGE_WIDTH = 400
    IMAGE_HEIGHT = IMAGE_WIDTH / 1.77778

    def __init__(self):
        super(AssetViewer, self).__init__(parent=None)

        self.setWindowTitle("Asset Viewer")
        self.setMinimumSize(400, 300)

        self.json_file_path = "{0}/{1}".format(self.ASSET_DIR_PATH, self.JSON_FILE_NAME)

        self.create_widgets()
        self.create_layout()
        self.create_connections()

        self.set_edit_enabled(False)

        self.load_assets_from_json()

    def create_widgets(self):
        self.asset_list_label = QtWidgets.QLabel("Asset Code:")
        self.asset_list_cmb = QtWidgets.QComboBox()

        self.preview_image_label = QtWidgets.QLabel()
        self.preview_image_label.setFixedHeight(self.IMAGE_HEIGHT)

        self.name_le = QtWidgets.QLineEdit()
        self.description_plaintext = QtWidgets.QPlainTextEdit()
        self.description_plaintext.setFixedHeight(100)
        self.creator_le = QtWidgets.QLineEdit()
        self.created_date_le = QtWidgets.QLineEdit()
        self.modified_date_le = QtWidgets.QLineEdit()

        self.edit_button = QtWidgets.QPushButton("Edit")
        self.save_button = QtWidgets.QPushButton("Save")
        self.cancel_button = QtWidgets.QPushButton("Cancel")

    def create_layout(self):
        asset_list_layout = QtWidgets.QHBoxLayout()
        asset_list_layout.addStretch()
        asset_list_layout.addWidget(self.asset_list_label)
        asset_list_layout.addWidget(self.asset_list_cmb)

        details_layout = QtWidgets.QFormLayout()
        details_layout.addRow("Name:", self.name_le)
        details_layout.addRow("Description:", self.description_plaintext)
        details_layout.addRow("Creator:", self.creator_le)
        details_layout.addRow("Created:", self.created_date_le)
        details_layout.addRow("Modified:", self.modified_date_le)

        button_layout = QtWidgets.QHBoxLayout()
        button_layout.addStretch()
        button_layout.addWidget(self.edit_button)
        button_layout.addWidget(self.save_button)
        button_layout.addWidget(self.cancel_button)

        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.setContentsMargins(2, 2, 2, 2)
        main_layout.addLayout(asset_list_layout)
        main_layout.addWidget(self.preview_image_label)
        main_layout.addLayout(details_layout)
        main_layout.addLayout(button_layout)

    def create_connections(self):
        self.asset_list_cmb.currentTextChanged.connect(self.refresh_asset_details)

        self.edit_button.clicked.connect(self.edit_asset_details)
        self.save_button.clicked.connect(self.save_asset_details)
        self.cancel_button.clicked.connect(self.cancel_edit)

    def set_edit_enabled(self, enabled):
        read_only = not enabled

        self.name_le.setReadOnly(read_only)
        self.description_plaintext.setReadOnly(read_only)
        if read_only:
            self.creator_le.setReadOnly(read_only)
            self.created_date_le.setReadOnly(read_only)
            self.modified_date_le.setReadOnly(read_only)

        self.edit_button.setVisible(read_only)
        self.save_button.setHidden(read_only)
        self.cancel_button.setHidden(read_only)

    def set_preview_image(self, file_name):
        image_path = "{0}/{1}".format(self.ASSET_DIR_PATH, file_name)

        file_info = QtCore.QFileInfo(image_path)
        if file_info.exists():
            image = QtGui.QImage(image_path)
            image = image.scaled(self.preview_image_label.width(), self.preview_image_label.height(),
                                 QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)
            pixmap = QtGui.QPixmap()
            pixmap.convertFromImage(image)

        else:
            pixmap = QtGui.QPixmap(self.preview_image_label.size())
            pixmap.fill(QtCore.Qt.transparent)

        self.preview_image_label.setPixmap(pixmap)

    def load_assets_from_json(self):
        with open(self.json_file_path, "r") as file_for_read:
            self.assets = json.load(file_for_read)

        for asset_code in self.assets.keys():
            self.asset_list_cmb.addItem(asset_code)

    def save_assets_to_json(self):
        with open(self.json_file_path, "w") as file_for_write:
            json.dump(self.assets, file_for_write, indent=4)

    def refresh_asset_details(self):
        asset_code = self.asset_list_cmb.currentText()

        current_asset = self.assets[asset_code]

        self.name_le.setText(current_asset["name"])
        self.description_plaintext.setPlainText(current_asset["description"])
        self.creator_le.setText(current_asset["creator"])
        self.created_date_le.setText(current_asset["created"])
        self.modified_date_le.setText(current_asset["modified"])

        self.set_preview_image(current_asset["image_path"])

    def edit_asset_details(self):
        self.set_edit_enabled(True)

    def save_asset_details(self):
        self.set_edit_enabled(False)

        modified = datetime.datetime.now()
        self.modified_date_le.setText(modified.strftime("%Y/%m/%d %H:%M:%S"))

        asset_code = self.asset_list_cmb.currentText()

        current_asset = self.assets[asset_code]
        current_asset["name"] = self.name_le.text()
        current_asset["description"] = self.description_plaintext.toPlainText()
        current_asset["modified"] = self.modified_date_le.text()

        self.save_assets_to_json()

    def cancel_edit(self):
        self.set_edit_enabled(False)

        self.refresh_asset_details()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    window = AssetViewer()
    window.show()

    app.exec_()

