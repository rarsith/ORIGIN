# save data in json
import json
from RND import xcg_config_old_not_used as gld

my_json = {"content":[]}

tw = ['one','middle','last']

for tweet in tw:
    dict_data = {'text':tweet, 'rt':'2', 'favs':'3',}

    my_json['content'].append(dict_data)
print(json.dumps(my_json, indent=4, sort_keys=True))


#
def create_xchange_db():
    db_name = [{'shows':[{'show_name': 'show_name'},{'assets':[{'characters':[{'chr_name': []}]},{'props':[{'prop_name': []}]}, {'environments':[{'env_name': []}]}]}, ]},{'sequences':[{'seq':[{'seq_name': 'seq_name'}, {'shot_name': 'shot_name'}, {'shot_tasks': []}]}, {'seq_name':[{'shot_name':['content']}]},[{'shot_name':['content']}]},{'seq_name': [{'shot_name': ['content']}]}]}]
    sxc = json.dumps(db_name, indent=4, sort_keys=True)
    with open(gld.XCHANGE_DB, "w") as f:
        f.write(sxc)
        print(json.dumps(sxc, indent=4, sort_keys=True))

    gld.XCHANGE_DB = {}
    gld.XCHANGE_DB['shows'] = []
    gld.XCHANGE_DB = {"show":"show_name"},{"sequences": []}


    db.shows.update({'name': show_name},{'$push': {'sequences': {"name": seq_name, "shots": []}}})

    db.shows.update({'name': show_name, 'sequences.name': seq_name},{'$push':{'sequences.$.shots': {"name": shot_name}}})

    db.shows.insert({"name": code_name,"long_name": long_name,"sequences": [],"active": False,"ptuid": 1})

def create_folders():
    with open (gld.XCHANGE_DB,"r") as db:
        xcg_db = json.loads(db)
        print xcg_db