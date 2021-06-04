import uuid
import pprint
import getpass
import datetime
from  xcg_utilities import xcg_utils as xutil
from xcg_config import xcg_validation as xvalid
from xcg_data_base import xcg_db_connection as xcon
from xcg_data_base import xcg_db_queries as xqry
import bson


#DATABASE UTILITIES

def generate_unique_id():
    unique_id = str(uuid.uuid4())
    return unique_id


def db_query(db_branch, item, **anchor):
    db = xcon.server.xchange
    data = []
    cursor = db[db_branch]
    results = cursor.find(anchor, {"_id": 0, item: 1})
    for result in results:
        for k, v in result.items():
            data.append(v)
    return data


#DEPRICATE THIS
######
def db_content_summary(show_name, object_type):
    """Returns the content of the assets or the shots, paired with the parent category/sequence.
    To be used to create arrays of dictionaries to be queried for the existence of an item."""
    valid_object_types = ['assets','shots','sequences','show', 'publishes']
    db = xcon.server.xchange
    items_in_collection = []
    if object_type not in valid_object_types:
        print ("Invalid category. Try one of these {}" .format(valid_object_types))

    elif object_type == "show":
        cursor = db.show
        items = cursor.find({}, {"_id": 0, "show_name":1})
        for item in items:
            items_in_collection.append(item)

    elif object_type == "assets":
        cursor = db.assets
        items = cursor.find({"show_name":show_name}, {"_id": 0, "entry_name": 1, "category":1, "show_name":1})
        for item in items:
            items_in_collection.append(item)

    elif object_type == "sequences":
        cursor = db.sequences
        items = cursor.find({"show_name":show_name}, {"_id": 0, "entry_name": 1, "show_name":show_name})
        for item in items:
            items_in_collection.append(item)

    elif object_type == "publishes":
        cursor = db.publishes
        items = cursor.find({"show_name":show_name}, {"_id": 0, "show_name":1, "entity_name":1, "published_by":1, "version":1, "category":1})
        for item in items:
            items_in_collection.append(item)

    return items_in_collection

######

def get_sub_branches(show_name, branch_name):
    sub_branches_list = []
    db = xcon.server.xchange
    query_path = "structure"+"."+branch_name
    all_branches = db.show.find({"show_name": show_name, "active": True},
                                     {'_id': 0, query_path: 1})
    for each in list(all_branches):
        print (each)
        sub_branches_list.append(list(each['structure'][branch_name].keys()))
    return sub_branches_list[0]


def get_sub_branches_content(show_name, branch_name, category_name):
    sub_branches_content_list = []
    db = xcon.server.xchange
    all_branches = db.show.find({"show_name": show_name, "active": True},
                                     {'_id': 0, 'structure': 1})
    if all_branches:
        for each in all_branches:
            sub_branches_content_list.append(list(each['structure'][branch_name][category_name]))
        return sub_branches_content_list[0]

#DATABASE CREATORS

def define_roots_types(root_type):
    db = xcon.server.xchange
    cursor = db['roots_types']
    cursor.insert_one(
        {
            "entry_name":root_type

        }
    )
    print("{} show created!".format(root_type))



def define_branches():
    pass


def define_categories():
    pass


def define_tasks_schemas():
    pass


def define_chains():
    pass


def define_db_hierachy():
    pass


def create_show(show_name, code_name, show_type):
    # create/connect to show database
    # TODO, need checking if show already exists, if True then halt
    get_items = db_content_summary(show_name, "show")
    search_combo = {"show_name": show_name}
    if search_combo in get_items:
        print ("{}} show already exists!".format(show_name))
    else:
        db = xcon.server.xchange
        # Create a collection that contains all shows with their specifications
        db.show.insert(
            {
                "show_code": code_name,
                "show_name": show_name,
                "structure":{"sequences":{},"assets":{'characters':{}, 'environments':{}, 'props':{}}},
                "show_defaults":{"asset_definition":{},
                                 "shot_definition":{},
                                 "assets_tasks_schema":{},
                                 "shots_tasks_schema":{},
                                 "branches_types":{},
                                 "categories_types":{}},
                "active": True,
                "date": datetime.datetime.now(),
                "owner":getpass.getuser(),
                "show_type":show_type
            }
        )
        print ("{} show created!".format(show_name))


def create_show_branch(show_name, branch_name):
    db = xcon.server.xchange
    # update "show" collection for easy navigation
    cursor = db[branch_name]
    cursor.insert({})

    insert_entry = "structure" + "." + branch_name
    db.show.update({"show_name": show_name},
                        {"$set": {insert_entry: {}}})

    print ("{} show_branch created".format(branch_name))


def create_sequence(show_name, seq_name):
    db = xcon.server.xchange
    insert_entry = "structure" + "." + "sequences" + "." + seq_name
    db.show.update({"show_name": show_name},
                        {"$set": {insert_entry:{}}})
    print ("{} sequence created".format(seq_name))


def create_assets_category(show_name, category_name):
    db = xcon.server.xchange
    insert_entry = "structure" + "." + "assets" + "." + category_name
    db.show.update({"show_name": show_name},
                        {"$set": {insert_entry:{}}})

    print ("{} asset_category created".format(category_name))


def create_shot(show_name, category, entry_name, status ='NOT-STARTED', definition = xvalid.VALID_SHOTS_TYPES):

    db = xcon.server.xchange
    db.sequences.insert({
                    "category":category,
                    "entry_name":entry_name,
                    "type":"shot",
                    "show_name": show_name,
                    "status": status,
                    "assignment":{},
                    "tasks": xvalid.VALID_SHOT_TASKS_SCHEMA,
                    "active": True,
                    "definition":definition,
                    "date": datetime.datetime.now(),
                    "owner": getpass.getuser()
    }
    )

    insert_entry = "structure" + "." + "sequences" + "." + category + "." + entry_name
    db.show.update({"show_name": show_name},
                        {"$set": {insert_entry:{}}})

    print ("{} Shot Created!".format(entry_name))


