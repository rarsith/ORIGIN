import os
import json


def write_json(file_name, designation, path, **kwargs):
    data_to_write = kwargs
    with open(os.path.join(path, file_name + '_' + designation + '.json'), 'w') as json_file:
        create_json_file = json.dump(data_to_write, json_file, indent=2, sort_keys=True )
    return kwargs


def open_json(file_name, path):
    with open(os.path.join(path, file_name), 'r') as json_read:
        read_buffer = json.load(json_read)
    return read_buffer


def read_task_linking(json_name, file_path, root, task, task_attribute):
    data = open_json(json_name, file_path)
    selected_root = {}
    selected_task = {}

    for data_set in data[root]:
        selected_root.update(data_set)
    for links in selected_root[task]:
        selected_task.update(links)

    return selected_task[task_attribute]


def json_entry(entry_parent, entry_name):
    data_save = {}
    data_save[entry_parent] = [{entry_name: []}]

    nnn = {}
    nun = json_entry('tasks', 'modding')
    n = json_entry('tasks', 'nodding')

    nnn.update(nun)
    nnn.update(n)

    print nnn

    return data_save


def read_data_json(key, dictionary):
    for k, v in dictionary.iteritems():
        if k == key:
            yield v
        elif isinstance(v, dict):
            for result in read_data_json(key, v):
                yield result

        elif isinstance(v, list):
            for d in v:
                for result in read_data_json(key, d):
                    yield result


