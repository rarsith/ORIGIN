import sys
from PySide2 import QtWidgets
from PySide2 import QtGui
from origin_data_base import xcg_db_actions as xac


class CreateShowCategoryUI(QtWidgets.QDialog):

    def __init__(self, parent=None):
        super(CreateShowCategoryUI, self).__init__(parent)

        self.setWindowTitle("Create Show Category")
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

        self.category_name_le = QtWidgets.QLineEdit()

        self.create_btn = QtWidgets.QPushButton("Create")
        self.create_and_close_btn = QtWidgets.QPushButton("Create and Close")
        self.cancel_btn = QtWidgets.QPushButton("Cancel")

    def create_layout(self):
        form_layout = QtWidgets.QFormLayout()
        form_layout.addRow("Show_name: ", self.show_name_cb)
        form_layout.addRow("Show Category Name:", self.category_name_le)

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
        self.create_btn.clicked.connect(self.db_commit)
        self.create_and_close_btn.clicked.connect(self.db_commit_close)
        self.cancel_btn.clicked.connect(self.close)

    def comboBox_shows(self):
        text = self.show_name_cb.currentText()
        return text

    def db_commit_close(self):
        self.db_commit()
        self.close()

    def db_commit(self):
        xac.create_show_branch(self.show_name_cb.currentText(), self.category_name_le.text())
        self.category_name_le.clear()

    def get_shows(self):
        shows = xac.get_all_active_shows()
        return shows


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    app.setStyle(QtWidgets.QStyleFactory.create("fusion"))

    dark_palette = QtGui.QPalette()
    dark_palette.setColor(QtGui.QPalette.Window, QtGui.QColor(45,45,45))
    dark_palette.setColor(QtGui.QPalette.WindowText, QtGui.QColor(208, 208, 208))



    create_shot = CreateShowCategoryUI()
    create_shot.show()

    sys.exit(app.exec_())
