import pprint
from origin_utilities import read_json as oread

def show_structure():
    json_load = oread.open_json("../origin_config_json/origin_db_defaults/show_structure.json")
    structure_read = oread.read_dictionary(json_load, 'structure')
    return structure_read

def task_defaults():
    json_load = oread.open_json("../origin_config_json/origin_db_templates/task_template.json")
    tasks_read = oread.read_dictionary(json_load, 'root')
    return tasks_read["task"]

def tasks_schema(category):
    json_load = oread.open_json("../origin_config_json/origin_db_defaults/tasks_schemas.json")
    tasks_read = oread.read_dictionary(json_load, category)
    return tasks_read["tasks"]

def tasks_pub_slot_schema():
    json_load = oread.open_json("../origin_config_json/origin_db_defaults/tasks_pub_slot_schemas.json")
    tasks_read = oread.read_dictionary(json_load, "pub_slot")
    return tasks_read

def entry_definition(category):
    json_load = oread.open_json("../origin_config_json/origin_db_defaults/entries_definition.json")
    tasks_read = oread.read_dictionary(json_load, category)
    return tasks_read["definition"]


if __name__=="__main__":
    tt = show_structure()
    pprint.pprint (tt)