import origin_ui.origin_master_control_ui as omc

try:
    test_dialog.close()
    test_dialog.deleteLater()
except:
    pass

test_dialog = omc.MainUI()
test_dialog.show()