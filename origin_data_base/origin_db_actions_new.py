import uuid
import re
import getpass
from bson import ObjectId
from bson.dbref import DBRef
from origin_utilities import utils as xutil
from origin_utilities.date_time import OriginDateTime
from origin_data_base import origin_templates as otmp
from origin_data_base import origin_templates_query as otmpq
from origin_config import xcg_validation as xvalid
from origin_data_base import xcg_db_connection as xcon
from origin_data_base import OriginEnvar

xnow = OriginDateTime()


class JunkStorage(object):
    pass


class OriginTasksTypes(object):

    @property
    def characters(self):
        return "character"

    @property
    def props(self):
        return 'prop'

    @property
    def environments(self):
        return 'environment'

    @property
    def shots(self):
        return 'shot'


class OriginBranchTypes(object):
    @property
    def build(self):
        return "build"

    @property
    def sequences(self):
        return "shots"

    @property
    def library(self):
        return 'lib_asset'

    @property
    def reference(self):
        return 'ref_asset'


class OriginAssetTypes(object):

    @property
    def build(self):
        return "build"

    @property
    def shot(self):
        return "shots"


class OriginDefaults(object):
    def __init__(self):
        self.db = xcon.server.xchange

    @property
    def root_definitions(self):
        return "definition"

    @property
    def root_tasks(self):
        return "tasks"

    @property
    def tasks_pub_slot(self):
        return "pub_slot"

    def get_show_defaults(self, default_type):
        root_id = OriginId.create_id("root", OriginEnvar.show_name)
        query_path = "show_defaults" + "." + (OriginEnvar.category + "_" + default_type)
        category_tasks = self.db.show.find({"_id": root_id}, {'_id': 0, query_path: 1})

        for data in category_tasks:
            return data["show_defaults"][(OriginEnvar.category + "_" + default_type)]


class OriginId(object):
    """
    Takes a list and joins the elements into a string
    Ex: list = ["element1", "element2"] >>>> result > "element1.element2"
    To be used in generatin ids for the created entities
    """

    @classmethod
    def create_id(cls, *data):
        id_elements = list()
        for elem in data:
            id_elements.append(elem)
        return str(".".join(id_elements))

    @classmethod
    def db_show_id(cls):
        return cls.create_id("root", OriginEnvar.show_name)

    @classmethod
    def db_entry_id(cls):
        return cls.create_id(OriginEnvar.show_name,
                             OriginEnvar.branch_name,
                             OriginEnvar.category,
                             OriginEnvar.entry_name)

    @classmethod
    def db_main_pub_id(cls, version):
        return cls.create_id(OriginEnvar.show_name,
                             OriginEnvar.branch_name,
                             OriginEnvar.category,
                             OriginEnvar.entry_name,
                             version)

    @classmethod
    def db_slot_pub_id(cls, version):
        return cls.create_id(OriginEnvar.show_name,
                             OriginEnvar.branch_name,
                             OriginEnvar.category,
                             OriginEnvar.entry_name,
                             version)


class OriginDbPath(object):

    @classmethod
    def origin_path(cls, *data):
        id_elements = list()
        for elem in data:
            id_elements.append(elem)
        return str(".".join(id_elements))

    @classmethod
    def db_branch_path(cls):
        return cls.origin_path(OriginEnvar.show_name,
                               OriginEnvar.branch_name
                               )

    @classmethod
    def db_category_path(cls):
        return cls.origin_path(OriginEnvar.show_name,
                               OriginEnvar.branch_name,
                               OriginEnvar.category
                               )

    @classmethod
    def db_entry_path(cls):
        return cls.origin_path(OriginEnvar.show_name,
                               OriginEnvar.branch_name,
                               OriginEnvar.category,
                               OriginEnvar.entry_name)

    @classmethod
    def db_task_path(cls):
        return "tasks"

    @classmethod
    def db_task_imp_from(cls):
        return cls.origin_path("tasks", OriginEnvar.task_name, 'imports_from')

    @classmethod
    def db_task_pub(cls):
        return cls.origin_path("tasks", OriginEnvar.task_name, 'pub_slots')

    @classmethod
    def db_task_pub_used_by(cls):
        return cls.origin_path("tasks", OriginEnvar.task_name, 'pub_slots')

    @classmethod
    def db_asset_definition_path(cls):
        return "definition"

    @classmethod
    def db_asset_master_bundle_path(cls):
        return "master_bundle"

    @classmethod
    def db_asset_assignment_path(cls):
        return "assignment"


class OriginDbRef(object):
    @classmethod
    def add_db_id_reference(cls, collection, parent_doc_id, destination_slot, id_to_add, from_collection):
        db = xcon.server.xchange
        db[collection].update_one({"_id": parent_doc_id},
                                  {"$push": {destination_slot: DBRef(from_collection, id_to_add)}})


