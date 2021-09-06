import json
import pprint


def open_json(source_file):
    with open(source_file, 'r') as json_read:
        read_buffer = json.load(json_read)
    return read_buffer


def read_dictionary(source_data, attribute_to_read):
    return source_data[attribute_to_read]

if __name__=="__main__":
    json_load = open_json("../origin_config_json/origin_db_templates/task_template.json")
    tasks_read = read_dictionary(json_load, 'root')
    print (tasks_read)

    gog = tasks_read["task"]

    pprint.pprint(gog)


