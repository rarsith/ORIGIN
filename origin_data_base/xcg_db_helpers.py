import pprint
from operator import itemgetter

import origin_utilities.utils
from origin_data_base import xcg_db_queries as xqr


def get_entity(db_collection, branch, show_name=""):
    get_items = origin_utilities.utils.db_find_dict_key(db_collection, branch, show_name=show_name)
    return get_items


def get_entity_root_structure(dictionary):
    for keys, val in dictionary.items():
        yield keys


def get_entity_structure(dictionary):
    for keys, val in dictionary.items():
        if isinstance(val, dict):
            for result in get_entity_root_structure(val):
                yield result


def deep_values(key, dictionary):
    for category, val in dictionary.items():
        if category == key:
            yield val
        elif isinstance(val, dict):
            for result in deep_values(key, val):
                yield result
        elif isinstance(val, list):
            for d in val:
                for result in deep_values(key, d):
                    yield result


def list_relatives(parent, entity):
    search_combo = []
    for k in parent:
        search_combo.append(k)
    for x in search_combo:
        get_children = deep_values(x, entity)
        for children in get_children:
            yield children





if __name__ == "__main__":

    entity = get_entity("show", "structure", show_name="gugu")
    print (entity)
    get_all_keys = get_entity_structure(entity)
    temp_list = []
    for t in get_all_keys:
        temp_list.append(t)

    for values in temp_list:
        fuf = deep_values(values, entity)
        for x in fuf:
            print (x)



    # test = list_relatives(temp_list, entity)
    # for y in test:
    #     print y





    # entity = get_entity("show", "structure", show_name="Domino")
    # get_structure = get_entity_root_structure(entity)
    # store_search = []
    # for k in get_structure:
    #     store_search.append(k)
    # # print store_search
    # for x in store_search:
    #     # print x
    #     depth = deep_values(x, entity)
    #     for d in depth:
    #         print d









    # root_structure = get_entity_structure(entity)