def create_asset(show_name, category, entry_name, status ='NOT-STARTED', definition = xvalid.DEFAULT_ASSET_DEFINITION):
    db = xcon.server.xchange
    db.assets.insert(
        {
            "entry_name": entry_name,
            "type": "asset",
            "show_name": show_name,
            "category": category,
            "status": status,
            "tasks": xvalid.VALID_ASSET_TASKS_SCHEMA,
            "active": True,
            "definition": definition,
            "date": datetime.datetime.now(),
            "owner": getpass.getuser()
        }
    )

    insert_entry = "structure" + "." + "assets" + "." + category + "." + entry_name
    db.show.update({"show_name": show_name},
                        {"$set": {insert_entry: {}}})

    print ("{} Asset Created!".format(entry_name))


def create_task(show_name, branch_category, parent_category, entry_name, task_name):
    show_branches = xvalid.VALID_SHOW_BRANCHES

    if branch_category not in show_branches:
        print ("create task func")
        print ("{} category is not valid. Please enter one of these {}".format(branch_category, show_branches))
    else:
        # create/connect to show database
        db = xcon.server.xchange
        cursor = db[branch_category]
        shot_task_address = "tasks" + "." + task_name
        cursor.update({"show_name": show_name, "entry_name": entry_name, "category":parent_category},
                        {"$set": {shot_task_address: {'active':True,'status':'NOT-STARTED','artist': None}}})


def create_subtask(show_name, entry_category, parent_category, entry_name, task_name, subtask_name):
    pass


# OMIT FUNC

def omit_sequence(show_name, entry_name):
    db = xcon.server.xchange
    db.sequences.update({"show_name":show_name, "entry_name":entry_name},
                        {"$set": {"active": False}})


def omit_shot(show_name, seq_name, entry_name):
    db = xcon.server.xchange
    db.sequences.update({"show_name": show_name, "category":seq_name, "entry_name": entry_name},
                        {"$set": {"active": False}})


def omit_asset(show_name, entry_category, entry_name):
    db = xcon.server.xchange
    cursor = db.sequences
    db.assets.update({"show_name": show_name, "category": entry_category, "entry_name": entry_name},
                    {"$set": {"active": False}})


def omit_task(show_name, branch_category, parent_category, entry_name, task_name):
    asset_categories = xvalid.VALID_ASSETS_CATEGORIES
    shot_categories = xvalid.VALID_SHOTS_CATEGORIES
    if branch_category not in (asset_categories + shot_categories):
        print ("omit task Func")
        print ("{} category is not valid. Please enter one of these {}".format(branch_category, (asset_categories + shot_categories)))
    else:
        # create/connect to show database
        db = xcon.server.xchange
        if branch_category == "assets":
            asset_task_address = "tasks" + "." + task_name
            db.assets.update({"show_name": show_name, "entry_name": entry_name},
                             {'$unset': {asset_task_address:""}})
            asset_taskLinking_address = "task_linking" + "." + task_name
            db.assets.update({"show_name": show_name, "entry_name": entry_name},
                             {"$unset": {asset_taskLinking_address:""}})

        elif branch_category == "sequences":
            shot_task_address = "tasks" + "." + task_name
            db.sequences.update({"show_name": show_name, "entry_name": entry_name, "category": parent_category},
                            {"$unset": {shot_task_address:""}})

            shot_taskLinking_address = "task_linking" + "." + task_name
            db.sequences.update({"show_name": show_name, "entry_name": entry_name, "category": parent_category},
                            {"$unset": {shot_taskLinking_address:""}})


def omit_task_pub_slot(show_name, show_branch, category, entry_name, task_name):
    pass


def rem_assets_from_shot(show_name, show_branch, category, entry_name, asset_to_remove):
    pass


#SET FUNC

def update_task_imports_from(show_name, branch_category, parent_category, entry_name, task_name, imports_from=[]):
    for each in imports_from:
        db = xcon.server.xchange
        cursor = db[branch_category]
        shot_taskLinking_address = "tasks" + "." + task_name + "." + "imports_from" + "." + each
        cursor.update({"show_name": show_name, "entry_name": entry_name, "category": parent_category},
                        {"$set": {shot_taskLinking_address: {}}})
        print ("{} task added as import_source".format(each))


def update_task_pub_slot(show_name, branch_category, parent_category, entry_name, task_name, pub_slot=[]):
    for each in pub_slot:
        db = xcon.server.xchange
        cursor = db[branch_category]
        taskLinking_path = "tasks" + "." + task_name + "." + "pub_slots" + "." + each
        cursor.update({"show_name": show_name, "entry_name": entry_name, "category": parent_category},
                      {"$set": {taskLinking_path: {}}})
        print ("{} added as pub_slot".format(each))


def update_task_pub_used_by(show_name, branch_category, parent_category, entry_name, task_name, pub_slot, used_by, remove_action=False):
    db = xcon.server.xchange
    cursor = db[branch_category]

    pub_slot_path = "tasks" + "." + task_name + "." + "pub_slots" + "." + pub_slot + "." + "used_by"
    existing_data = cursor.find_one({"show_name": show_name, "entry_name": entry_name, "category": parent_category},
                                    {'_id': 0, pub_slot_path: 1})
    existing_assignment = existing_data['tasks'][task_name]['pub_slots'][pub_slot]['used_by']
    if not remove_action:
        if used_by not in existing_assignment:
            cursor.update_one({"show_name": show_name, "entry_name": entry_name, "category": parent_category},
                          {"$push": {pub_slot_path: used_by}})
    else:
        if used_by in existing_assignment:
            cursor.update_one({"show_name": show_name, "entry_name": entry_name, "category": parent_category},
                          {"$pull": {pub_slot_path: used_by}})