class OriginCreate(object):
    def __init__(self):
        self.db = xcon.server.xchange

    def db_project(self, name):
        entity_id = OriginId.create_id("root", name)
        try:
            self.db.show.insert_one(
                {
                    "_id": entity_id,
                    "show_code": " ",
                    "show_name": name,
                    "structure": otmp.show_structure(),
                    "show_defaults": {"asset_definition": otmp.entry_definition("build"),
                                      "shots_definition": otmp.entry_definition("shot"),
                                      "characters_tasks": otmp.tasks_schema("character"),
                                      "props_tasks": otmp.tasks_schema("prop"),
                                      "environments_tasks": otmp.tasks_schema("environment"),
                                      "shots_tasks": otmp.tasks_schema("shot")},
                    "active": True,
                    "date": xnow.return_date(),
                    "time": xnow.return_time(),
                    "owner": getpass.getuser(),
                    "show_type": "vfx"
                }
            )
            print("{} show created!".format(name))
        except Exception as e:
            print("{} Error! Nothing created!".format(e))

    def db_show_branch(self, name, branch_type):
        root_id = OriginId().db_show_id()
        insert_entry = "structure" + "." + name
        self.db.show.update_one({"_id": root_id}, {"$set": {insert_entry: {"type": branch_type}}})
        print("{} Origin Branch created!".format(name))
        return name

    def db_category(self, name, tasks_type):
        root_id = OriginId().db_show_id()
        insert_entry = OriginDbPath.origin_path("structure", OriginEnvar.branch_name, name)
        insert_tasks_definition = OriginDbPath.origin_path("show_defaults", (name + "_tasks"))
        insert_definition = OriginDbPath.origin_path("show_defaults", (name + "_definition"))
        self.db.show.update_one({"_id": root_id}, {"$set": {insert_entry: []}})
        self.db.show.update_one({"_id": root_id}, {"$set": {insert_tasks_definition: otmp.tasks_schema(tasks_type)}})
        self.db.show.update_one({"_id": root_id}, {"$set": {insert_definition: otmp.entry_definition(tasks_type)}})
        print("{} Origin Category created!".format(name))
        return name

    def db_asset(self, name):
        root_id = OriginId.db_show_id()
        asset_id = OriginDbPath.origin_path(OriginDbPath.db_category_path(), name)
        collection = self.db[OriginShowQuery().get_branch_type]
        try:
            collection.insert_one(
                {
                    "_id": asset_id,
                    "show_name": OriginEnvar.show_name,
                    "entry_name": name,
                    "type": "build",
                    "category": OriginEnvar.category,
                    "status": " ",
                    "assignment": {},
                    "tasks": OriginDefaults().get_show_defaults(OriginDefaults().root_tasks),
                    "master_bundle": [],
                    "active": True,
                    "definition": OriginDefaults().get_show_defaults(OriginDefaults().root_definitions),
                    "date": xnow.return_date(),
                    "time": xnow.return_time(),
                    "owner": getpass.getuser()
                }
            )
            insert_entry = OriginDbPath.origin_path("structure", OriginEnvar.branch_name, OriginEnvar.category)
            OriginDbRef.add_db_id_reference("show", root_id, insert_entry, asset_id, OriginEnvar.branch_name)
            print("{} Origin Asset created!".format(name))

        except Exception as e:
            print("{} Error! Nothing Created!".format(e))

    def asset_task(self, name):
        asset_id = OriginDbPath().db_entry_path()
        cursor = self.db[OriginQuery().get_branch_type]
        task_db_path = OriginDbPath.origin_path(OriginDbPath.db_task_path(), name)
        tasks_defaults = otmp.task_defaults()
        cursor.update_one({"_id": asset_id}, {"$set": {task_db_path: tasks_defaults}})
        print("{} Origin Asset Task created!".format(name))
        return name

    def task_pub_slot(self, name):
        asset_id = OriginDbPath().db_entry_path()
        cursor = self.db[OriginQuery().get_branch_type]
        task_pub_slot_db_path = OriginDbPath.origin_path(OriginDbPath.db_task_pub(), name)
        tasks_pub_slot_defaults = otmp.tasks_pub_slot_schema()
        cursor.update_one({"_id": asset_id}, {"$set": {task_pub_slot_db_path: tasks_pub_slot_defaults}})
        print("{} Task Pub Slot created!".format(name))
        return name


