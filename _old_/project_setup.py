# global project file structure

import os
from xcg_config import xcg_validation as tsk
from RND import xcg_config_old_not_used as gld


def create_project(projName):


    try:
        os.makedirs(os.path.join(gld.PROJECTS_ROOT, projName))
        os.makedirs(gld.PROJ_ASSETS_PATH)
        os.makedirs(gld.PROJ_SEQ_PATH)
    except:
        pass
        print "Project %s already exists!" % projName

    for asset_type in tsk.assets_types:
        try:
            os.makedirs(os.path.join(gld.PROJ_ASSETS_PATH, asset_type))
        except:
            pass

    return projName