def update_task_pub_slot_dict(show_name, branch_category, parent_category, entry_name, task_name, pub_slot=[]):
    for each in pub_slot:
        get_slot_name = (list(each.keys()))
        get_slot_param = (list(each.values()))
        db = xcon.server.xchange
        cursor = db[branch_category]
        pub_slot_path = "tasks" + "." + task_name + "." + "pub_slots" + "." + get_slot_name[0]
        cursor.update({"show_name": show_name, "entry_name": entry_name, "category": parent_category},
                      {"$set": {pub_slot_path: get_slot_param[0]}})
    print ("Publish Slot added succesfully!")


def update_task_status(show_name, branch_category, parent_category, entry_name, task_name, task_status):
    # create/connect to show database
    db = xcon.server.xchange
    db_collection = db[branch_category]
    db_address = "tasks" + "." + task_name + "." + "status"
    db_collection.update({"show_name": show_name, "entry_name": entry_name, "category": parent_category},
                         {'$set': {db_address:task_status}})


def update_task_is_active(show_name, branch_category, parent_category, entry_name, task_name, is_active):
    # create/connect to show database
    db = xcon.server.xchange
    db_collection = db[branch_category]
    db_address = "tasks" + "." + task_name + "." + "active"
    db_collection.update({"show_name": show_name, "entry_name": entry_name, "category": parent_category},
                         {'$set': {db_address:is_active}})


def update_task_user(show_name, branch_category, parent_category, entry_name, task_name, artist_name):
    asset_categories = xvalid.VALID_ASSETS_CATEGORIES
    shot_categories = xvalid.VALID_SHOTS_CATEGORIES
    if branch_category not in (asset_categories + shot_categories):
        print ("update_task_user")
        print ("{} category is not valid. Please enter one of these {}".format(branch_category,(asset_categories + shot_categories)))
    else:
        # create/connect to show database
        db = xcon.server.xchange
        db_collection = db[branch_category]
        db_address = "tasks" + "." + task_name + "." + "artist"
        db_collection.update({"show_name": show_name, "entry_name": entry_name, "category": parent_category},
                             {'$set': {db_address: artist_name}})


def update_asset_category(show_name, asset_name, asset_category):
    # create/connect to show database
    db = xcon.server.xchange
    db.assets.update({"show_name":show_name, "entry_name":asset_name},
                        {'$set':{"category": asset_category}})
    db.show.update({"show_name": show_name, "structure.assets.entry_name":asset_name},
                        {"$set": {"assets.category": asset_category}})


def update_entry_definition(show_name, branch_category, parent_category, entry_name, definition):
    db = xcon.server.xchange
    cursor = db[branch_category]
    cursor.update({"show_name": show_name, "entry_name": entry_name, "category": parent_category},
                  {"$set": {"definition": definition}})

    print ("{} definition Updated!".format(entry_name))


def add_asset_to_shot(show_name, seq_name, shot_name, asset_name, asset_category, asset_count):
    asset_categories = xvalid.VALID_ASSETS_CATEGORIES

    if asset_category not in asset_categories:
        print ("{} not a valid category. Please use one of these %s".format (asset_category, asset_categories))

    else:
        get_assets = db_content_summary(show_name, "assets")
        search_combo = {"show_name": show_name, "entry_name": asset_name, "category": asset_category}

        if search_combo not in get_assets:
            print ("Asset does not exist. Please check your input!")

        else:
            db = xcon.server.xchange
            cursor = db.sequences
            get_assignments_list = []
            current = cursor.find({'show_name': show_name,'entry_name':shot_name, 'category':seq_name}, {'_id': 0, 'assignment':1})
            for i in current:
                for keys, values in i.iteritems():
                    for each in values:
                        get_assignments_list.append(each[0])

            if asset_name in get_assignments_list:
                print ("Asset {} already assigned to {} shot. Please check your input!".format (asset_name, shot_name))

            else:
                asset_path = "assignment" + "." + asset_name
                db.sequences.update({"show_name": show_name, "entry_name": shot_name, "category":seq_name},
                                {"$set": {asset_path: {'category':asset_category, 'count':asset_count}}})

# DATABASE REMOVERS


def remove_all_task_pub_slots(show_name, branch_category, parent_category, entry_name, task_name):
    try:

        show_branches = xvalid.VALID_SHOW_BRANCHES

        if branch_category not in show_branches:
            print ("remove_all_task_pub_slots")
            print ("{} category is not valid. Please enter one of these {}".format(branch_category, show_branches))
        else:
            # create/connect to show database
            db = xcon.server.xchange
            task_path = "tasks" + "." + task_name + "." + "pub_slots"
            cursor = db[branch_category]
            cursor.update({"show_name": show_name, "category": parent_category, "entry_name": entry_name},
                                       {"$unset":{task_path:1}})

            cursor.update({"show_name": show_name, "category": parent_category, "entry_name": entry_name},
                          {"$set": {task_path: {}}})


    except:
        pass


def remove_all_task_import_slots(show_name, branch_category, parent_category, entry_name, task_name):
    try:

        show_branches = xvalid.VALID_SHOW_BRANCHES

        if branch_category not in show_branches:
            print ("remove_all_task_import_slots")
            print ("{} category is not valid. Please enter one of these {}".format(branch_category, show_branches))
        else:
            # create/connect to show database
            db = xcon.server.xchange
            task_path = "tasks" + "." + task_name + "." + "imports_from"
            cursor = db[branch_category]
            cursor.update({"show_name": show_name, "category": parent_category, "entry_name": entry_name},
                                       {"$unset":{task_path:1}})

            cursor.update({"show_name": show_name, "category": parent_category, "entry_name": entry_name},
                          {"$set": {task_path: {}}})


    except:
        pass