class OriginShowQuery(object):
    def __init__(self):
        self.db = xcon.server.xchange

    def structure(self):
        try:
            all_assets = self.db.show.find({"_id": OriginId.db_show_id(), "active": True},
                                           {'_id': 0, 'structure': 1})
            for each in list(all_assets):
                return each['structure']
        except:
            pass

    @property
    def get_branch_type(self):
        branch_name = OriginEnvar.branch_name
        try:
            show_structure = self.db.show.find({"_id": OriginId.db_show_id(), "active": True},
                                               {'_id': 0, 'structure': 1})
            for each in list(show_structure):
                return each['structure'][branch_name]["type"]
        except:
            pass

    def db_query(self, db_branch, item, **anchor):
        data = []
        cursor = self.db[db_branch]
        results = cursor.find(anchor, {"_id": 0, item: 1})
        for result in results:
            for k, v in result.items():
                data.append(v)
        return data

    def show_type(self):
        try:
            show_type = self.db.show.find({"_id": OriginId.db_show_id(), "active": True},
                                          {'_id': 0, 'show_type': 1})
            for each in list(show_type):
                return each['show_type']
        except:
            pass

    def get_active(self):
        try:
            shows_list = []
            all_shows = self.db.show.find({"active": True}, {'_id': 0, 'show_name': 1})
            for each in all_shows:
                get_values = list(each.values())
                shows_list.append(get_values[0])
            return shows_list

        except:
            pass

    # def get_all_assets(self):
    #     try:
    #         assets_list = []
    #         db = xcon.server.xchange
    #         all_assets = db.show.find({"_id": OriginId.db_show_id(), "active": True}, {'_id': 0, 'entry_name': 1})
    #         for each in all_assets:
    #             assets_list.append(each['entry_name'])
    #         return assets_list
    #     except:
    #         pass

    # def get_all_shots(self, show_name, category):
    #     try:
    #         shots_list = []
    #         db = xcon.server.xchange
    #         all_shots = db.sequences.find({"show_name": show_name, "category": category, "active": True},
    #                                       {'_id': 0, 'entry_name': 1})
    #         for each in all_shots:
    #             shots_list.append(each['entry_name'])
    #         return shots_list
    #     except:
    #         pass


