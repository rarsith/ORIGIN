import json
import pprint


def save_json(file_name, data):
    json_object = json.dumps(data, indent = 4)
    with open(file_name, 'w') as outfile:
        outfile.write(json_object)


if __name__=="__main__":
    json_load = open_json("../origin_config_json/origin_db_templates/task_template.json")
    tasks_read = read_dictionary(json_load, 'root')
    print (tasks_read)

    gog = tasks_read["task"]

    pprint.pprint(gog)