def remove_entry(show_name, branch_category, entry_category, entry_name):
    try:

        show_branches = xvalid.VALID_SHOW_BRANCHES
        if branch_category not in show_branches:
            print ("remove_entry")
            print ("{} category is not valid. Please enter one of these {}".format(branch_category, show_branches))
        else:
            # create/connect to show database
            db = xcon.server.xchange
            # remove the entry from the show structure
            entry_path = "structure" + "." + branch_category + "." + entry_category + "." + entry_name
            db.show.update({"show_name": show_name}, {"$unset": {entry_path: 1}})

            # remove entry from its collection
            cursor = db[branch_category]
            cursor.remove({"show_name": show_name, "category": entry_category, "entry_name": entry_name},
                          {entry_name})

            print ('entry {} deleted from {} collection and removed from {} show structure'.format (entry_name, branch_category, show_name))


    except:
        pass



#DATABASE GETTERS

def get_all_active_shows():
    try:
        shows_list = []
        db = xcon.server.xchange
        all_shows = db.show.find({"active":True}, {'_id':0, 'show_name':1})
        for each in all_shows:
            get_values = list(each.values())
            shows_list.append(get_values[0])
        return shows_list

    except:
        pass


def get_show_base_structure(show_name):
     try:
        db = xcon.server.xchange
        all_assets = db.show.find({"show_name": show_name, "active": True},
                                       {'_id': 0, 'structure': 1})
        for each in list(all_assets):
            return each['structure']

     except:
        pass


def get_show_branches_structure(show_name):
    try:
        branches_list = []
        db = xcon.server.xchange
        all_assets = db.show.find({"show_name": show_name, "active": True},
                                       {'_id': 0, 'structure': 1})
        for each in list(all_assets):
            return list(each['structure'])
    except:
        pass


def get_show_assets_categories(show_name):
    try:
        db = xcon.server.xchange
        all_assets = db.show.find({"show_name": show_name, "active": True},
                                       {'_id': 0, 'structure.assets': 1})
        for each in all_assets:
            return list(each['structure']['assets'].keys())

    except:
        pass


def get_all_active_assets(show_name, category):
    try:
        assets_list = []
        db = xcon.server.xchange
        all_assets = db.assets.find({"show_name": show_name, "category": category, "active": True}, {'_id': 0, 'entry_name': 1})
        for each in all_assets:
            assets_list.append(each['entry_name'])
        return assets_list
    except:
        pass


def get_show_sequences(show_name):
    try:
        db = xcon.server.xchange
        all_assets = db.show.find({"show_name": show_name, "active": True},
                                       {"_id": 0, "structure.sequences":1})
        for each in all_assets:
            return list(each['structure']['sequences'])

    except:
        pass


def get_all_active_shots(show_name, category):
    try:
        shots_list = []
        db = xcon.server.xchange
        all_shots = db.sequences.find({"show_name": show_name, "category": category, "active": True},
                                    {'_id': 0, 'entry_name': 1})
        for each in all_shots:
            shots_list.append(each['entry_name'])
        return shots_list
    except:
        pass


def get_tasks_content(show_name, branch_category, parent_category, entry_name):
    try:
        entry_tasks = []
        if branch_category == None or parent_category == None:
            return
        else:
            # create/connect to show database
            db = xcon.server.xchange
            cursor = db[branch_category]
            tasks_list = cursor.find({"show_name": show_name, "category": parent_category, "entry_name": entry_name}, {'_id':0, 'tasks':1})
            for elements in tasks_list:
                print (elements)
                for tasks, task_name in elements.items():
                    entry_tasks.append(list(task_name.keys()))

            return entry_tasks
    except:
        pass


def get_tasks(show_name, branch_category, parent_category, entry_name):
    try:
        entry_tasks = []
        if branch_category == None or parent_category == None:
            return
        else:
            # create/connect to show database
            db = xcon.server.xchange
            cursor = db[branch_category]
            tasks_list = cursor.find({"show_name": show_name, "category": parent_category, "entry_name": entry_name}, {'_id':0, 'tasks':1})
            for elements in tasks_list:
                for tasks, task_name in elements.items():
                    entry_tasks.append(list(task_name.keys()))

            return entry_tasks[0]
    except:
        pass


def get_task_definition(show_name, branch_category, parent_category, entry_name, task_name):

    try:
        entry_task = []
        show_branches = xvalid.VALID_SHOW_BRANCHES

        if branch_category not in show_branches:
            print ("get_task_definition")
            print ("{} category is not valid. Please enter one of these {}".format(branch_category, show_branches))
        else:
            # create/connect to show database
            db = xcon.server.xchange
            task_path = "tasks" + "." + task_name
            cursor = db[branch_category]
            tasks_list = cursor.find({"show_name": show_name, "category": parent_category, "entry_name": entry_name},
                                       {'_id': 0, task_path: 1})
            for tasks in tasks_list:
                entry_task.append(tasks.values()[0].values()[0])
        return entry_task

    except:
        pass


