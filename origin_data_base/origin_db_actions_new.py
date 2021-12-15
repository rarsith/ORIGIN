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

class JunkStorage():
    def db_asset_category(self, name, category_type):
        root_id = OriginId.create_id("root", OriginEnvar.show_name)
        insert_entry = OriginDbPath.origin_path("structure", "assets", name)
        insert_definition = OriginDbPath.origin_path("show_defaults", (name + "_tasks"))
        self.db.show.update_one({"_id": root_id}, {"$set": {insert_entry: []}})
        self.db.show.update_one({"_id":root_id},{"$set": {insert_definition:otmp.tasks_schema(category_type)}})
        print("{} category created".format(name))
        return name

    def db_shot_category(self, name, category_type):
        root_id = OriginId.create_id("root", OriginEnvar.show_name)
        insert_entry = OriginDbPath.origin_path("structure", OriginEnvar.branch_name, name)
        insert_definition = OriginDbPath.origin_path("show_defaults",(name + "_tasks"))
        self.db.show.update_one({"_id": root_id},{"$set": {insert_entry:[]}})
        self.db.show.update_one({"_id": root_id},{"$set": {insert_definition:otmp.tasks_schema(category_type)}})
        print ("{} sequence created".format(name))
        return name

class OriginTasksTypes():

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

class OriginBranchTypes():
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

class OriginAssetTypes():
    def __init__(self):
        self.db = xcon.server.xchange

    @classmethod
    def build(cls):
        pass

    @classmethod
    def shot(cls):
        pass

class OriginDefaults():
    def __init__(self):
        self.db = xcon.server.xchange

    @property
    def root_definitions(self):
        return "definition"

    @property
    def root_tasks(self):
        return "tasks"

    def get_show_defaults(self, default_type):
        root_id = OriginId.create_id("root", OriginEnvar.show_name)
        query_path = "show_defaults" + "." + (OriginEnvar.category + "_" + default_type)
        category_tasks = self.db.show.find({"_id": root_id},{'_id': 0, query_path: 1})

        for data in category_tasks:
            return data["show_defaults"][(OriginEnvar.category + "_" + default_type)]

class OriginId():
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
        return cls.create_id("root",OriginEnvar.show_name)

    @classmethod
    def db_entry_id(cls):
        return cls.create_id(OriginEnvar.show_name,
                              OriginEnvar.branch_name,
                              OriginEnvar.category,
                              OriginEnvar.entry_name)


class OriginDbPath():

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
        return cls.origin_path(OriginEnvar.show_name,
                                        OriginEnvar.branch_name,
                                        OriginEnvar.category,
                                        OriginEnvar.entry_name,
                                        "tasks")

    @classmethod
    def db_task_imp_from(cls):
        return cls.origin_path("tasks", OriginEnvar.task_name, 'imports_from')

    @classmethod
    def db_task_pub(cls):
        return cls.origin_path("tasks", OriginEnvar.task_name,'pub_slots')

    @classmethod
    def db_task_pub_used_by(cls):
        return cls.origin_path("tasks", OriginEnvar.task_name, 'pub_slots')

    @classmethod
    def db_asset_definition_path(cls):
        return cls.origin_path(OriginEnvar.show_name,
                               OriginEnvar.branch_name,
                               OriginEnvar.category,
                               OriginEnvar.entry_name,
                               "definition")

    @classmethod
    def db_asset_master_bundle_path(cls):
        return cls.origin_path(OriginEnvar.show_name,
                               OriginEnvar.branch_name,
                               OriginEnvar.category,
                               OriginEnvar.entry_name,
                               "master_bundle")

    @classmethod
    def db_asset_assignment_path(cls):
        return cls.origin_path(OriginEnvar.show_name,
                               OriginEnvar.branch_name,
                               OriginEnvar.category,
                               OriginEnvar.entry_name,
                               "assignment")


class OriginDbRef():
    @classmethod
    def add_db_id_reference(cls, collection, parent_doc_id, destination_slot, id_to_add, from_collection):
        db = xcon.server.xchange
        db[collection].update_one({"_id":parent_doc_id}, {"$push":{destination_slot:DBRef(from_collection, id_to_add)}})

