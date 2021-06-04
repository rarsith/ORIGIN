import os
import json
from RND import xcg_config_old_not_used as gld

LIST_PROJECTS = []
LIST_SEQ = []
SELECTED_SEQ = ""




def select_project():
    global LIST_PROJECTS
    for path in os.listdir(gld.PROJECTS_ROOT):
        LIST_PROJECTS.append(path)
    print LIST_PROJECTS
    print "Select Project: \n"
    for key in LIST_PROJECTS:
        print key

    selection = raw_input("select project: ").upper()

    if selection in LIST_PROJECTS:


        gld.SELECTED_PROJECT_NAME = selection
        print "selected %s project" % gld.SELECTED_PROJECT_NAME

    else:
        print "Project not found"

    return LIST_PROJECTS

def select_seq():
    global LIST_SEQ
    select_project()
    with open(os.path.join(gld.PROJECTS_ROOT, (str.lower(gld.SELECTED_PROJECT_NAME) + ".json")), "r") as f:
        data = f.read()
        show_dat = json.loads(data)
        seq_path = show_dat[3]["seq_path"]

    for name in os.listdir(seq_path):
        if not name.endswith("json"):
            LIST_SEQ.append(name)

    print "Select Seq: \n"
    for key in LIST_SEQ:
        print key

    selection = raw_input("3 letter code: ").upper()

    if selection in LIST_SEQ:

        global SELECTED_SEQ
        SELECTED_SEQ = selection
        print "selected %s Seq" % SELECTED_SEQ

    else:
        print "Seq %s not found" % selection



