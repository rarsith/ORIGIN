import sys
from PySide2 import QtWidgets, QtGui, QtCore


class LayerObject(object):

    def __init__(self, **kwargs):
        self.name = kwargs.get('name', '')
        self.enabled = kwargs.get('enabled', False)


class LayerWidget(QtWidgets.QWidget):

    def __init__(self, layer):
        super(LayerWidget, self).__init__()
        self.resize(400, 50)

        # controls
        self.ui_enabled = QtWidgets.QCheckBox()
        self.ui_layername = QtWidgets.QLabel()
        self.ui_items = QtWidgets.QComboBox()
        self.ui_items.addItems(['Color', 'Saturation', 'Blend'])

        main_layout = QtWidgets.QHBoxLayout()
        main_layout.addWidget(self.ui_layername)
        main_layout.addWidget(self.ui_items)
        main_layout.addStretch()
        main_layout.addWidget(self.ui_enabled)
        self.setLayout(main_layout)

        # construct
        self._layer = None
        self.layer = layer


    # properties
    @property
    def layer(self):
        return self._layer

    @layer.setter
    def layer(self, value):
        self._layer== value
        self.ui_layername.setText(value.name)
        self.ui_enabled.setChecked(value.enabled)


class LayerManager(QtWidgets.QWidget):
    def __init__(self):
        super(LayerManager, self).__init__()
        self.resize(400, 300)

        # controls
        self.ui_scroll = QtWidgets.QWidget()
        self.ui_scroll_layout = QtWidgets.QVBoxLayout()
        self.ui_scroll.setLayout(self.ui_scroll_layout)

        self.ui_scroll_area = QtWidgets.QScrollArea()
        self.ui_scroll_area.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.ui_scroll_area.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.ui_scroll_area.setWidgetResizable(True)
        self.ui_scroll_area.setWidget(self.ui_scroll)

        main_layout = QtWidgets.QHBoxLayout()
        main_layout.addWidget(self.ui_scroll_area)
        self.setLayout(main_layout)


        self.add_layers()

    def add_layers(self):
        layers = [
            LayerObject(name='Layer001', enabled=False),
            LayerObject(name='Layer002', enabled=False),
            LayerObject(name='Layer003', enabled=True),
            LayerObject(name='Layer004', enabled=False),
            LayerObject(name='Layer005', enabled=True),
            LayerObject(name='Layer006', enabled=False),
            LayerObject(name='Layer007', enabled=False),
            LayerObject(name='Layer008', enabled=True),
            LayerObject(name='Layer009', enabled=False),
            LayerObject(name='Layer010', enabled=True)
        ]

        for x in layers:
            widget = LayerWidget(layer=x)
            self.ui_scroll_layout.addWidget(widget)


def main():
    app = QtWidgets.QApplication(sys.argv)
    ex = LayerManager()
    ex.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()