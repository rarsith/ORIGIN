from PySide2 import QtCore, QtGui, QtWidgets

def fill_model_from_json(parent, d):
    if isinstance(d, dict):
        for k, v in d.items():
            child = QtGui.QStandardItem(str(k))
            parent.appendRow(child)
            fill_model_from_json(child, v)
    elif isinstance(d, list):
        for v in d:
            fill_model_from_json(parent, v)
    else:
        parent.appendRow(QtGui.QStandardItem(str(d)))

def fill_dict_from_model(parent_index, d):
    v = {}
    for i in range(model.rowCount(parent_index)):
        ix = model.index(i, 0, parent_index)
        fill_dict_from_model(ix, v)
    d[parent_index.data()] = v

def model_to_dict(model):
    d = dict()
    for i in range(model.rowCount()):
        ix = model.index(i, 0)
        fill_dict_from_model(ix, d)
    return d

if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    tree = QtWidgets.QTreeView()
    model = QtGui.QStandardItemModel()
    data = {u'ZUHU': {u'Level01': {}}, u'assets': {u'characters': {u'jukka': {}}, u'environments': {u'dongeon': {}}, u'props': {u'knife': {}}}, u'sequences': {u'DDR': {u'0010': {}}}}
    fill_model_from_json(model.invisibleRootItem(), data)
    tree.setModel(model)
    tree.expandAll()
    tree.resize(360, 480)
    tree.show()
    d = model_to_dict(model)
    assert(d == data)
    print(d)
    sys.exit(app.exec_())