class OriginEntitiesQuery(object):
    def __init__(self):
        self.db = xcon.server.xchange

    def get_tasks(self):
        try:
            cursor = self.db[OriginShowQuery().get_branch_type]
            tasks_list = cursor.find({"_id": OriginId.db_entry_id()}, {'_id': 0, 'tasks': 1})
            for elements in tasks_list:
                return list(elements["tasks"].keys())
        except:
            pass

    def get_task_definition(self):
        # TODO, needs to be checked for what it is used
        try:
            task_path = OriginDbPath.origin_path("tasks", OriginEnvar.task_name)
            cursor = self.db[OriginShowQuery().get_branch_type]
            tasks_list = cursor.find({"_id": OriginId.db_entry_id()}, {'_id': 0, task_path: 1})
            for tasks in tasks_list:
                return (tasks["tasks"][OriginEnvar.task_name])
        except:
            pass

    def get_task_pub_slots(self):
        try:
            task_path = OriginDbPath.origin_path("tasks", OriginEnvar.task_name, "pub_slots")
            cursor = self.db[OriginShowQuery().get_branch_type]
            tasks_list = cursor.find({"_id": OriginId.db_entry_id()}, {'_id': 0, task_path: 1})
            for tasks in tasks_list:
                for tsk, tsk_name in tasks.items():
                    return list(tsk_name[OriginEnvar.task_name]['pub_slots'])

        except:
            pass

    def get_pub_type(self, pub_slot):
        try:
            task_path = OriginDbPath.origin_path("tasks", OriginEnvar.task_name, "pub_slots", pub_slot, "type")
            cursor = self.db[OriginShowQuery().get_branch_type]
            tasks_list = cursor.find({"_id": OriginId.db_entry_id()}, {'_id': 0, task_path: 1})
            for tasks in tasks_list:
                return tasks['tasks'][OriginEnvar.task_name]["pub_slots"][pub_slot]["type"]

        except:
            pass

    def get_pub_method(self, pub_slot):
        try:
            task_path = OriginDbPath.origin_path("tasks", OriginEnvar.task_name, "pub_slots", pub_slot, "method")
            cursor = self.db[OriginShowQuery().get_branch_type]
            tasks_list = cursor.find({"_id": OriginId.db_entry_id()}, {'_id': 0, task_path: 1})
            for tasks in tasks_list:
                return tasks['tasks'][OriginEnvar.task_name]["pub_slots"][pub_slot]["method"]

        except:
            pass

    def get_pub_used_by(self, pub_slot):
        try:
            task_path = OriginDbPath.origin_path("tasks", OriginEnvar.task_name, "pub_slots", pub_slot, "used_by")
            cursor = self.db[OriginShowQuery().get_branch_type]
            tasks_list = cursor.find({"_id": OriginId.db_entry_id()}, {'_id': 0, task_path: 1})
            for tasks in tasks_list:
                return tasks['tasks'][OriginEnvar.task_name]["pub_slots"][pub_slot]["used_by"]

        except:
            pass

    def get_pub_used_by_task(self, data, task_name):
        get_pub_slots = []
        get_slots = list(data.keys())
        for x in get_slots:
            if task_name in data[x]['used_by']:
                get_pub_slots.append(x)
        return get_pub_slots

    def get_pub_is_reviewable(self, pub_slot):
        try:
            task_path = OriginDbPath.origin_path("tasks", OriginEnvar.task_name, "pub_slots", pub_slot, "reviewable")
            cursor = self.db[OriginShowQuery().get_branch_type]
            tasks_list = cursor.find({"_id": OriginId.db_entry_id()}, {'_id': 0, task_path: 1})
            for tasks in tasks_list:
                return tasks['tasks'][OriginEnvar.task_name]["pub_slots"][pub_slot]["reviewable"]

        except:
            pass

    def get_pub_is_active(self, pub_slot):
        try:
            task_path = OriginDbPath.origin_path("tasks", OriginEnvar.task_name, "pub_slots", pub_slot, "active")
            cursor = self.db[OriginShowQuery().get_branch_type]
            tasks_list = cursor.find({"_id": OriginId.db_entry_id()}, {'_id': 0, task_path: 1})
            for tasks in tasks_list:
                return tasks['tasks'][OriginEnvar.task_name]["pub_slots"][pub_slot]["active"]

        except:
            pass

    def get_task_imports_from(self):
        try:
            task_path = OriginDbPath.origin_path("tasks", OriginEnvar.task_name, "imports_from")
            cursor = self.db[OriginShowQuery().get_branch_type]
            tasks_list = cursor.find({"_id": OriginId.db_entry_id()}, {'_id': 0, task_path: 1})
            for tasks in tasks_list:
                for tsk, tsk_name in tasks.items():
                    return list(tsk_name[OriginEnvar.task_name]['imports_from'])

        except:
            pass

    def get_task_status(self):
        try:
            task_path = OriginDbPath.origin_path("tasks", OriginEnvar.task_name, "status")
            cursor = self.db[OriginShowQuery().get_branch_type]
            tasks_list = cursor.find({"_id": OriginId.db_entry_id()}, {'_id': 0, task_path: 1})
            for tasks in tasks_list:
                return tasks['tasks'][OriginEnvar.task_name]['status']

        except:
            pass

    def get_task_is_active(self):
        try:
            task_path = OriginDbPath.origin_path("tasks", OriginEnvar.task_name, "active")
            cursor = self.db[OriginShowQuery().get_branch_type]
            tasks_list = cursor.find({"_id": OriginId.db_entry_id()}, {'_id': 0, task_path: 1})
            for tasks in tasks_list:
                return tasks['tasks'][OriginEnvar.task_name]['active']

        except:
            pass

    def get_task_user(self):
        try:
            task_path = OriginDbPath.origin_path("tasks", OriginEnvar.task_name, "artist")
            cursor = self.db[OriginShowQuery().get_branch_type]
            tasks_list = cursor.find({"_id": OriginId.db_entry_id()}, {'_id': 0, task_path: 1})
            for tasks in tasks_list:
                return tasks['tasks'][OriginEnvar.task_name]['artist']

        except:
            pass

    def get_entry_definition(self):
        try:
            cursor = self.db[OriginShowQuery().get_branch_type]
            definitions_list = cursor.find({"_id": OriginId.db_entry_id()}, {'_id': 0, 'definition': 1})
            for definitions in definitions_list:
                return definitions['definition']
        except:
            pass

    def get_entry_type(self):
        try:
            cursor = self.db[OriginShowQuery().get_branch_type]
            definitions_list = cursor.find({"_id": OriginId.db_entry_id()}, {'_id': 0, 'type': 1})
            for definitions in definitions_list:
                return definitions['type']
        except:
            pass

    def get_entry_assigned(self):
        try:
            cursor = self.db[OriginShowQuery().get_branch_type]
            definitions_list = cursor.find({"_id": OriginId.db_entry_id()}, {'_id': 0, 'assignment': 1})
            for definitions in definitions_list:
                return definitions['assignment']
        except:
            pass


