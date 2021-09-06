import os
import re
from origin_data_base import xcg_db_connection as xcon
import sys

def db_set_work_session(db_collection, show_name, category, entry_name, entry_type):

    db = xcon.server.xchange
    cursor = db.session
    cursor.insert(
        {"WORK_SESSION":seq_name,
         "USER":shot_name
         }
                  )
    session = str(db_collection + show_name + category + entry_name + entry_type )
    envvar = "XCG_CURRENT_SESSION"
    os.environ[envvar] = session


def db_find_key(db_collection, item_to_search, **kwargs):
    """
    will find all the key values from a collection and returns them as a dictionary
    """
    items = []
    db = xcon.server.xchange
    cursor = db[db_collection]
    results = cursor.find(kwargs, {"_id": 0, item_to_search: 1})
    for result in results:
        for k, v in result.items():
            items.append(v)

    return items



def db_find_dict_key(db_collection, item_to_search, **kwargs):
    """
    will find all the key values from a collection and returns them as a dictionary
    """
    items = {}
    db = xcon.server.xchange
    cursor = db[db_collection]
    results = cursor.find(kwargs, {"_id": 0, item_to_search: 1})
    for result in results:
        for k, v in result.items():
            items.update(v)

    return items


def db_deep_find(key, dictionary):
    """
    Given a dictionary, will find the value of a key
    the results can be parsed with a for loop
    """
    for k, v in dictionary.iteritems():
        if k == key:
            yield v
        elif isinstance(v, dict):
            for result in db_deep_find(key, v):
                yield result
        elif isinstance(v, list):
            for result in db_deep_find(key, d):
                yield result

def write_nice_names(items_list):
    extract = []
    for each in items_list:
        catch_it = re.sub('[_]', ' ', each)
        extract.append(catch_it.title())
    return extract


if __name__ == "__main__":
    # db_set_work_session = get_wrk_session("cars", "Doom", "characters", "hulk", "vuvu")
    # print  (os.environ["XCG_CURRENT_SESSION"])
    b = db_find_key("publishes", "version")
    print (b)
    items = ['rend_geo', 'proxy_geo', 'util_geo', 'util_rig', 'anm_crv', 'shot_cam']
    names = write_nice_names(items)
    print (names)

