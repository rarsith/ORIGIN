import os
import json
from RND import xcg_config_old_not_used as gld
from _old_ import xcg_database_utils as xu


# LIST_PROJECTS = []
# LIST_SEQ = []
# SELECTED_SEQ = ""

def writeJsonFile(dataToWrite, fileName):
    if ".json" not in fileName:
        fileName += ".json"

    print "> write to json file is seeing: {0}".format(fileName)

    with open(fileName, "w") as jsonFile:
        json.dump(dataToWrite, jsonFile, indent=2)

    print "Data was successfully written to {0}".format(fileName)

    return fileName

def readJsonFile(fileName):
    try:
      with open(fileName, 'r') as jsonFile:
          return json.load(jsonFile)
    except:
        cmds.error("Could not read {0}".format(fileName))

def create_xchange_db(db_name):
    shows_db = {}
    shows_db['shows'] = []
    shows_db['shows'].append(db_name)


    with open(os.path.join(gld.XCHANGE_DB),"w") as db:
        json.dumps(shows_db, db)

def update_db(show_name, type_to_update):
    pass

def update_shots():
    pass

def update_seq():
    pass

def update_assets():
    pass

def xchange_publish():
    pass


# def update_db(data, key_address, db_json_file):
#
#     db_file = open(os.path.join(gld.PROJECTS_ROOT, db_json_file), "r")
#     json_file = json.load(db_file)
#     db_file.close()
#
#     json_file[key_address] = [data]
#
#     db_file = open(os.path.join(gld.PROJECTS_ROOT, entity_name + ".json"), "w")
#     json.dump(json_file, db_file)
#     db_file.close()



def commit_to_server(show_name, type, *data):
    valid_types = ['shot', 'seq','asset']
    if type not in valid_types:
        print "Check Type spelling!"
        print "Use these: %s" % valid_types
    else:
        if type==shot:
            os.makedirs(os.path.join((project_data[1]["show_path"]), (project_data[0]["show_name"]), seq_path))
            os.makedirs(os.path.join((project_data[1]["show_path"]), (project_data[0]["show_name"]), assets_path))



















def create_show(code_name):
    # code_name = raw_input("Enter Show Code Name: ").upper()
    proj_path = os.path.join(gld.PROJECTS_ROOT, code_name)
    seq_path = os.path.join(proj_path, "seq")
    assets_path = os.path.join(proj_path, "assets")

    # create project description json
    project_data = [{'shows':[{"show_name": code_name},{"show_path": proj_path},{"assets_path": assets_path},{"seq_path": seq_path}]}]

    data = json.dumps(project_data, indent=4, sort_keys=True)
    with open(os.path.join(gld.PROJECTS_ROOT, code_name+".json"),"w") as f:
        data_f = f.write(data)

    # os.makedirs(os.path.join((project_data[1]["show_path"]), (project_data[0]["show_name"]), seq_path))
    # os.makedirs(os.path.join((project_data[1]["show_path"]), (project_data[0]["show_name"]), assets_path))
    return code_name

def create_seq(show_name, seq_name):
    # show_name = xu.select_project()
    # seq_name = raw_input("Enter Seq Name To Create: ").upper()

    with open(os.path.join(gld.PROJECTS_ROOT, (gld.SELECTED_PROJECT_NAME + ".json")), "r") as f:
        data = f.read()
        show_dat = json.loads(data)
        seq_path = show_dat[3]["seq_path"]


    seq_data = [
        {"show_name": gld.SELECTED_PROJECT_NAME},
        {"seq_path": seq_path},
        {"seq_name": seq_name},
    ]
    data = json.dumps(seq_data)
    with open(os.path.join(seq_path, (seq_name + ".json")), "w") as f:
        data_f = f.write(data)

    # os.makedirs(os.path.join(gld.PROJECTS_ROOT, seq_path, seq_name))
    return seq_name

def create_shot(show_name, seq_name, shot_name, rend_x=1920, rend_y=1080, frame_in=1001, frame_out=1001,tasks=[], status="NOT-STARTED", target_date=None):
    # show_name = xu.select_project()
    # seq_name = xu.select_seq()
    # shot_name = raw_input ("Enter Shot ID: ")
    with open(os.path.join(gld.PROJECTS_ROOT, (str.lower(gld.SELECTED_PROJECT_NAME) + ".json")), "r") as f:
        data = f.read()
        show_dat = json.loads(data)
        seq_path = show_dat[3]["seq_path"]

    shot_data = [
        {"show_name": gld.SELECTED_PROJECT_NAME},
        {"seq_path": seq_path},
        {"seq_name": xu.SELECTED_SEQ},
        {"shot_name": shot_name},
        {"frameIn": frame_in},
        {"frameOut": frame_out},
        {"tasks": tasks},
        {"status": status},
        {"target_date": target_date},
        {"rend_x": rend_x},
        {"rend_y": rend_y},

    ]
    data = json.dumps(shot_data)
    with open(os.path.join((os.path.join(seq_path, xu.SELECTED_SEQ)), (shot_name + ".json")), "w") as f:
        data_f = f.write(data)

    # os.makedirs(os.path.join(gld.PROJECTS_ROOT, seq_path, xu.SELECTED_SEQ, shot_name))
    return shot_name

def create_asset(show_name, asset_type, asset_name, hero=False, target_date=None):
    pass

def add_task(entity_name, task_type, assignee, status="NOT_STARTED"):
    pass

def update_task_status(entity_type, entity_name, task, status):

    valid_statuses = ["NOT-STARTED", "IN-PROGRESS", "ON-HOLD", "CANCELLED",
                      "CREATIVE-APPROVED", "FINAL-PENDING-TECH-CHECK", "FINAL"]
    update_db()




    db_file = open(os.path.join(gld.PROJECTS_ROOT, entity_name + ".json"), "r")
    json_file = json.load(db_file)
    db_file.close()

    json_file['task_status'] = [status]

    db_file = open(os.path.join(gld.PROJECTS_ROOT, entity_name + ".json"), "w")
    json.dump(json_file, db_file)
    db_file.close()

    print "Database Updated!"

def set_active_show(show_name, activeBool):
    pass

def link_asset_to_shot(asset_name, shot_name):
    pass



#
# start()
# xu.select_project()
# create_show("TEST")
# query_project_json()
# create_seq("","")
# select_seq()
# create_shot("","","")
#



