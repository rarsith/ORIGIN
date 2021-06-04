import project_setup as ftr
import os
import json
from xcg_config import xcg_validation as tsk
from RND import xcg_config_old_not_used as gld
from _old_ import xcg_database_actions as progen


def write_json_data(proj_name, ):
    movies = [
        {"id": 1, "title": "TestMovie"},
        {"id": 2, "title": "CrapMovie"}
    ]

    data = json.dumps(movies)
    with open(os.path.join(gld.PROJECTS_ROOT, "movies.json"), "w") as file:
        file.write(data)


def entity_exists(name):
    if name not in gld.ACTIVE_PROJECT:
        print "%s needs to be created!" % name
    else:
        print "%s already exists!" % name
    return name


def active_project():
    active = gld.ACTIVE_PROJECT
    return active


def set_asset_path():
    pass


# createAsset (project=currentProject, type="character", name="lucius", tasks="all")
def create_asset(type, name):
    pass


# createSeq (project=currentProject, name="BGG")
def create_seq(proj_name, seq_name):
    get_seq_path = gld.PROJ_SEQ_PATH

    try:
        entity_path = os.listdir(get_seq_path)

    except:
        pass


    if not seq_name in entity_path:
        os.makedirs(os.path.join(gld.PROJ_SEQ_PATH, seq_name))
    else:
        print "sequence %s already exists!" % seq_name


# createShot (project=currentProject, seq="BGG", name="0010")
def create_shot(proj_name, seq, shot_name, frameIn="1001", frameOut="1002"):
    get_shot_path = os.path.join(gld.PROJ_SEQ_PATH, seq)

    try:
        entity_path = os.listdir(get_shot_path)

    except:
        pass

    if not shot_name in entity_path:
        os.makedirs(os.path.join(gld.PROJ_SEQ_PATH, seq, shot_name))
    else:
        print "shot %s, in seq %s, already exists!" % (shot_name, seq)


def create_shot_tasks(proj_name, seq, shot_name):
    # get_shot_path = os.path.join(gld.PROJ_SEQ_PATH, seq, shot_name)
    # entity_path = os.listdir(get_shot_path)

    try:
        for shot_task in tsk.shot_tasks:
            os.makedirs(os.path.join(gld.PROJ_SEQ_PATH, seq, shot_name, shot_task))

    except:
        print "tasks %s already exists!" % tsk.shot_tasks


# modeling publishing
# ------generic WIP file saving function
# saveWipFile (currentContext=current, savePath=os.path.join(currentContext, "wip", version)
    # assetName_userName_description_v####.mb
def save_wip():
    pass


# ------generic Publishing function
    # assetName_bundleVersion_v####.mb <-> assetName_bundleVersion_v####.abc
    # createAssetBundle = INCLUDE "assetName_bundleVersion_v####.abc"
def publish_work():
    pass


def create_entry(path, name):
    pass


ftr.create_project(gld.ACTIVE_PROJECT)
progen.create_show(gld.ACTIVE_PROJECT, "24", "2115", "1015")

create_seq(gld.ACTIVE_PROJECT,"XCV")
create_shot(gld.ACTIVE_PROJECT,"XCV", "1010")
create_shot_tasks(gld.ACTIVE_PROJECT,"XCV","1010")

# createproject (name="FUF", framerate="24", global_resolution = "2k")
# create_seq (names=[],)