class OriginUpdate(object):
    def __init__(self):
        self.db = xcon.server.xchange

    def origin_update(self, entity_id, db_path, data=[]):
        cursor = self.db[OriginShowQuery().get_branch_type]
        cursor.update_one({"_id": entity_id}, {"$set": {db_path: data}})

    def task_imports_from(self, imports_from=[]):
        for each in imports_from:
            task_imports_from_address = OriginDbPath.origin_path(OriginDbPath.db_task_imp_from(), each)
            asset_id = OriginId.db_entry_id()
            self.origin_update(asset_id, task_imports_from_address)
            print("{} task added as import_source".format(each))

    def add_task_pub_slot(self, pub_slot=[]):
        for each in pub_slot:
            task_imports_from_address = OriginDbPath.origin_path(OriginDbPath.db_task_pub(), each)
            asset_id = OriginId.db_entry_id()
            self.origin_update(asset_id, task_imports_from_address)
            print("{} added as pub_slot".format(each))

    def task_pub_used_by(self, pub_slot, used_by, remove_action=False):
        cursor = self.db[OriginShowQuery().get_branch_type]
        pub_slot_path = OriginDbPath.origin_path(OriginDbPath().db_task_pub(), pub_slot, "used_by")
        asset_id = OriginId.db_entry_id()

        existing_data = cursor.find_one({"_id": asset_id}, {'_id': 0, pub_slot_path: 1})
        existing_assignment = existing_data['tasks'][OriginEnvar.task_name]['pub_slots'][pub_slot]['used_by']
        if not remove_action:
            if used_by not in existing_assignment:
                cursor.update_one({"_id": asset_id}, {"$push": {pub_slot_path: used_by}})
        else:
            if used_by in existing_assignment:
                cursor.update_one({"_id": asset_id}, {"$pull": {pub_slot_path: used_by}})

    def task_pub_slot_dict(self, pub_slot=[]):
        asset_id = OriginId.db_entry_id()
        for each in pub_slot:
            get_slot_name = (list(each.keys()))
            get_slot_param = (list(each.values()))
            pub_slot_path = OriginDbPath.origin_path(OriginDbPath.db_task_pub(), get_slot_name[0])
            print(pub_slot_path)
            self.origin_update(asset_id, pub_slot_path, get_slot_param[0])
        print("Publish Slot added succesfully!")

    def task_status(self, task_status):
        asset_id = OriginDbPath().db_entry_path()
        db_collection = self.db[OriginShowQuery().get_branch_type]
        db_address = OriginDbPath.origin_path(OriginDbPath.db_task_path(), "status")
        db_collection.update_one({"_id": asset_id}, {'$set': {db_address: task_status}})

    def task_user(self, artist_name):
        asset_id = OriginDbPath().db_entry_path()
        db_collection = self.db[OriginShowQuery().get_branch_type]
        db_address = OriginDbPath.origin_path(OriginDbPath.db_task_path(), "artist")
        db_collection.update_one({"_id": asset_id}, {'$set': {db_address: artist_name}})

    def entry_definition(self, definition):
        db = xcon.server.xchange
        cursor = db[OriginShowQuery().get_branch_type]
        cursor.update({"_id": OriginId.db_entry_id()}, {"$set": {"definition": definition}})
        print("{} Definition Updated!".format(OriginEnvar.entry_name))

    def entity_is_active(self, is_active=True):
        cursor = self.db[OriginShowQuery().get_branch_type]
        cursor.update_one({"_id": OriginId.db_entry_id()},{"$set": {"active": is_active}})
        print("{} Omitted!".format(OriginId.db_entry_id()))

    def task_is_active(self, is_active=True):
        db_collection = self.db[OriginShowQuery().get_branch_type]
        db_address = OriginDbPath.origin_path(OriginDbPath.db_task_path(), "active")
        db_collection.update_one({"_id": OriginId.db_entry_id()}, {'$set': {db_address: is_active}})

    def rem_assets_from_shot(show_name, show_branch, category, entry_name, asset_to_remove):
        pass

    def remove_task_pub_slots(self):
        try:
            task_path = OriginDbPath.db_task_pub()
            print(task_path)
            cursor = self.db[OriginShowQuery().get_branch_type]
            cursor.update_one({"_id": OriginId.db_entry_id()}, {"$unset": {task_path: 1}})
            cursor.update_one({"_id": OriginId.db_entry_id()}, {"$set": {task_path: {}}})
        except:
            pass

    def remove_task_import_slots(self):
        try:
            task_path = OriginDbPath.db_task_imp_from()
            print(task_path)
            cursor = self.db[OriginShowQuery().get_branch_type]
            cursor.update_one({"_id": OriginId.db_entry_id()}, {"$unset": {task_path: 1}})
            cursor.update_one({"_id": OriginId.db_entry_id()}, {"$set": {task_path: {}}})
        except:
            pass

    def remove_entry(self, show_name, branch_category, entry_category, entry_name):
        try:

            show_branches = xvalid.VALID_SHOW_BRANCHES
            if branch_category not in show_branches:
                print("remove_entry")
                print("{} category is not valid. Please enter one of these {}".format(branch_category, show_branches))
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

                print('entry {} deleted from {} collection and removed from {} show structure'.format(entry_name,
                                                                                                      branch_category,
                                                                                                      show_name))


        except:
            pass