def get_task_pub_slots(show_name, branch_category, parent_category, entry_name, task_name):
    try:
        entry_task = []
        show_branches = xvalid.VALID_SHOW_BRANCHES
        if branch_category not in show_branches:
            print ("get_task_pub_slots")
            print ("{} category is not valid. Please enter one of these {}".format(branch_category, show_branches))
        else:
            # create/connect to show database
            db = xcon.server.xchange
            task_path = "tasks" + "." + task_name + "." + "pub_slots"
            cursor = db[branch_category]
            tasks_list = cursor.find({"show_name": show_name, "category": parent_category, "entry_name": entry_name},
                                       {'_id': 0, task_path: 1})
            for tasks in tasks_list:
                for tsk, tsk_name in tasks.items():
                    entry_task.append(list(tsk_name[task_name]['pub_slots']))
        return entry_task[0]
    except:
        pass


def get_pub_slots(show_name, branch_category, parent_category, entry_name, task_name):
    try:
        entry_task = []
        show_branches = xvalid.VALID_SHOW_BRANCHES
        if branch_category not in show_branches:
            print ("get_task_pub_slots")
            print ("{} category is not valid. Please enter one of these {}".format(branch_category, show_branches))
        else:
            # create/connect to show database
            db = xcon.server.xchange
            task_path = "tasks" + "." + task_name + "." + "pub_slots"
            cursor = db[branch_category]
            tasks_list = cursor.find({"show_name": show_name, "category": parent_category, "entry_name": entry_name},
                                       {'_id': 0, task_path: 1})
            for tasks in tasks_list:
                for tsk, tsk_name in tasks.items():
                    entry_task.append(tsk_name[task_name]['pub_slots'])
        return entry_task[0]
    except:
        pass

def get_ALL(*args):
    print (args)
    # try:
    #     entry_task = []
    #     show_branches = xvalid.VALID_SHOW_BRANCHES
    #     if branch_category not in show_branches:
    #         print ("get_task_pub_slots")
    #         print ("{} category is not valid. Please enter one of these {}".format(branch_category, show_branches))
    #     else:
    #         # create/connect to show database
    #         db = xcon.server.xchange
    #         task_path = "tasks" + "." + task_name + "." + "pub_slots"
    #         cursor = db[branch_category]
    #         tasks_list = cursor.find({"show_name": show_name, "category": parent_category, "entry_name": entry_name},
    #                                    {'_id': 0, task_path: 1})
    #         for tasks in tasks_list:
    #             for tsk, tsk_name in tasks.items():
    #                 entry_task.append(tsk_name[task_name]['pub_slots'])
    #     return entry_task[0]
    # except:
    #     pass


def get_pub_type(show_name, branch_category, parent_category, entry_name, task_name, pub_slot):
    try:
        entry_task = []
        show_branches = xvalid.VALID_SHOW_BRANCHES

        if branch_category not in show_branches:
            print ('get_pub_type')
            print ("{} category is not valid. Please enter one of these {}".format(branch_category, show_branches))
        else:
            # create/connect to show database
            db = xcon.server.xchange
            task_path = "tasks" + "." + task_name + "." + "pub_slots" + "." + pub_slot + "." + "type"
            cursor = db[branch_category]
            tasks_list = cursor.find({"show_name": show_name, "category": parent_category, "entry_name": entry_name},
                                       {'_id': 0, task_path: 1})
            for tasks in tasks_list:
                for tsk, tsk_name in tasks.items():
                    entry_task.append(tsk_name[task_name]['pub_slots'][pub_slot]['type'])
        return entry_task

    except:
        pass


def get_pub_method(show_name, branch_category, parent_category, entry_name, task_name, pub_slot):
    try:
        entry_task = []
        show_branches = xvalid.VALID_SHOW_BRANCHES

        if branch_category not in show_branches:
            print ("get_pub_type")
            print ("{} category is not valid. Please enter one of these {}".format(branch_category, show_branches))
        else:
            # create/connect to show database
            db = xcon.server.xchange
            task_path = "tasks" + "." + task_name + "." + "pub_slots" + "." + pub_slot + "." + "method"
            cursor = db[branch_category]
            tasks_list = cursor.find({"show_name": show_name, "category": parent_category, "entry_name": entry_name},
                                       {'_id': 0, task_path: 1})
            for tasks in tasks_list:
                for tsk, tsk_name in tasks.items():
                    entry_task.append(entry_task.append(tsk_name[task_name]['pub_slots'][pub_slot]['method']))

        return entry_task

    except:
        pass


def get_pub_used_by(show_name, branch_category, parent_category, entry_name, task_name, pub_slot):
    try:
        show_branches = xvalid.VALID_SHOW_BRANCHES

        if branch_category not in show_branches:
            print ("get_pub_type")
            print ("{} category is not valid. Please enter one of these {}".format(branch_category, show_branches))
        else:
            # create/connect to show database
            db = xcon.server.xchange
            task_path = "tasks" + "." + task_name + "." + "pub_slots" + "." + pub_slot + "." + "used_by"
            cursor = db[branch_category]
            tasks_list = cursor.find({"show_name": show_name, "category": parent_category, "entry_name": entry_name},
                                       {'_id': 0, task_path: 1})
            for tasks in tasks_list:
                for tsk, tsk_name in tasks.items():
                    return tsk_name[task_name]['pub_slots'][pub_slot]['used_by']


    except:
        pass


def get_pub_used_by_task(data, task_name):
    get_pub_slots = []
    get_slots = list(data.keys())
    for x  in get_slots:
        if task_name in data[x]['used_by']:
            get_pub_slots.append(x)
    return get_pub_slots


def get_pub_is_reviewable(show_name, branch_category, parent_category, entry_name, task_name, pub_slot):
    try:
        entry_task = []
        show_branches = xvalid.VALID_SHOW_BRANCHES

        if branch_category not in show_branches:
            print ("get_pub_is_reviewable")
            print ("{} category is not valid. Please enter one of these {}".format(branch_category, show_branches))
        else:
            # create/connect to show database
            db = xcon.server.xchange
            task_path = "tasks" + "." + task_name + "." + "pub_slots" + "." + pub_slot + "." + "reviewable"
            cursor = db[branch_category]
            tasks_list = cursor.find({"show_name": show_name, "category": parent_category, "entry_name": entry_name},
                                       {'_id': 0, task_path: 1})
            for tasks in tasks_list:
                for tsk, tsk_name in tasks.items():
                    entry_task.append(entry_task.append(tsk_name[task_name]['pub_slots'][pub_slot]['reviewable']))

        return entry_task
    except:
        pass


