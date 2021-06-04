import xcg_database_custom_widgets.xcg_project_tree_viewer_core
reload (xcg_database_custom_widgets.xcg_project_tree_viewer_core)



if __name__ == "__main__":
    test_dialog = xcg_database_custom_widgets.xcg_project_tree_viewer_core.ProjectTreeViewerCore()
    test_dialog.show_name = os.environ.get('XCG_PROJECT')
    test_dialog.branch_name = os.environ.get('XCG_PROJECT_BRANCH')
    test_dialog.category_name = os.environ.get('XCG_PROJECT_CATEGORY')
    test_dialog.entry_name = os.environ.get('XCG_PROJECT_ENTITY')
    test_dialog.set_show_to()
    test_dialog.show()