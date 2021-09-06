import os

# try:
#     xchange_root =  os.environ["XCHANGE_ROOT"]
# except:
#     print ("XCHANGE_ROOT environment variable not correctly configured")

# else:
#     import sys
#     if not xchange_root in sys.path:
#         sys.path.append(xchange_root)


from origin_database_custom_widgets.xcg_project_tree_viewer_core import ProjectTreeViewerCore



if __name__ == "__main__":
    create_shot = ProjectTreeViewerCore()
    create_shot.show()
