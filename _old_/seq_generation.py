import os
import json
from RND import xcg_config_old_not_used as gld


def create_seq_json(show_name, frame_rate, rx, ry, render_template):
    seq_name = raw_input("Seq_Name: ")
    seq_path = gld.PROJ_SEQ_PATH
    seq_data = [
        {"show_name": show_name},
        {"seq_name": seq_name},
        {"seq_path": seq_path},
        {"frame_rate": frame_rate},
        {"ren_res_x": rx},
        {"ren_res_y": ry},
        {"ren_templ": render_template}
    ]

    data = json.dumps(seq_data)
    with open(os.path.join(gld.PROJ_SEQ_PATH,(seq_name+".json")),"w") as f:
        f.write(data)
    os.makedirs(os.path.join((seq_data[2]["seq_path"]), (seq_data[1]["seq_name"])))



def query_seq_json(show_name, seq_json):
    with open(os.path.join(gld.PROJECTS_ROOT, show_name, seq_json), "r") as f:
        data = f.read()
        show_dat = json.loads(data)
        return show_dat




# create_seq_json(gld.ACTIVE_PROJECT,"24","2115","1015","TEST_RE")
# query_seq_json(gld.PROJ_SEQ_PATH,"BBB.json")




# def create_folders(json_name):
#     get_seq = query_seq_json(gld.PROJ_SEQ_PATH, json_name)
#     os.makedirs (os.path.join((get_seq[2]["seq_path"]), (get_seq[1]["seq_name"])))
#
#
#
# create_folders("KOKO.json")