
import pprint
from xcg_data_base import xcg_db_connection as xcon
from xcg_utilities.xcg_utils import db_find_key, db_deep_find


class CurrentSession(object):

    def __init__(self):
        self.get_active_collection()
        self.get_active_entry()
        self.get_active_task()

    def get_active_collection(self):
        db = xcon.server.xchange
        cursor = db.sessions
        get_data = {}
        get_all = cursor.find({},{"_id":0})
        for data in get_all:
            get_data.update(data)
        collection = get_data["db_collection"]

        return collection

    def get_active_entry(self):
        db = xcon.server.xchange
        cursor = db.sessions
        get_data = {}
        get_all = cursor.find({}, {"_id": 0})
        for data in get_all:
            get_data.update(data)
        entry_id = get_data["session_id"]

        return entry_id

    def get_active_task(self):
        db = xcon.server.xchange
        cursor = db.sessions
        get_data = {}
        get_all = cursor.find({}, {"_id": 0})
        for data in get_all:
            get_data.update(data)
        task_id = get_data["task_name"]

        return task_id


def db_q_entry_id(show_name, db_collection, branch, category, entry_name, query_item):
    db = xcon.server.xchange
    cursor = db[db_collection]

    dictionary_out = {}
    result = []
    path_to_entry = branch + "." + category + "." + entry_name + "." + query_item
    get_entry = cursor.find({"show_name":show_name}, {"_id":1, path_to_entry:1})
    for elem in get_entry:
        dictionary_out.update(elem)

    get_entry_value = db_deep_find(query_item, dictionary_out)
    for elem in get_entry_value:
        result.append(elem)

        return result


def db_q_entry_definition():
    pass


def db_q_tsk_pub_slots():
    db = xcon.server.xchange

    current_session = CurrentSession()
    db_collection = current_session.get_active_collection()
    entry_id = current_session.get_active_entry()
    active_task = current_session.get_active_task()

    get_path = {}
    cursor = db[db_collection]

    task_path = "tasks" + "." + active_task + "." + "pub_slots"
    get_entry = cursor.find({"entry_id":entry_id},{"_id":0, task_path:1})
    for stuff in get_entry:
        get_path.update(stuff)
    return get_path["tasks"][active_task]["pub_slots"]



def db_q_tsk_imports_from():
    db = xcon.server.xchange

    current_session = CurrentSession()
    db_collection = current_session.get_active_collection()
    entry_id = current_session.get_active_entry()
    active_task = current_session.get_active_task()

    get_path = {}
    cursor = db[db_collection]

    task_path = "tasks" + "." + active_task + "." + "imports_from"
    get_entry = cursor.find({"entry_id":entry_id},{"_id":0, task_path:1})
    for stuff in get_entry:
        get_path.update(stuff)

    return get_path["tasks"][active_task]["imports_from"]


def db_q_tsk_artist():
    pass


def db_check_bundle():
    pass


def db_tsk_slots():
    pass


def db_make_slot_reviewable():
    pass




if __name__ == "__main__":
    # jj = db_find_key("assets", "tasks", show_name="Domino", entry_name="guru")
    # pprint.pprint(jj)
    # dictionary =  jj[0]
    # get_keys = dictionary.keys()
    # pprint.pprint(get_keys)

    # num = '7'
    # print type((num.rjust(3, "0")))
    #
    # i = 5
    # print '{0:05d}'.format(i)
    # pub_slots = db_q_tsk_pub_slots()
    # for slot in pub_slots:
    #     print slot
    #
    # imports_from = db_q_tsk_imports_from()
    # for k in imports_from.iteritems():
    #     print k
    #
    # db_q_tsk_pub_slots()
    #
    print ("")
    #
    # db = xcon.server.xchange
    # cursor = db.show
    # db.list_collections()
    #
    # ranging = {}
    # test = cursor.find({}, {"_id": 0, "show_name":1 })
    #
    # for each in test:
    #     print each













