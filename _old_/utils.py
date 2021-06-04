


import os
import json
from RND import xcg_config_old_not_used as gld
from _old_ import xcg_database_actions as xa

shows_list = os.listdir(gld.PROJECTS_ROOT)

selected_project = xa.select_project()
selected_seq = xa.select_seq()
selected_shot = ""

def update_db(category):

    global selected_project
    global selected_seq
    global selected_shot

    data = {}
    data[category] = []
    shows_root = gld.PROJECTS_ROOT
    seq_root = gld.PROJ_SEQ_PATH
    shots_root = os.path.join(gld.PROJ_SEQ_PATH, selected_seq)
    assets_root = os.path.join(gld.PROJ_ASSETS_PATH)


    categories_types = ['shows','show_sequences','seq_shots','show_assets','all']

    if category not in categories_types:
        print ("Unknown category! Check spelling!")

    else:
        for show in shows_list:
            if not show.endswith("json"):
                data[category].append(show)

        with open(os.path.join(shows_root, category + '.json'), 'w') as outfile:
            json.dump(data, outfile)

update_db()