def get_pub_is_active(show_name, branch_category, parent_category, entry_name, task_name, pub_slot):
    try:
        entry_task = []
        show_branches = xvalid.VALID_SHOW_BRANCHES

        if branch_category not in show_branches:
            print ("get_pub_is_active")
            print ("{} category is not valid. Please enter one of these {}".format(branch_category, show_branches))
        else:
            # create/connect to show database
            db = xcon.server.xchange
            task_path = "tasks" + "." + task_name + "." + "pub_slots" + "." + pub_slot + "." + "active"
            cursor = db[branch_category]
            tasks_list = cursor.find({"show_name": show_name, "category": parent_category, "entry_name": entry_name},
                                       {'_id': 0, task_path: 1})
            for tasks in tasks_list:

                for tsk, tsk_name in tasks.items():
                    entry_task.append(entry_task.append(tsk_name[task_name]['pub_slots'][pub_slot]['active']))

        return entry_task
    except:
        pass


def get_task_imports_from(show_name, branch_category, parent_category, entry_name, task_name):
    try:
        task_imports_from_list = []
        task_imports_from = []
        show_branches = xvalid.VALID_SHOW_BRANCHES

        if branch_category not in show_branches:
            print ("get_task_imports_from")
            print ("{} category is not valid. Please enter one of these {}".format(branch_category, show_branches))
        else:
            # create/connect to show database
            db = xcon.server.xchange
            task_path = "tasks" + "." + task_name + "." + "imports_from"
            cursor = db[branch_category]
            tasks_list = cursor.find({"show_name": show_name, "category": parent_category, "entry_name": entry_name},
                                     {'_id': 0, task_path: 1})
            for tasks in tasks_list:
                for tsk, tsk_name in tasks.items():
                    task_imports_from_list.append(list(tsk_name[task_name]['imports_from'].keys()))
        return task_imports_from_list[0]



    except:
        pass


def get_task_status(show_name, branch_category, parent_category, entry_name, task_name):
    try:
        entry_task = []
        show_branches = xvalid.VALID_SHOW_BRANCHES

        if branch_category not in show_branches:
            print ("get_task_status")
            print ("{} category is not valid. Please enter one of these {}".format(branch_category, show_branches))
        else:
            # create/connect to show database
            db = xcon.server.xchange
            task_path = "tasks" + "." + task_name + "." + "status"
            cursor = db[branch_category]
            tasks_list = cursor.find({"show_name": show_name, "category": parent_category, "entry_name": entry_name},
                                     {'_id': 0, task_path: 1})
            for tasks in tasks_list:
                entry_task.append(tasks['tasks'][task_name]['status'])
        return entry_task
    except:
        pass


def get_task_is_active(show_name, branch_category, parent_category, entry_name, task_name):
    try:
        entry_task = []
        show_branches = xvalid.VALID_SHOW_BRANCHES

        if branch_category not in show_branches:
            print ("get_task_is_active")
            print ("{} category is not valid. Please enter one of these {}".format(branch_category, show_branches))
        else:
            # create/connect to show database
            db = xcon.server.xchange
            task_path = "tasks" + "." + task_name + "." + "active"
            cursor = db[branch_category]
            tasks_list = cursor.find({"show_name": show_name, "category": parent_category, "entry_name": entry_name},
                                     {'_id': 0, task_path: 1})
            for tasks in tasks_list:
                entry_task.append(tasks['tasks'][task_name]['active'])
        return entry_task
    except:
        pass


def get_task_user():
    pass


def get_entry_definition(show_name, branch_category, parent_category, entry_name):
    try:
        entry_definition = []
        if branch_category == None or parent_category == None:
            return ""
        else:
            # create/connect to show database
            db = xcon.server.xchange
            cursor = db[branch_category]
            definitions_list = cursor.find({"show_name": show_name, "category": parent_category, "entry_name": entry_name},
                                     {'_id': 0, 'definition': 1})
            for definitions in definitions_list:
                entry_definition.append(definitions['definition'])
        return entry_definition[0]
    except:
        pass


def get_entry_type(show_name, branch_category, parent_category, entry_name):
    try:
        entry_type = []
        if branch_category == None or parent_category == None:
            return ""
        else:
            # create/connect to show database
            db = xcon.server.xchange
            cursor = db[branch_category]
            read_type = cursor.find({"show_name": show_name, "category": parent_category, "entry_name": entry_name}, {'_id': 0, 'type': 1})
            for definitions in read_type:
                entry_type.append(definitions['type'])
        return entry_type[0]
    except:
        pass


def get_entry_assigned(show_name, branch_category, parent_category, entry_name):
    try:
        entry_assignment = []

        show_branches = xvalid.VALID_SHOW_BRANCHES
        if branch_category not in show_branches:
            print ("get_entry_assigned")
            print ("{} category is not valid. Please enter one of these {}".format(branch_category, show_branches))
        else:
            # create/connect to show database
            db = xcon.server.xchange
            cursor = db[branch_category]
            tasks_list = cursor.find({"show_name": show_name, "category": parent_category, "entry_name": entry_name},
                                        {'_id': 0, 'assignment': 1})
            for elements in tasks_list:
                for tasks, task_name in elements.iteritems():
                    entry_assignment.append(task_name.keys())

        return entry_assignment[0]
    except:
        pass


