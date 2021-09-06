import os


try:
    xchange_root =  os.environ["XCHANGE_ROOT"]
except:
    print "XCHANGE_ROOT environment variable not correctly configured"

else:
    import sys
    if not xchange_root in sys.path:
        sys.path.append(xchange_root)

import origin_database_custom_widgets.xcg_task_publishing_slots_core
reload(origin_database_custom_widgets.xcg_task_publishing_slots_core)

import origin_database_custom_widgets.xcg_task_imports_from_core
reload(origin_database_custom_widgets.xcg_task_imports_from_core)

from origin_database_custom_widgets.xcg_task_publishing_slots_core import PublishSlotsWidgetCore
from origin_database_custom_widgets.xcg_task_imports_from_core import TasksImportFromCore


from origin_data_base import xcg_db_connection as xcon
from origin_data_base import xcg_db_actions as xac



db = xcon.server.exchange
test_position = db.show_name

show_name = os.environ.get('XCG_PROJECT')
branch_name = os.environ.get('XCG_PROJECT_BRANCH')
category_name = os.environ.get('XCG_PROJECT_CATEGORY')
entry_name = os.environ.get('XCG_PROJECT_ENTITY')
task_name = os.environ.get('XCG_ENTITY_TASK')



test_dialog = PublishSlotsWidgetCore()
test_dialog.show_name = show_name
test_dialog.branch_name = branch_name
test_dialog.category_name = category_name
test_dialog.entry_name = entry_name
test_dialog.task_name = task_name
test_dialog.populate_main_widget()
test_dialog.show()