class OriginPublish(object):

    def get_sub_branches(show_name, branch_name):
        sub_branches_list = []
        db = xcon.server.xchange
        query_path = "structure" + "." + branch_name
        all_branches = db.show.find({"show_name": show_name, "active": True},
                                    {'_id': 0, query_path: 1})
        for each in list(all_branches):
            sub_branches_list.append(list(each['structure'][branch_name].keys()))
        return sub_branches_list[0]

    def get_sub_branches_content(self, show_name, branch_name, category_name):
        db = xcon.server.xchange
        query_path = "structure" + "." + branch_name + "." + category_name
        all_branches = db.show.find({"show_name": show_name, "active": True},
                                    {'_id': 0, query_path: 1})

        for each in all_branches:
            return (list(each['structure'][branch_name][category_name].keys()))

    # DB_PUBLISHES GETTERS
    def get_db_publishes_ids(self, collection, show_name=None, branch_name=None, category_name=None, entry_name=None,
                             task_name=None, view_limit=0):
        store_value = list()
        db = xcon.server.xchange

        cursor = db[collection]

        if show_name and branch_name and category_name and entry_name and task_name:
            test = cursor.find(
                {"show_name": show_name, "branch": branch_name, "category": category_name, "entry_name": entry_name,
                 "task_name": task_name}).limit(view_limit)
            for publishes in test:
                store_value.append(str(publishes["_id"]))
        elif show_name and branch_name and category_name and entry_name:
            test = cursor.find({"show_name": show_name, "branch": branch_name, "category": category_name,
                                "entry_name": entry_name}).limit(view_limit)
            for publishes in test:
                store_value.append(str(publishes["_id"]))

        elif show_name and branch_name and category_name:
            test = cursor.find({"show_name": show_name, "branch": branch_name, "category": category_name}).limit(
                view_limit)
            for publishes in test:
                store_value.append(str(publishes["_id"]))

        elif show_name and branch_name:
            test = cursor.find({"show_name": show_name, "branch": branch_name}).limit(view_limit)
            for publishes in test:
                store_value.append(str(publishes["_id"]))

        elif show_name:
            test = cursor.find({"show_name": show_name}).limit(view_limit)
            for publishes in test:
                store_value.append(str(publishes["_id"]))

        else:
            test = cursor.find({}).limit(view_limit)
            for publishes in test:
                store_value.append(str(publishes["_id"]))

        return store_value

    def get_db_values(collection, document_id, value_to_return):
        db = xcon.server.xchange
        if not collection or not document_id or collection == None or document_id == None:
            return
        else:
            selected_document = db[collection].find_one({"_id": ObjectId(document_id)})
            return (selected_document[value_to_return])

    def get_published_entries(show_name, branch_category, parent_category, entry_name, task_name):
        db = xcon.server.xchange
        db.publishes.find({"show_name": show_name, "entry_name": entry_name, "task_name": task_name}, {"_id": 0})
        pass

    # DATABASE MISC
    def db_task_ver_increase(self, show_name, entity_type, entity_name, task_name):

        get_versions = xutil.db_find_key("publishes", "version",
                                         show_name=show_name,
                                         category=entity_type,
                                         entry_name=entity_name,
                                         task_name=task_name
                                         )

        if not len(get_versions) < 1:
            conv_to_int = []

            for versions in get_versions:
                conv_to_int.append(versions)

            highest = max(conv_to_int)
            get_digit = re.findall('\d+', highest)

            return "{0}{1:04d}".format("v", (int(get_digit[0]) + 1))

        else:
            return "{0}{1:04d}".format("v", (int(1)))

    def db_pubslot_ver_increase(self, collection_name, show_name, entity_type, entity_name, slot_name):

        get_versions = xutil.db_find_key(collection_name, "version",
                                         show_name=show_name,
                                         category=entity_type,
                                         entry_name=entity_name,
                                         slot_name=slot_name
                                         )

        if not len(get_versions) < 1:
            conv_to_int = []

            for versions in get_versions:
                conv_to_int.append(versions)

            highest = max(conv_to_int)
            get_digit = re.findall('\d+', highest)

            return "{0}{1:04d}".format("v", (int(get_digit[0]) + 1))

        else:
            return "{0}{1:04d}".format("v", (int(1)))

    def db_master_bundle_ver_increase(self, collection_name, show_name, entity_type, entity_name):

        get_versions = xutil.db_find_key(collection_name, "version",
                                         show_name=show_name,
                                         category=entity_type,
                                         entry_name=entity_name
                                         )

        if not len(get_versions) < 1:
            conv_to_int = []

            for versions in get_versions:
                conv_to_int.append(versions)

            highest = max(conv_to_int)
            get_digit = re.findall('\d+', highest)

            return "{0}{1:04d}".format("v", (int(get_digit[0]) + 1))

        else:
            return "{0}{1:04d}".format("v", (int(1)))

    def db_publish(self, show_name, branch_name, category, entry_name, task_name, bundle_type, bundle_version, status):

        version = self.db_task_ver_increase(show_name, category, entry_name, task_name)
        set_display_name = "_".join([entry_name, "main_publish"])

        common_id = ObjectId()
        db = xcon.server.xchange
        collection_name = "_".join(["publishes"])
        published = db[collection_name].insert_one({
            "_id": common_id,
            "reviewable_component": "insert_movie",
            "show_name": show_name,
            "entry_name": entry_name,
            "category": category,
            "branch": branch_name,
            "task_name": task_name,
            "status": status,
            "description": [],
            "artist": get_current_user(),
            "version": version,
            "date": xnow.return_date(),
            "time": xnow.return_time(),
            "publish_packaging": "main",
            "publishing_slots": [],
            "display_name": set_display_name,
            "bundle_type": bundle_type,
            "bundle_version": bundle_version
        }
        )

        xcon.server.close()
        print("{0} Main Publish Done!".format(set_display_name))
        return (published.inserted_id), collection_name

    def pub_slot_publish(show_name, branch_name, category, entry_name, task_name, pub_slot):
        collection_name_elem = ["publish", "slots", task_name]
        collection_name = "_".join(collection_name_elem)
        version = db_pubslot_ver_increase(collection_name, show_name, category, entry_name, pub_slot)
        set_display_name = ["pubslot", pub_slot, task_name]
        status = "PENDING-REVIEW"
        build_server_path = [show_name, branch_name, category, entry_name, task_name, version, pub_slot]
        common_id = ObjectId()

        main_path = 'project/branch/category/entry/task/output/version/slot/file.ext'
        review_images_path = 'project/branch/category/entry/data/task/version/slot/reviewable/file_v001.####.exr'
        review_video_path = 'project/branch/category/entry/data/task/version/slot/reviewable/file_v001.mov'
        preview_video_path = 'project/branch/category/entry/data/task/version/slot/reviewable/file_v001_preview.mov'
        used_template_path = 'project/branch/category/templates/task/versions/template_v001.scene'
        work_file_path = 'project/branch/category/entry/task/output/versions/origin_file.scene'
        origin = {'input': 'task/imports_from/slot/version/file.ext', 'link': 'insert_link'}
        bundle = 'current_bundle'

        db = xcon.server.xchange
        published_slot = db[collection_name].insert_one({
            "_id": common_id,
            "reviewable_component": "insert_movie_path",
            "slot_thumbnail": "insert_thumbnail_path",
            "show_name": show_name,
            "entry_name": entry_name,
            "category": category,
            "branch": branch_name,
            "task_name": task_name,
            "artist": get_current_user(),
            "slot_name": pub_slot,
            "status": status,
            "version_origin": "created",
            "version": version,
            "date": xnow.return_date(),
            "time": xnow.return_time(),
            "publish_packaging": "slots",
            "parent_collection": collection_name,
            "display_name": "_".join(set_display_name),
            "output_path": build_server_path,
            "components": {"path": main_path,
                           "rc_source_images": review_images_path,
                           "rc_source_video": review_video_path,
                           "rc_preview": preview_video_path,
                           "template": used_template_path,
                           "work_file": work_file_path,
                           "chain": origin,
                           "bundle": bundle},
            "rc_output_path": "_path"
        }
        )

        xcon.server.close()
        print("{0} slot has been published".format(pub_slot))
        return (published_slot.inserted_id), collection_name

    def create_master_bundle(show_name, branch_name, category, entry_name):
        status = "PENDING-REVIEW"
        collection_name = "bundles"
        common_id = ObjectId()
        entity_tasks = get_tasks(show_name, branch_name, category, entry_name)
        version = db_master_bundle_ver_increase(collection_name, show_name, category, entry_name)
        set_display_name = [entry_name, "master_bundle"]

        db = xcon.server.xchange
        published_slot = db[collection_name].insert_one({
            "_id": common_id,
            "show_name": show_name,
            "entry_name": entry_name,
            "category": category,
            "branch": branch_name,
            "display_name": "_".join(set_display_name),
            "artist": get_current_user(),
            "status": status,
            "version": version,
            "date": xnow.return_date(),
            "time": xnow.return_time(),
            "bundle_slots": dict.fromkeys(entity_tasks, [])
        }
        )

        xcon.server.close()
        print("{0} bundle has been published".format("_".join(set_display_name)))
        return published_slot.inserted_id, collection_name

    def select_entity(collection, show_name, branch_name, category, entry_name, version):
        bundle_slots = list()
        db = xcon.server.xchange
        select_bundle = db[collection].find(
            {"show_name": show_name, "branch": branch_name, "category": category, "entry_name": entry_name,
             "version": version})
        for slots in select_bundle:
            bundle_slots.append(slots)

        return bundle_slots[0]

    def add_db_id_reference(collection, parent_doc_id, parent_doc_slot, id_to_add, from_collection):
        db = xcon.server.xchange
        db[collection].update_one({"_id": ObjectId(parent_doc_id)},
                                  {"$push": {parent_doc_slot: DBRef(from_collection, id_to_add)}})

    def get_db_referenced_attr(self, source_collection, source_id, source_attr, find_attr):
        db = xcon.server.xchange
        list_attr = list()
        if not source_id or source_id == None:
            return
        else:
            id_list = db[source_collection].find_one({"_id": ObjectId(source_id)})
            for each_id in id_list[source_attr]:
                attr_data = (db.dereference(each_id)[find_attr])
                list_attr.append(attr_data)
            return list_attr

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
                "date": xnow.return_date(),
                "time": xnow.return_time(),
                "created_by": getpass.getuser()

            }
        )
        print(" user for {} created!".format(first_name + " " + name))
        pass

    def get_current_user():
        username = getpass.getuser()
        return username