def get_definition_element(show_name, branch_category, parent_category, entry_name, definition_element):
    try:
        entry_assignment = []
        # create/connect to show database

        db = xcon.server.xchange
        cursor = db[branch_category]
        tasks_list = cursor.find({"show_name": show_name, "category": parent_category, "entry_name": entry_name},
                                    {'_id': 0, 'definition': 1})

        for elements in tasks_list:
            for tasks, task_name in elements.items():
                if tasks != "definition":
                    return ""
                else:
                    entry_assignment.append(task_name[definition_element])
        return entry_assignment[0]

    except:
        return ""


def get_definition_attributes(show_name, branch_category, parent_category, entry_name):
    try:
        attribute_name = []
        attribute_value = []
        full_attrib = {}
        # create/connect to show database

        db = xcon.server.xchange
        cursor = db[branch_category]
        tasks_list = cursor.find({"show_name": show_name, "category": parent_category, "entry_name": entry_name},
                                    {'_id': 0, 'definition': 1})

        for elements in tasks_list:
            for tasks, task_name in elements.iteritems():
                if tasks != "definition":
                    return ""
                else:
                    attribute_name.append(task_name)
                    # attribute_value.append(task_name.values())

        # for each in attribute_name:
        #     full_attrib[each] =
        #
        # print full_attrib
        return attribute_name[0]

    except:
        return ""


#DATABASE MISC
def db_create_session():
    db = xcon.server.xchange
    db.sessions.insert(
        {

            "user": "",
            "db_collection": "",
            "task_name": "",
            "session_id": ""

        }
    )


def db_set_session(db_collection, show_name, category, entry_name, task_name, user):
    db = xcon.server.xchange

    cursor = db[db_collection]
    entry_id_save = {}
    session_id = []
    get_session_path = cursor.find({"show_name":show_name, "category":category, "entry_name": entry_name},  {"_id":0, "entry_id":1})

    for dictionary in get_session_path:
        entry_id_save.update(dictionary)

    get_entry_value = xcg_utilities.xcg_utils.db_deep_find("entry_id", entry_id_save)
    for elem in get_entry_value:
        session_id.append(elem)

    db.sessions.update({},{"$set":{"user":user, "db_collection":db_collection, "session_id":session_id[0], "task_name": task_name}})


def db_ver_increase(show_name, entity_type, entity_name, task_name, artist):

    get_versions = xcg_utilities.xcg_utils.db_find_key("publishes", "version",
                                                       entry_type=entity_type,
                                                       entry_name=entity_name,
                                                       task_name=task_name,
                                                       artist=artist,
                                                       show_name=show_name
                                                       )

    if not len(get_versions) < 1:
        conv_to_int = []
        for string in get_versions:
            conv_to_int.append(int(string))
        ref_elem = conv_to_int[0]
        for item in range(0, len(conv_to_int)):
            if conv_to_int[item] > ref_elem:
                ref_elem = conv_to_int[item]
        next_ver = ref_elem + 1
        next_ver_format = "{0:04d}".format(next_ver)
        return next_ver_format
    else:
        first_ver = 1
        first_ver_format = "{0:04d}".format(first_ver)
        return first_ver_format


def db_publish(show_name, category, entry_type, entry_name, task_name, artist, bundle_type, bundle_version, status):

    version = db_ver_increase(show_name, entry_type, entry_name, task_name, artist)
    components = xqry.db_q_tsk_pub_slots()

    db = xcon.server.xchange
    db.publishes.insert({
        "show_name": show_name,
        "entry_name": entry_name,
        "category": category,
        "entry_type": entry_type,
        "task_name": task_name,
        "status": status,
        "description":[],
        "artist": artist,
        "version": version,
        "components": components,
        "display_name":(entry_name + "_" + task_name + "_" + version),
        "bundle_type": bundle_type,
        "bundle_version": bundle_version
    }
    )


def db_create_bundle():
    pass


def db_validate_bundle():
    pass


def db_health_check():
    pass


#####USERS#####

def create_user(first_name, name, personal_email, job_title):
    db = xcon.server.xchange
    db.users.insert_one(
        {
            "first_name": first_name,
            "name": name,
            "active": True,
            "personal_email": personal_email,
            "job_title": job_title,
            "user_name": {},
            "internal_email": {},
            "date": datetime.datetime.now(),
            "created_by": getpass.getuser()

        }
    )
    print(" user for {} created!".format(first_name+" "+name))
    pass

class GetProject(object):
    def __init__(self):
        pass

class GetEntity(object):
    def __init__(self):
        self.show_name = ''
        self.branch_name = ''
        self.category_name = ''
        self.entry_name = ''
        self.task_name = ''