class OriginCreate():
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
                    "structure":{"sequences":{},"assets":{'characters':[], 'environments':[], 'props':[]}},
                    "show_defaults":{"asset_definition":otmp.entry_definition("build"),
                                     "shots_definition":otmp.entry_definition("shot"),
                                     "characters_tasks":otmp.tasks_schema("character"),
                                     "props_tasks":otmp.tasks_schema("prop"),
                                     "environments_tasks":otmp.tasks_schema("environment"),
                                     "shots_tasks":otmp.tasks_schema("shot")},
                    "active": True,
                    "date": xnow.return_date(),
                    "time": xnow.return_time(),
                    "owner":getpass.getuser(),
                    "show_type":"vfx"
                }
            )
            print ("{} show created!".format(name))
        except Exception as e:
            print ("{} Error! Nothing created!".format(e))

    def db_branch(self, name, branch_type):
        get_root = OriginEnvar.show_name
        sel_id = OriginId.create_id("root", get_root)
        collection_anchor = OriginId.create_id("anchor", name)
        insert_entry = "structure" + "." + name
        self.db[name].insert_one({"_id":collection_anchor})
        self.db.show.update_one({"_id":sel_id},{"$set": {insert_entry: {"type":branch_type}}})
        print ("{} Origin Branch created!".format(name))
        return name

    def db_category(self, name, tasks_type):
        root_id = OriginDbPath().db_show_path()
        insert_entry = OriginDbPath.origin_path("structure", OriginEnvar.branch_name, name)
        insert_tasks_definition = OriginDbPath.origin_path("show_defaults", (name + "_tasks"))
        insert_definition = OriginDbPath.origin_path("show_defaults", (name + "_definition"))
        self.db.show.update_one({"_id": root_id}, {"$set": {insert_entry: []}})
        self.db.show.update_one({"_id": root_id}, {"$set": {insert_tasks_definition: otmp.tasks_schema(tasks_type)}})
        self.db.show.update_one({"_id": root_id}, {"$set": {insert_definition: otmp.entry_definition(tasks_type)}})
        print("{} Origin Category created!".format(name))
        return name

    def db_asset(self, name):
        root_id = OriginDbPath.db_show_path()
        asset_id = OriginDbPath.db_category_path()
        collection = self.db[OriginEnvar.branch_name]
        try:
            collection.insert_one(
                {
                    "_id": asset_id,
                    "show_name": OriginEnvar.show_name,
                    "entry_name": name,
                    "type": "asset",
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
            print ("{} Error! Nothing Created!".format(e))

    def create_task(self, name):
        asset_id = OriginDbPath().db_entry_path()
        cursor = self.db[OriginEnvar.branch_name]
        task_db_path = OriginDbPath.origin_path("tasks", name)
        tasks_defaults = otmp.task_defaults()
        cursor.update_one({"_id": asset_id},{"$set": {task_db_path: tasks_defaults}})
        print("{} Origin Asset Task created!".format(name))
        return name

class OriginQuery():
    def db_query(db_branch, item, **anchor):
        db = xcon.server.xchange
        data = []
        cursor = db[db_branch]
        results = cursor.find(anchor, {"_id": 0, item: 1})
        for result in results:
            for k, v in result.items():
                data.append(v)
        return data

    pass

class OriginUpdate():
    def __init__(self):
        self.db = xcon.server.xchange

    def origin_update(self, entity_id, db_path, data=[]):
        cursor = self.db[OriginEnvar.branch_name]
        cursor.update_one({"_id": entity_id}, {"$set": {db_path:data}})

    def task_imports_from(self, imports_from=[]):
        for each in imports_from:
            task_imports_from_address = OriginDbPath.origin_path(OriginDbPath.db_task_imp_from(), each)
            asset_id = OriginId.db_entry_id()
            self.origin_update(asset_id, task_imports_from_address)
            print("{} task added as import_source".format(each))

    def update_task_pub_slot(self, pub_slot=[]):
        for each in pub_slot:
            task_imports_from_address = OriginDbPath.origin_path(OriginDbPath.db_task_pub(), each)
            asset_id = OriginId.db_entry_id()
            self.origin_update(asset_id, task_imports_from_address)
            print("{} added as pub_slot".format(each))

    def update_task_pub_used_by(self, pub_slot, used_by, remove_action=False):
        cursor = self.db[OriginEnvar.branch_name]
        pub_slot_path = OriginDbPath.origin_path(OriginDbPath().db_task_pub(), pub_slot,"used_by")
        asset_id = OriginId.db_entry_id()

        existing_data = cursor.find_one({"_id": asset_id}, {'_id': 0, pub_slot_path: 1})
        existing_assignment = existing_data['tasks'][OriginEnvar.task_name]['pub_slots'][pub_slot]['used_by']
        if not remove_action:
            if used_by not in existing_assignment:
                cursor.update_one({"_id": asset_id},{"$push": {pub_slot_path: used_by}})
        else:
            if used_by in existing_assignment:
                cursor.update_one({"_id": asset_id},{"$pull": {pub_slot_path: used_by}})

    def update_task_pub_slot_dict(self, pub_slot=[]):
        asset_id = OriginId.db_entry_id()
        for each in pub_slot:
            get_slot_name = (list(each.keys()))
            get_slot_param = (list(each.values()))
            pub_slot_path = OriginDbPath.origin_path(OriginDbPath.db_task_pub(), get_slot_name[0])
            print(pub_slot_path)
            self.origin_update(asset_id, pub_slot_path, get_slot_param[0])
        print("Publish Slot added succesfully!")

    def update_task_status(self, task_status):
        asset_id = OriginDbPath().db_entry_path()
        db_collection = self.db[OriginEnvar.branch_name]
        db_address = OriginDbPath.origin_path(OriginDbPath.db_task_path(),"status")
        db_collection.update_one({"_id": asset_id}, {'$set': {db_address: task_status}})

    def update_task_is_active(self, is_active=True):
        asset_id = OriginDbPath().db_entry_path()
        db_collection = self.db[OriginEnvar.branch_name]
        db_address = OriginDbPath.origin_path(OriginDbPath.db_task_path(), "active")
        db_collection.update_one({"_id": asset_id}, {'$set': {db_address: is_active}})

    def update_task_user(self, artist_name):
        asset_id = OriginDbPath().db_entry_path()
        db_collection = self.db[OriginEnvar.branch_name]
        db_address = OriginDbPath.origin_path(OriginDbPath.db_task_path(), "artist")
        db_collection.update_one({"_id": asset_id}, {'$set': {db_address: artist_name}})

    def update_asset_category(show_name, asset_name, asset_category):
        # create/connect to show database
        db = xcon.server.xchange
        db.assets.update({"show_name": show_name, "entry_name": asset_name},
                         {'$set': {"category": asset_category}})
        db.show.update({"show_name": show_name, "structure.assets.entry_name": asset_name},
                       {"$set": {"assets.category": asset_category}})

    def update_entry_definition(show_name, branch_category, parent_category, entry_name, definition):
        db = xcon.server.xchange
        cursor = db[branch_category]
        cursor.update({"show_name": show_name, "entry_name": entry_name, "category": parent_category},
                      {"$set": {"definition": definition}})

        print("{} definition Updated!".format(entry_name))
    pass

class OriginPublish():
    pass

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
    # def db_content_summary(show_name, object_type):
    #     """Returns the content of the assets or the shots, paired with the parent category/sequence.
    #     To be used to create arrays of dictionaries to be queried for the existence of an item."""
    #     valid_object_types = ['assets','shots','sequences','show', 'publishes']
    #     db = xcon.server.xchange
    #     items_in_collection = []
    #     if object_type not in valid_object_types:
    #         print ("Invalid category. Try one of these {}" .format(valid_object_types))
    #
    #     elif object_type == "show":
    #         cursor = db.show
    #         items = cursor.find({}, {"_id": 0, "show_name":1})
    #         for item in items:
    #             items_in_collection.append(item)
    #
    #     elif object_type == "assets":
    #         cursor = db.assets
    #         items = cursor.find({"show_name":show_name}, {"_id": 0, "entry_name": 1, "category":1, "show_name":1})
    #         for item in items:
    #             items_in_collection.append(item)
    #
    #     elif object_type == "sequences":
    #         cursor = db.sequences
    #         items = cursor.find({"show_name":show_name}, {"_id": 0, "entry_name": 1, "show_name":show_name})
    #         for item in items:
    #             items_in_collection.append(item)
    #
    #     elif object_type == "publishes":
    #         cursor = db.publishes
    #         items = cursor.find({"show_name":show_name}, {"_id": 0, "show_name":1, "entity_name":1, "published_by":1, "version":1, "category":1})
    #         for item in items:
    #             items_in_collection.append(item)
    #
    #     return items_in_collection
    ######

    ######
    def get_sub_branches(show_name, branch_name):
        sub_branches_list = []
        db = xcon.server.xchange
        query_path = "structure"+"."+branch_name
        all_branches = db.show.find({"show_name": show_name, "active": True},
                                         {'_id': 0, query_path: 1})
        for each in list(all_branches):
            sub_branches_list.append(list(each['structure'][branch_name].keys()))
        return sub_branches_list[0]

    def get_sub_branches_content(show_name, branch_name, category_name):
        db = xcon.server.xchange
        query_path = "structure" + "." + branch_name + "." + category_name
        all_branches = db.show.find({"show_name": show_name, "active": True},
                                         {'_id': 0, query_path: 1})

        for each in all_branches:
            return (list(each['structure'][branch_name][category_name].keys()))
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

    # def define_branches():
    #     pass
    #
    # def define_categories():
    #     pass
    #
    # def define_tasks_schemas():
    #     pass
    #
    # def define_chains():
    #     pass
    #
    # def define_db_hierachy():
    #     pass

    # def create_show(show_name, code_name, show_type):
    #     # create/connect to show database
    #     # TODO, need checking if show already exists, if True then halt
    #     get_items = db_content_summary(show_name, "show")
    #     search_combo = {"show_name": show_name}
    #     if search_combo in get_items:
    #         print ("{}} show already exists!".format(show_name))
    #     else:
    #         db = xcon.server.xchange
    #         # Create a collection that contains all shows with their specifications
    #         db.show.insert(
    #             {
    #                 "show_code": code_name,
    #                 "show_name": show_name,
    #                 "structure":{"sequences":{},"assets":{'characters':{}, 'environments':{}, 'props':{}}},
    #                 "show_defaults":{"asset_definition":{},
    #                                  "shots_definition":otmp.entry_definition("shot"),
    #                                  "characters_tasks":otmp.tasks_schema("character"),
    #                                  "props_tasks":otmp.tasks_schema("prop"),
    #                                  "environments_tasks":otmp.tasks_schema("environment"),
    #                                  "shots_tasks":otmp.tasks_schema("shot")},
    #                 "active": True,
    #                 "date": xnow.return_date(),
    #                 "time": xnow.return_time(),
    #                 "owner":getpass.getuser(),
    #                 "show_type":show_type
    #             }
    #         )
    #         print ("{} show created!".format(show_name))

    # def create_show_branch(show_name, branch_name):
    #     db = xcon.server.xchange
    #     # update "show" collection for easy navigation
    #     cursor = db[branch_name]
    #     cursor.insert({})
    #
    #     insert_entry = "structure" + "." + branch_name
    #     db.show.update({"show_name": show_name},
    #                         {"$set": {insert_entry: {}}})
    #
    #     print ("{} show_branch created".format(branch_name))

    # def create_sequence(show_name, seq_name):
    #     db = xcon.server.xchange
    #     insert_entry = "structure" + "." + "sequences" + "." + seq_name
    #     insert_definition = "show_defaults" + "." + (seq_name + "_" + "tasks")
    #     db.show.update({"show_name": show_name},
    #                         {"$set": {insert_entry:{}}})
    #
    #     db.show.update({"show_name": show_name},
    #                         {"$set": {insert_definition:otmp.tasks_schema("shot")}})
    #     print ("{} sequence created".format(seq_name))

    # def create_assets_category(show_name, category_name, category_type):
    #     db = xcon.server.xchange
    #     insert_entry = "structure" + "." + "assets" + "." + category_name
    #     insert_definition = "show_defaults" + "." + (category_name + "_" + "tasks")
    #     db.show.update({"show_name": show_name},
    #                         {"$set": {insert_entry:{}}})
    #
    #     db.show.update({"show_name": show_name},
    #                    {"$set": {insert_definition:otmp.tasks_schema(category_type)}})
    #
    #     print ("{} asset_category created".format(category_name))

    # def create_shot(show_name, category, entry_name, status ='NOT-STARTED', definition = xvalid.VALID_SHOTS_TYPES):
    #
    #     db = xcon.server.xchange
    #     db.sequences.insert({
    #                     "show_name": show_name,
    #                     "entry_name": entry_name,
    #                     "type": "shot",
    #                     "category":category,
    #                     "status": status,
    #                     "content":[],
    #                     "tasks": otmpq.get_show_defaults(show_name,category,"tasks"),
    #                     "master_bundle": {},
    #                     "active": True,
    #                     "definition":otmpq.get_show_defaults(show_name,"shots","definition"),
    #                     "date": xnow.return_date(),
    #                     "time": xnow.return_time(),
    #                     "owner": getpass.getuser()
    #     }
    #     )
    #
    #     insert_entry = "structure" + "." + "sequences" + "." + category + "." + entry_name
    #     db.show.update({"show_name": show_name},
    #                         {"$set": {insert_entry:{}}})
    #
    #     print ("{} Shot Created!".format(entry_name))

    # def create_asset(show_name, category, entry_name, status ='NOT-STARTED', definition = xvalid.DEFAULT_ASSET_DEFINITION):
    #     db = xcon.server.xchange
    #     db.assets.insert(
    #         {
    #             "show_name": show_name,
    #             "entry_name": entry_name,
    #             "type": "asset",
    #             "category": category,
    #             "status": status,
    #             "assignment": {},
    #             "tasks": otmpq.get_show_defaults(show_name,category,"tasks"),
    #             "master_bundle":[],
    #             "active": True,
    #             "definition": definition,
    #             "date": xnow.return_date(),
    #             "time": xnow.return_time(),
    #             "owner": getpass.getuser()
    #         }
    #     )
    #
    #     insert_entry = "structure" + "." + "assets" + "." + category + "." + entry_name
    #
    #     db.show.update({"show_name": show_name},
    #                         {"$set": {insert_entry: {}}})
    #
    #     print ("{} Asset Created!".format(entry_name))

    def create_task(show_name, branch_category, parent_category, entry_name, task_name):
        db = xcon.server.xchange
        cursor = db[branch_category]
        shot_task_address = "tasks" + "." + task_name

        tasks_defaults = otmp.task_defaults()

        cursor.update({"show_name": show_name, "entry_name": entry_name, "category":parent_category},
                        {"$set": {shot_task_address: tasks_defaults}})

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

    def add_asset_to_shot02(show_name, seq_name, shot_name, asset_name, asset_category, asset_count):
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
                current = cursor.find({'show_name': show_name,'entry_name':shot_name, 'category':seq_name}, {'_id': 0, 'content':1})
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
                current = cursor.find({'show_name': show_name,'entry_name':shot_name, 'category':seq_name}, {'_id': 0, 'content':1})
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
                    for tasks, task_name in elements.items():
                        entry_tasks.append(list(task_name.keys()))

                return entry_tasks
        except:
            pass

    def get_tasks(show_name, branch_category, parent_category, entry_name, active=True):
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
    #DB_PUBLISHES GETTERS
    def get_db_publishes_ids(collection, show_name = None, branch_name = None, category_name = None, entry_name = None, task_name = None,  view_limit=0):
        store_value = list()
        db = xcon.server.xchange

        cursor = db[collection]

        if show_name and branch_name and category_name and entry_name and task_name:
            test = cursor.find({"show_name": show_name, "branch":branch_name, "category":category_name, "entry_name": entry_name, "task_name":task_name}).limit(view_limit)
            for publishes in test:
               store_value.append(str(publishes["_id"]))
        elif show_name and branch_name and category_name and entry_name:
            test = cursor.find({"show_name": show_name, "branch":branch_name, "category":category_name, "entry_name": entry_name}).limit(view_limit)
            for publishes in test:
               store_value.append(str(publishes["_id"]))

        elif show_name and branch_name and category_name:
            test = cursor.find({"show_name": show_name, "branch": branch_name, "category": category_name}).limit(view_limit)
            for publishes in test:
                store_value.append(str(publishes["_id"]))

        elif show_name and branch_name:
            test = cursor.find({"show_name":show_name, "branch":branch_name}).limit(view_limit)
            for publishes in test:
               store_value.append(str(publishes["_id"]))

        elif show_name:
            test = cursor.find({"show_name":show_name}).limit(view_limit)
            for publishes in test:
               store_value.append(str(publishes["_id"]))

        else:
            test = cursor.find({}).limit(view_limit)
            for publishes in test:
                store_value.append(str(publishes["_id"]))


        return store_value

    def get_db_values(collection, document_id, value_to_return):
        db = xcon.server.xchange
        if not collection or not document_id or collection==None or document_id==None:
            return
        else:
            selected_document = db[collection].find_one({"_id": ObjectId(document_id)})
            return (selected_document[value_to_return])

    def get_published_entries(show_name, branch_category, parent_category, entry_name, task_name):
        db = xcon.server.xchange
        db.publishes.find({"show_name": show_name, "entry_name": entry_name, "task_name": task_name}, {"_id": 0})
        pass
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

    def db_task_ver_increase(show_name, entity_type, entity_name, task_name):

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

    def db_pubslot_ver_increase(collection_name, show_name, entity_type, entity_name, slot_name):

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

    def db_master_bundle_ver_increase(collection_name, show_name, entity_type, entity_name):

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

    def db_publish(show_name, branch_name, category, entry_name, task_name, bundle_type, bundle_version, status):

        version = db_task_ver_increase(show_name, category, entry_name, task_name)
        set_display_name = "_".join([entry_name, "main_publish"])

        common_id = ObjectId()
        db = xcon.server.xchange
        collection_name = "_".join(["publishes"])
        published = db[collection_name].insert_one({
                                            "_id": common_id,
                                            "reviewable_component":"insert_movie",
                                            "show_name": show_name,
                                            "entry_name": entry_name,
                                            "category": category,
                                            "branch": branch_name,
                                            "task_name": task_name,
                                            "status": status,
                                            "description":[],
                                            "artist": get_current_user(),
                                            "version": version,
                                            "date": xnow.return_date(),
                                            "time": xnow.return_time(),
                                            "publish_packaging": "main",
                                            "publishing_slots": [],
                                            "display_name":set_display_name,
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
        origin = {'input':'task/imports_from/slot/version/file.ext', 'link':'insert_link'}
        bundle = 'current_bundle'


        db = xcon.server.xchange
        published_slot = db[collection_name].insert_one({
                                                        "_id": common_id,
                                                        "reviewable_component": "insert_movie_path",
                                                        "slot_thumbnail":"insert_thumbnail_path",
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
                                                        "components":{"path":main_path,
                                                                      "rc_source_images":review_images_path,
                                                                      "rc_source_video":review_video_path,
                                                                      "rc_preview":preview_video_path,
                                                                      "template":used_template_path,
                                                                      "work_file":work_file_path,
                                                                      "chain":origin,
                                                                      "bundle":bundle},
                                                        "rc_output_path":"_path"
                                                    }
                                                    )

        xcon.server.close()
        print ("{0} slot has been published".format(pub_slot))
        return(published_slot.inserted_id), collection_name

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
            "bundle_slots":dict.fromkeys(entity_tasks,[])
        }
        )

        xcon.server.close()
        print("{0} bundle has been published".format("_".join(set_display_name)))
        return published_slot.inserted_id, collection_name

    def select_entity(collection, show_name, branch_name, category, entry_name, version):
        bundle_slots = list()
        db = xcon.server.xchange
        select_bundle = db[collection].find({"show_name": show_name, "branch":branch_name, "category":category, "entry_name": entry_name, "version":version})
        for slots in select_bundle:
            bundle_slots.append(slots)

        return bundle_slots[0]

    def add_db_id_reference(collection, parent_doc_id, parent_doc_slot, id_to_add, from_collection):
        db = xcon.server.xchange
        db[collection].update_one({"_id":ObjectId(parent_doc_id)},{"$push":{parent_doc_slot:DBRef(from_collection, id_to_add)}})

    def get_db_referenced_attr(source_collection, source_id, source_attr, find_attr):
        db = xcon.server.xchange
        list_attr = list()
        if not source_id or source_id==None:
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
        print(" user for {} created!".format(first_name+" "+name))
        pass

    def get_current_user():
        username = getpass.getuser()
        return username

if __name__=="__main__":
    from origin_data_base import OriginEnvar

    OriginEnvar.show_name = "Test"
    OriginEnvar.branch_name = "origin_library"
    OriginEnvar.category = "airplanes"
    OriginEnvar.entry_name = "707"
    OriginEnvar.task_name = "modeling"

    c = OriginId.db_show_id()
    print(c)

    db_paths = OriginDbPath.db_task_imp_from()
    print(db_paths)

    db_update = OriginUpdate()
    db_update.task_imports_from(['testCCC','testB','testBBBBB'])
    db_update.update_task_is_active(False)
    db_update.update_task_pub_slot(['slot1', 'slot2', 'slot3'])
    db_update.update_task_pub_slot_dict([{"proj":{}}])


    ocreate = OriginCreate()
    # ocreate.db_project(name="Test")
    # ocreate.db_branch(name="origin_library", branch_type=OriginBranchTypes().library)
    # ocreate.db_category(name="airplanes", tasks_type=OriginTasksTypes().props)
    # ocreate.db_asset(name="707")
    # ocreate.create_task(name="another_task")


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





