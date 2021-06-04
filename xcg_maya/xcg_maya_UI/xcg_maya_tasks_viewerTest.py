import xcg_database_custom_widgets.xcg_task_viewer_core
reload (xcg_database_custom_widgets.xcg_task_viewer_core)



if __name__ == "__main__":
    import os
    test_dialog = xcg_database_custom_widgets.xcg_task_viewer_core.TaskViewerCore()
    test_dialog.show_name = os.environ.get('XCG_PROJECT')
    test_dialog.branch_name = os.environ.get('XCG_PROJECT_BRANCH')
    test_dialog.category_name = os.environ.get('XCG_PROJECT_CATEGORY')
    test_dialog.entry_name = os.environ.get('XCG_PROJECT_ENTITY')
    test_dialog.populate_tasks()

    test_dialog.show()