if __name__=="__main__":
    import pprint
    cc = get_sub_branches_content('Test', 'sequences', 'TST')
    print (cc)
    # db_publish("DOmino", "characters", "assets", "sukka", "modeling", "john", "asset", "0013", "Pending-Review")

    # user_task_assign("Fly", "characters", "assets", "spear", "facial_expressions", "Kuku")

    # change_task_status("Fly", "characters", "assets", "spear", "facial_expressions", "WIP")

    # db_ver_increase("Test", "assets", "hulk", "modeling", "john")

    # create_tasks("Destroy","assets","JHJHGKJHG")

    # add_tasks("Doom","shots","DDD","0010","retopology","modeling","sculpting")
    # h = get_tasks("Doom","shots","DDD","0010")
    # pprint.pprint(h)
    # add_tasks(show_name, entry_category, parent_category, entry_name, task_name, *imports_from)
    # add_asset_to_shot("Doom","DDD","0010", "clark", "characters", "5" )

    # change_task_status('Fighter','GFF','shots','0010','ChoochityPuh','WIP')

    # delete_task('Fighter','shots','GFF','0010','ChoochityPuh')

    # get current session

    # gg = get_tasks("Test", "assets",  "characters", "hulky")
    # print(gg)
    # ww = get_task_definition("Test", "assets",  "characters", "hulky", "modeling")
    # print (ww)
    # jj = get_show_base_structure('Test')
    # print (jj)
    # oo = get_show_branches_structure('Test')
    # print (oo)
    # pp = get_show_assets_categories('Test')
    # print (pp)
    # ss = get_all_active_assets('Test', 'characters')
    # print (ss)
    # bb = get_show_sequences('Test')
    # print (bb)
    # kl = get_all_active_shots('Test', 'TST')
    # print (kl)
    # hj = get_sub_branches_content( 'Test', 'assets', 'characters')
    # print (hj)
    # mb = get_definition_element("Test", "sequences",  "TST", '0100', 'frame_in')
    # print (mb)
    # # create_user("Dodo", "Georgio", "georgio.antonio@gmail.com", "cook")
    # op = get_task_pub_slots("Test", "sequences",  "VVV", '0150', 'animation')
    # print (op)
    # kl = get_pub_slots("Test", "sequences",  "TST", '0100', 'cam_track')
    # pprint.pprint (kl)
    # tty = get_tasks_content("Test", "sequences", "TST", '0100')
    # pprint.pprint(tty)



    # update_task_pub_used_by("Test", "sequences",  "TST", '0100', 'cam_track', 'HO','animation')

    # dt = {'distortion': {'type': 'cfg', 'method': 'cfg_scn_exp', 'used_by': [], 'source': {}, 'reviewable': False, 'active': True}, 'shot_cam': {'type': 'csh', 'method': 'mf_csh', 'used_by': ['animation'], 'source': {}, 'reviewable': False, 'active': True}, 'HO': {'type': 'csh', 'method': 'sf_csh', 'used_by': ['animation'], 'source': {}, 'reviewable': False, 'active': True}, 'locators': {'type': 'img', 'method': 'sf_csh', 'used_by': [], 'source': {}, 'reviewable': False, 'active': True}, 'wit_cam_01': {'type': 'csh', 'method': 'mf_csh', 'used_by': [], 'source': {}, 'reviewable': False, 'active': True}, 'wit_cam_02': {'type': 'csh', 'method': 'mf_csh', 'used_by': [], 'source': {}, 'reviewable': False, 'active': True}, 'wit_cam_03': {'type': 'csh', 'method': 'mf_csh', 'used_by': [], 'source': {}, 'reviewable': False, 'active': True}, 'wit_cam_04': {'type': 'csh', 'method': 'mf_csh', 'used_by': [], 'source': {}, 'reviewable': False, 'active': True}, 'wit_cam_05': {'type': 'csh', 'method': 'mf_csh', 'used_by': [], 'source': {}, 'reviewable': False, 'active': True}}


    # lk = get_pub_used_by_task(dt, "animation")
    # print (lk)

    # bb = get_pub_used_by("Test", "sequences",  "TST", '0100', 'animation','HO')
    # print (bb)

    # qw = get_task_imports_from("Test", "sequences",  "DDDD", '0100', 'animation')
    # print (qw)
    # list_of_crap = ['plate_io', 'layout']
    # str = get_pub_used_by("Test", "sequences",  "TST", '0100', 'animation', 'proxy_geo')
    # print (str)
    # jj = db_query("assets", "entry_name", show_name="Now", category="characters",active=True)
    # print(jj)

    # sss = get_entry_definition("Test", "sequences",  "VVV", '0150')
    # print (sss)
    # the_list = (list(sss.keys()))
    # make_nice = xutil.write_nice_names(the_list)
    # print (make_nice)



    # set_task_imports_from("Doom", "shots",  "GGF", "1500", "animation", imports_from=["paint", "cfx", "layout", "compositing", "fx", "roto"])
    # gg = get_task_imports_from("Aliens", "assets", "environment", "cave", "modeling")
    # print gg
    # Aliens
    # assets
    # environment
    # city
    # concept
    # imports_from_list = [u'concept', u'ttss', u'cfx_set', u'rigging']
    # ww = set_task_imports_from("Blade_Runner", "assets", "characters", "hulk", "concept", imports_from_list)
    # pprint.pprint(ww)

    # imports_from_list = [u'concept', u'ttss', u'cfx_set', u'rigging']
    # set_task_imports_from("Aliens", "assets", "environment", "cave", "vbdd", imports_from_list)


    # list_to_insert = [{'images':{'type':'img', 'reviewable':'True', 'active':'True'}},
    #                   {'videos':{'type':'vid', 'reviewable':'True', 'active':'True'}},
    #                   {'pdfs':{'type':'pdf', 'reviewable':'True', 'active':'True'}}]
    # set_task_pub_slot_dict("Blade_Runner", "assets", "characters", "hulk", "modeling", list_to_insert)
    # get_id = xqry.db_q_entry_id("Duda","show", "assets", "characters", "bukka", "entry_id" )
    # omit_sequence ("Doom", "NNO")
    # omit_shot("Doom", "GGF", "1500")
    # remove_entry("Blade_Runner", "sequences", "BHJHU", "0010")
    # kk = get_pub_method("Blade_Runner", "assets", "vehicles", "opel", "modeling", "vport_mat")
    #
    # print (kk)
    # print ("")
    # h = get_show_base_structure("gugu")
    # print (h)
    # # for i in gg:
    #     print (i.items())

    # jj = get_show_base_structure("gugu")
    # print (jj)
    # loo = get_entry_type("Test", "sequences",  "VVV", '0150')
    # print (loo)





