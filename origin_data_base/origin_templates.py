import pprint
from origin_utilities import read_json as oread

def task_defaults():
    json_load = oread.open_json("../origin_config_json/origin_db_templates/task_template.json")
    tasks_read = oread.read_dictionary(json_load, 'root')
    return tasks_read["task"]

def tasks_schema(category):
    json_load = oread.open_json("../origin_config_json/origin_db_defaults/tasks_schemas.json")
    tasks_read = oread.read_dictionary(json_load, category)
    return tasks_read["tasks"]

def entry_definition(category):
    json_load = oread.open_json("../origin_config_json/origin_db_defaults/entries_definition.json")
    tasks_read = oread.read_dictionary(json_load, category)
    return tasks_read["definition"]


if __name__=="__main__":
    tt = entry_definition("build")
    pprint.pprint (tt.keys())