if __name__ == "__main__":
    from origin_data_base import OriginEnvar

    OriginEnvar.show_name = "Mofo"
    OriginEnvar.branch_name = "library_"
    OriginEnvar.category = "TTT"
    OriginEnvar.entry_name = "102255"
    OriginEnvar.task_name = "animation"

    c = OriginCreate()
    # c.task_pub_slot("Test_Slot02")
    #
    #
    # c = OriginId.db_show_id()
    # print(c)
    # db_paths = OriginDbPath.db_task_imp_from()
    # print(db_paths)
    #
    # db_update = OriginUpdate()
    # db_update.task_imports_from(['testCCC','testB','testBBBBB'])
    # db_update.update_task_is_active(False)
    # db_update.update_task_pub_slot(['slot1', 'slot2', 'slot3'])
    # db_update.update_task_pub_slot_dict([{"proj":{}}])

    ocreate = OriginCreate()
    # ocreate.db_project(name="Mofo")
    # ocreate.db_show_branch(name="library_", branch_type=OriginBranchTypes().library)
    # ocreate.db_category(name="TTT", tasks_type=OriginTasksTypes().shots)
    # ocreate.db_asset(name="xx-xx")
    # ocreate.asset_task(name="another")

    oq = OriginUpdate()
    tsk_cont = oq.remove_all_task_import_slots()
    print(tsk_cont)

    # oquery = OriginShowQuery()
    # ff = oquery.structure()
    # ttt = oquery.show_type()
    # print(ff)
    # print(ttt)

    # OriginQuery.show(OriginPath.definition, OriginType.content)
    # OriginCreate.Asset().at_path()
    # print (ocreate)

    import pprint
    # import os
    # import getpass
    #
    # db = xcon.server.xchange
    #
    # os.environ['XCG_PROJECT'] = 'Test'
    # os.environ['XCG_PROJECT_BRANCH'] = 'assets'
    # os.environ['XCG_PROJECT_CATEGORY'] = 'characters'
    # os.environ['XCG_PROJECT_ENTITY'] = 'hulk'
    # os.environ['XCG_ENTITY_TASK'] = 'modeling'
    # #
    # #
    # show_name = os.environ.get('XCG_PROJECT')
    # branch_name = os.environ.get('XCG_PROJECT_BRANCH')
    # category_name = os.environ.get('XCG_PROJECT_CATEGORY')
    # entity_name = os.environ.get('XCG_PROJECT_ENTITY')
    # task_name = os.environ.get('XCG_ENTITY_TASK')
    #
    # current_user = get_current_user()
    #
    # v = get_tasks(show_name, branch_name, category_name, entity_name)
    #
    # # components = get_pub_slots(show_name, branch_name, category_name, entity_name, task_name)
    # # main_publish = db_publish(show_name, branch_name, category_name, entity_name, task_name, branch_name, "0012",
    # #                           "PENDING-REVIEW")
    # # for component in components:
    # #     secondary_publish = pub_slot_publish(show_name, branch_name, category_name, entity_name, task_name, component)
    # #     add_db_id_reference(main_publish[1], main_publish[0], "publishing_slots", secondary_publish[0],secondary_publish[1])
    #
    # create_master_bundle(show_name, branch_name, category_name, entity_name)
    # v = select_entity("bundles", show_name, branch_name, category_name, entity_name,"v0001")
    # p = select_entity("publishes", show_name, branch_name, category_name, entity_name, "v0001")
    # path_elements = ['bundle_slots', task_name]
    # path_to_write = '.'.join(path_elements)
    # bb = add_db_id_reference("bundles", str(v["_id"]), path_to_write, str(p["_id"]),"publishes")

    # cc = get_db_publishes_ids ("publishes", "Dark", "assets", "characters", "nuoa")

    # pprint.pprint (cc)

    # db = xcon.server.xchange
    # # doc_id = '60adf11a9d8e3f8d996f58f5'
    # doc_id = ''
    #
    # # id_list = get_db_entity_attr_content('publishes', doc_id, 'publishing_slots')
    # # for each_id in id_list:
    # #     print(db.dereference(each_id)['slot_name'])
    # vv = get_db_referenced_attr('publishes', doc_id, 'publishing_slots', 'parent_collection')
    # print (type(ObjectId))
    # print (vv)

    # report_back = db.publishes.find_one({"show_name":show_name, "entry_name":entity_name, "version":"v0001", "task_name":task_name},{"_id":0})
    # x = (report_back["publishing_slots"])
    # print (report_back["publishing_slots"])
    # for each in x:
    #     get_back = db[collection_name].find_one({"_id": each})
    #     print (get_back)

    # vv = get_pub_slots(show_name, branch_name, category_name, entity_name, task_name)
    # pprint.pprint(vv)

    # bb = get_db_publishes_ids("publishes")
    # pprint.pprint(bb)

    # cc = get_sub_branches_content('Test', 'sequences', 'TST')
    # print (cc)
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

    # gg = get_tasks_package("Test", "assets",  "characters", "greenHulk")
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
    # Hi Anna

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

    # sh = get_all_active_shows()
    # print (sh)
    #
    # h = get_show_branches_structure("Test")
    # print (h)
    #
    # sub = get_sub_branches("Test", "assets")
    # print (sub)
