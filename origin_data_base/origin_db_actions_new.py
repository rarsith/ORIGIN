import uuid
import re
import os
import getpass
from asyncio import tasks

# import output as output
from bson import ObjectId
from bson.dbref import DBRef

from origin_utilities import utils as xutil
from origin_utilities.date_time import OriginDateTime
from origin_data_base import origin_templates as otmp
from origin_data_base import origin_templates_query as otmpq
from origin_config import xcg_validation as xvalid
from origin_data_base import xcg_db_connection as xcon
from origin_data_base.OriginEnvar import OriginEnvar, OriginOSEnvar
from origin_data_base.OriginOSUtils import OriginOSUtils

xnow = OriginDateTime()


class JunkStorage(object):
    pass


class OriginOutputPaths(object):
    def __init__(self, version="", pub_slot="", output_file_name="default"):
        self.version = version
        self.pub_slot = pub_slot
        self.output_file_name = output_file_name

    def base_path(self):
        path_entities = [OriginEnvar.show_name,
                         OriginEnvar.branch_name,
                         OriginEnvar.category,
                         OriginEnvar.entry_name,
                         OriginEnvar.task_name]
        return path_entities


    def main_publish_path(self):
        base_path = self.base_path()
        main_pub_elements = ["output", self.version, self.pub_slot, self.output_file_name]
        path_entities = base_path+main_pub_elements

        return path_entities

    def original_images_path(self):
        #TODO need to find a way to contain the file image seq with a REGEX pattern
        path_entities = [OriginEnvar.show_name,
                         OriginEnvar.branch_name,
                         OriginEnvar.category,
                         OriginEnvar.entry_name,
                         OriginEnvar.task_name,
                         "output",
                         self.version,
                         "original",
                         self.pub_slot,
                         self.output_file_name]

        return path_entities

    def review_video_path(self):
        path_entities = [OriginEnvar.show_name,
                         OriginEnvar.branch_name,
                         OriginEnvar.category,
                         OriginEnvar.entry_name,
                         "data",
                         OriginEnvar.task_name,
                         self.version,
                         self.pub_slot,
                         self.output_file_name]

        return path_entities

    def preview_video_path(self):
        path_entities = [OriginEnvar.show_name,
                         OriginEnvar.branch_name,
                         OriginEnvar.category,
                         OriginEnvar.entry_name,
                         "data",
                         OriginEnvar.task_name,
                         self.version,
                         self.pub_slot,
                         self.output_file_name]

        return path_entities

    def used_template_path(self):
        pass

    def work_file_path(self):
        path_entities = [OriginEnvar.show_name,
                         OriginEnvar.branch_name,
                         OriginEnvar.category,
                         OriginEnvar.entry_name,
                         OriginEnvar.task_name,
                         "output",
                         self.version,
                         self.output_file_name]

        return path_entities

    def wip_file_path(self):
        path_entities = [OriginEnvar.show_name,
                         OriginEnvar.branch_name,
                         OriginEnvar.category,
                         OriginEnvar.entry_name,
                         OriginEnvar.task_name,
                         "users",
                         OriginUsers.get_current_user(),
                         self.version,
                         self.output_file_name]

        return path_entities

    @staticmethod
    def origin():
        return {'input': 'task/imports_from/slot/version/file.ext', 'link': 'insert_link'}

    @staticmethod
    def compose_db_path_dict(path_entities=[]):
        main_path_all = dict(path_elements=path_entities)
        return main_path_all

    def compose_path(self, path_elements):
        pass


class OriginUsers(object):
    def __init__(self):
        self.db = xcon.server.xchange

    def create_user(self, first_name, name, personal_email, job_title):
        self.db.users.insert_one(
            {
                "first_name": first_name,
                "name": name,
                "active": True,
                "personal_email": personal_email,
                "job_title": job_title,
                "user_name": {},
                "internal_email": {},
                "date": xnow.return_date(),
                "time": xnow.return_time()
            }
        )
        print(" user for {} created!".format(first_name + " " + name))
        pass

    @staticmethod
    def get_current_user():
        username = getpass.getuser()
        return username


class OriginDBVersions(object):

    def version_increment(self, versions_list=[]):
        if not len(versions_list) < 1:
            conv_to_int = []

            for versions in versions_list:
                conv_to_int.append(versions)

            highest = max(conv_to_int)
            get_digit = re.findall('\d+', highest)

            return "{0}{1:04d}".format("v", (int(get_digit[0]) + 1))

        else:
            return "{0}{1:04d}".format("v", (int(1)))

    def db_task_ver_increase(self):
        get_versions = xutil.db_find_key("publishes", "version",
                                         show_name=OriginEnvar.show_name,
                                         category=OriginEnvar.category,
                                         entry_name=OriginEnvar.entry_name,
                                         task_name=OriginEnvar.task_name,
                                         )
        new_version = self.version_increment(get_versions)
        return new_version

    def db_pubslot_ver_increase(self, collection_name, slot_name):

        get_versions = xutil.db_find_key(collection_name, "version",
                                         show_name=OriginEnvar.show_name,
                                         category=OriginEnvar.category,
                                         entry_name=OriginEnvar.entry_name,
                                         task_name=OriginEnvar.task_name,
                                         slot_name=slot_name
                                         )

        new_version = self.version_increment(get_versions)
        return new_version

    def db_master_bundle_ver_increase(self):

        get_versions = xutil.db_find_key("bundles", "version",
                                         show_name=OriginEnvar.show_name,
                                         category=OriginEnvar.category,
                                         entry_name=OriginEnvar.entry_name
                                         )

        new_version = self.version_increment(get_versions)
        return new_version

    def db_sync_tasks_ver_increase(self):

        get_versions = xutil.db_find_key("task_sync", "version",
                                         show_name=OriginEnvar.show_name,
                                         category=OriginEnvar.category,
                                         entry_name=OriginEnvar.entry_name
                                         )

        new_version = self.version_increment(get_versions)
        return new_version

    def db_wip_files_version_increase(self, collection_name):
        get_versions = xutil.db_find_key(collection_name, "version",
                                         show_name=OriginEnvar.show_name,
                                         category=OriginEnvar.category,
                                         entry_name=OriginEnvar.entry_name,
                                         task_name=OriginEnvar.task_name
                                         )
        new_version = self.version_increment(get_versions)
        return new_version


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
            full_structure = data["show_defaults"][(OriginEnvar.category + "_" + default_type)]
            properties_names = list(full_structure.keys())
            return full_structure, properties_names


class OriginId(object):
    """
    Takes a list and joins the elements into a string
    Ex: list = ["element1", "element2"] >>>> result > "element1.element2"
    To be used for generating ids for entities at creation time
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
    def db_wip_file_id(cls, version):
        return cls.create_id(OriginEnvar.show_name,
                             OriginEnvar.branch_name,
                             OriginEnvar.category,
                             OriginEnvar.entry_name,
                             OriginEnvar.task_name,
                             "wip",
                             version)

    @classmethod
    def db_main_pub_id(cls, version):
        return cls.create_id("main_pub",
                             OriginEnvar.show_name,
                             OriginEnvar.branch_name,
                             OriginEnvar.category,
                             OriginEnvar.entry_name,
                             OriginEnvar.task_name,
                             version)

    @classmethod
    def db_slot_pub_id(cls, pub_slot,version):
        return cls.create_id("slot_pub",
                             pub_slot,
                             OriginEnvar.show_name,
                             OriginEnvar.branch_name,
                             OriginEnvar.category,
                             OriginEnvar.entry_name,
                             OriginEnvar.task_name,
                             version)

    @classmethod
    def db_master_bundle_id(cls, version):
        return cls.create_id("bundle",
                             OriginEnvar.show_name,
                             OriginEnvar.branch_name,
                             OriginEnvar.category,
                             OriginEnvar.entry_name,
                             version)

    @classmethod
    def db_sync_tasks_id(cls, version):
        return cls.create_id("sync_tasks",
                             OriginEnvar.show_name,
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
    def db_sync_task_path(cls):
        return "sync_tasks"

    @classmethod
    def db_task_imp_from(cls):
        return cls.origin_path("tasks", OriginEnvar.task_name, 'imports_from')

    @classmethod
    def db_task_pub(cls):
        return cls.origin_path("tasks", OriginEnvar.task_name, 'pub_slots')

    @classmethod
    def db_sync_slot_path(cls):
        return cls.origin_path("sync_tasks", OriginEnvar.task_name)

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


class ODBRef(object):
    def __init__(self, collection="", entity_id=""):
        self.collection = collection
        self.entity_id = entity_id
        self.db = xcon.server.xchange


    @property
    def odbref(self):
        id_list = [self.collection, self.entity_id]
        gen_id = ",".join(id_list)
        return str(gen_id)


    def oderef(self, ref_string, get_field=None):
        extr_collection, extr_entity_id = ref_string.split(",")
        if not get_field:
            return extr_collection, extr_entity_id
        elif get_field:
            cursor = self.db[extr_collection]
            db_field = cursor.find_one({"_id":extr_entity_id})
            return db_field[get_field]


class OriginDbRef(object):
    def __init__(self):
        self.db = xcon.server.xchange

    @classmethod
    def add_db_id_reference(cls, collection, parent_doc_id, destination_slot, id_to_add, from_collection, replace=False):
        db = xcon.server.xchange
        if not replace:
            db[collection].update_one({"_id": parent_doc_id},
                                      {"$push": {destination_slot: ODBRef(from_collection, id_to_add).odbref}})
        else:
            db[collection].update_one({"_id": parent_doc_id},
                                      {"$set": {destination_slot: ODBRef(from_collection, id_to_add).odbref}})


class OriginCreate(object):
    def __init__(self):
        self.db = xcon.server.xchange

    def db_project(self, name):
        entity_id = OriginId.create_id("root", name)

        save_data = dict(
            _id= entity_id,
            show_code= " ",
            show_name= name,
            structure= otmp.show_structure(),
            show_defaults= dict(asset_definition= otmp.entry_definition("build"),
                                shots_definition= otmp.entry_definition("shot"),
                                characters_tasks= otmp.tasks_schema("character"),
                                props_tasks= otmp.tasks_schema("prop"),
                                environments_tasks= otmp.tasks_schema("environment"),
                                shots_tasks= otmp.tasks_schema("shot")),
            active= True,
            date= xnow.return_date(),
            time= xnow.return_time(),
            owner= getpass.getuser(),
            show_type= "vfx")

        try:
            self.db.show.insert_one(save_data)

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
        get_tasks_config = OriginDefaults().get_show_defaults(OriginDefaults().root_tasks)

        entity_attributes = dict(
            _id= asset_id,
            show_name= OriginEnvar.show_name,
            entry_name= name,
            type= OriginShowQuery().get_branch_type,
            category= OriginEnvar.category,
            status= " ",
            assignment= {},
            tasks= get_tasks_config[0],
            sync_tasks= OriginTasksSync().create_from_template(),
            master_bundle=dict(main_stream=[]),
            active= True,
            definition= OriginDefaults().get_show_defaults(OriginDefaults().root_definitions),
            date= xnow.return_date(),
            time= xnow.return_time(),
            owner= getpass.getuser()

        )

        try:
            collection.insert_one(entity_attributes)

            insert_entry = OriginDbPath.origin_path("structure", OriginEnvar.branch_name, OriginEnvar.category)
            OriginDbRef.add_db_id_reference("show", root_id, insert_entry, asset_id, OriginShowQuery().get_branch_type)
            print("{} Origin Asset created!".format(name))

        except Exception as e:
            print("{} Error! Nothing Created!".format(e))

    def db_task(self, name):
        asset_id = OriginDbPath().db_entry_path()
        cursor = self.db[OriginShowQuery().get_branch_type]
        task_db_path = OriginDbPath.origin_path(OriginDbPath.db_task_path(), name)
        tasks_defaults = otmp.task_defaults()

        cursor.update_one({"_id": asset_id}, {"$set": {task_db_path: tasks_defaults}})

        OriginTasksSync().add_sync_task(name)
        print("{} Origin Asset Task created!".format(name))

        return name

    def db_pub_slot(self, name):
        asset_id = OriginDbPath().db_entry_path()
        cursor = self.db[OriginShowQuery().get_branch_type]
        task_pub_slot_db_path = OriginDbPath.origin_path(OriginDbPath.db_task_pub(), name)
        tasks_pub_slot_defaults = otmp.tasks_pub_slot_schema()

        cursor.update_one({"_id": asset_id}, {"$set": {task_pub_slot_db_path: tasks_pub_slot_defaults}})

        OriginTasksSync().add_sync_task_slot(name)
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

    def get_branches(self):
        show_structure = self.structure()
        return list(show_structure.keys())

    def get_categories(self, branch):
        show_structure = self.structure()
        full_list = list(show_structure[branch])
        full_list.remove("type")
        return full_list

    def get_entities_names(self, branch, category):
        entities_found = list()
        show_structure = self.structure()
        all_referenced_entities = list(show_structure[branch][category])
        for entity in all_referenced_entities:
            x,y = entity.split(",")
            entities_found.append(ODBRef().oderef(ref_string=entity, get_field="entry_name"))
        return entities_found

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

    def get_tasks_full(self):
        try:
            cursor = self.db[OriginShowQuery().get_branch_type]
            tasks_list = cursor.find({"_id": OriginId.db_entry_id()}, {'_id': 0, 'tasks': 1})
            for elements in tasks_list:
                return elements["tasks"]
        except:
            pass

    def get_task_definition(self, task=OriginEnvar.task_name):
        # TODO, needs to be checked for what it is used
        try:
            task_path = OriginDbPath.origin_path("tasks", task)
            cursor = self.db[OriginShowQuery().get_branch_type]
            tasks_list = cursor.find({"_id": OriginId.db_entry_id()}, {'_id': 0, task_path: 1})
            for tasks in tasks_list:
                return (tasks["tasks"][task])
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


####
class OriginQuery(object):
    def __init__(self, query_type):
        self.query_type = query_type
        self.db = xcon.server.xchange

    def structure(self):
        try:
            all_assets = self.db[self.query_type].find_one({"_id": OriginId.db_show_id(), "active": True},
                                           {'_id': 0, 'structure': 1})
            for each in list(all_assets):
                return each['structure']
        except:
            pass
####


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

    def rem_assets_from_shot(self, show_name, show_branch, category, entry_name, asset_to_remove):
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
            entry_path = "structure" + "." + branch_category + "." + entry_category + "." + entry_name
            self.db.show.update({"show_name": show_name}, {"$unset": {entry_path: 1}})

            # remove entry from its collection
            cursor = self.db[OriginShowQuery().get_branch_type]
            cursor.remove({"_id": OriginId.db_entry_id()})
            print('entry {} deleted from {} collection and removed from {} show structure'.format(entry_name,
                                                                                                  branch_category,
                                                                                                  show_name))

        except:
            pass


class OriginPublish(object):
    def __init__(self):
        self.db = xcon.server.xchange

    def get_db_publishes_ids(self, collection, show_name=None, branch_name=None, category_name=None, entry_name=None, task_name=None, view_limit=0):
        #TODO change this to database aggregations
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

    def get_db_values(self, collection, document_id, value_to_return):
        db = xcon.server.xchange
        if not collection or not document_id or collection == None or document_id == None:
            return
        else:
            selected_document = db[collection].find_one({"_id": ObjectId(document_id)})
            return (selected_document[value_to_return])

    def db_main_publish(self):

        version = OriginDBVersions().db_task_ver_increase()
        set_display_name = "_".join([OriginEnvar.entry_name, "main_publish"])

        common_id = OriginId.db_main_pub_id(version)
        collection_name = "publishes"

        save_content = dict(
            _id= common_id,
            reviewable_component= "insert_movie",
            show_name= OriginEnvar.show_name,
            entry_name= OriginEnvar.entry_name,
            category= OriginEnvar.category,
            branch= OriginEnvar.branch_name,
            task_name= OriginEnvar.task_name,
            status= "PENDING_REVIEW",
            description= [],
            artist= OriginUsers.get_current_user(),
            version= version,
            date= xnow.return_date(),
            time= xnow.return_time(),
            publish_packaging= "main",
            publishing_slots= [],
            display_name= set_display_name
        )


        published = self.db[collection_name].insert_one(save_content)

        print("{0} Main Publish Done!".format(set_display_name))
        return published.inserted_id, collection_name

    def db_slot_publish(self, pub_slot):
        #TODO check if slot is active

        collection_name = "_".join(["publish", "slots", OriginEnvar.task_name])
        version = OriginDBVersions().db_pubslot_ver_increase(collection_name, pub_slot)
        set_display_name = "_".join(["pubslot", pub_slot, OriginEnvar.task_name])
        build_server_path = [OriginEnvar.show_name,
                             OriginEnvar.branch_name,
                             OriginEnvar.category,
                             OriginEnvar.entry_name,
                             OriginEnvar.task_name,
                             version,
                             pub_slot]

        common_id = OriginId.db_slot_pub_id(pub_slot, version)
        bundle = 'current_bundle'


        save_content = dict(
            _id=common_id,
            reviewable_component = "insert_movie_path",
            slot_thumbnail= "insert_thumbnail_path",
            show_name= OriginEnvar.show_name,
            entry_name= OriginEnvar.entry_name,
            category= OriginEnvar.category,
            branch= OriginEnvar.branch_name,
            task_name= OriginEnvar.task_name,
            update_type="non-critical",
            artist= OriginUsers.get_current_user(),
            slot_name= pub_slot,
            status= "PENDING-REVIEW",
            version_origin= "created",
            version= version,
            date= xnow.return_date(),
            time= xnow.return_time(),
            publish_packaging= "slots",
            parent_collection= collection_name,
            display_name= set_display_name ,
            output_path= build_server_path,
            components= dict(path=OriginOutputPaths(version, pub_slot, "cache.abc").main_publish_path(),
                             rc_source_images=OriginOutputPaths(version, pub_slot, "image.%04d.exr").original_images_path(),
                             rc_source_video= OriginOutputPaths(version, pub_slot, "video.mov").review_video_path(),
                             rc_preview= OriginOutputPaths(version, pub_slot, "video.mov").preview_video_path(),
                             template= OriginOutputPaths().used_template_path(),
                             work_file= OriginOutputPaths(version, "work_scene.ext").work_file_path(),
                             chain= OriginOutputPaths().origin(),
                             bundle= bundle,
                             rc_output_path="_path"))

        published_slot = self.db[collection_name].insert_one(save_content)

        print("{0} slot {1} has been published".format(pub_slot, version))
        return published_slot.inserted_id, collection_name

    def db_publish(self):
        task_pub_slots = OriginEntitiesQuery().get_task_pub_slots()
        current_task = OriginEnvar().task_name

        main_publish = self.db_main_publish()
        for pub_slot in task_pub_slots:

            get_sync_path = ".".join(["sync_tasks", current_task, pub_slot])

            pub_slots_publish = self.db_slot_publish(pub_slot)

            OriginDbRef.add_db_id_reference(collection=main_publish[1],
                                            parent_doc_id=main_publish[0],
                                            destination_slot="publishing_slots",
                                            id_to_add=pub_slots_publish[0],
                                            from_collection=pub_slots_publish[1])

            OriginDbRef.add_db_id_reference(collection=OriginShowQuery().get_branch_type,
                                            parent_doc_id=OriginId.db_entry_id(),
                                            destination_slot=get_sync_path,
                                            id_to_add=pub_slots_publish[0],
                                            from_collection=pub_slots_publish[1],
                                            replace=True)

        return main_publish

    def db_publish_sel(self, sel_pub_slots=[]):
        current_task = OriginEnvar().task_name
        task_pub_slots = OriginEntitiesQuery().get_task_pub_slots()
        get_sync_tasks = OriginTasksSync().capture_all()
        sync_to_curr_task = get_sync_tasks[current_task]

        if len(sel_pub_slots)==0:
            sel_pub_slots = task_pub_slots

        for sync_slot in sel_pub_slots:
             del sync_to_curr_task[sync_slot]

        main_publish = self.db_main_publish()

        for pub_slot in sel_pub_slots:

            get_sync_path = ".".join(["sync_tasks", current_task, pub_slot])

            pub_slots_publish = self.db_slot_publish(pub_slot)

            OriginDbRef.add_db_id_reference(collection=main_publish[1],
                                            parent_doc_id=main_publish[0],
                                            destination_slot="publishing_slots",
                                            id_to_add=pub_slots_publish[0],
                                            from_collection=pub_slots_publish[1])

            OriginDbRef.add_db_id_reference(collection=OriginShowQuery().get_branch_type,
                                            parent_doc_id=OriginId.db_entry_id(),
                                            destination_slot=get_sync_path,
                                            id_to_add=pub_slots_publish[0],
                                            from_collection=pub_slots_publish[1],
                                            replace=True)

        for inherited_slot in sync_to_curr_task.items():
            get_collection = inherited_slot[1].split(",")

            OriginDbRef.add_db_id_reference(collection=main_publish[1],
                                            parent_doc_id=main_publish[0],
                                            destination_slot="publishing_slots",
                                            id_to_add=get_collection[1],
                                            from_collection=get_collection[0])





        return main_publish


    def db_work_file_save(self, file_name):
        version = OriginDBVersions().db_wip_files_version_increase("work_files")
        set_display_name = "_".join([OriginEnvar.entry_name,OriginEnvar.task_name, "work_file"])

        common_id = OriginId.db_wip_file_id(version)
        collection_name = "work_files"

        save_content = dict(
            _id= common_id,
            show_name= OriginEnvar.show_name,
            entry_name= OriginEnvar.entry_name,
            category= OriginEnvar.category,
            branch= OriginEnvar.branch_name,
            task_name= OriginEnvar.task_name,
            status= "WIP",
            description= [],
            artist= OriginUsers.get_current_user(),
            version= version,
            date= xnow.return_date(),
            time= xnow.return_time(),
            publish_packaging= "wip_scene",
            display_name= set_display_name,
            origin=[],
            components = dict(main_path = OriginOutputPaths(version, output_file_name=file_name).wip_file_path()),
            session=[]

        )


        published = self.db[collection_name].insert_one(save_content)

        print("{0} Saved!".format(set_display_name))
        return published.inserted_id, collection_name

    def select_entity(self, collection, show_name, branch_name, category, entry_name, version):
        bundle_slots = list()
        db = xcon.server.xchange
        select_bundle = db[collection].find(
            {"show_name": show_name, "branch": branch_name, "category": category, "entry_name": entry_name,
             "version": version})
        for slots in select_bundle:
            bundle_slots.append(slots)

        return bundle_slots[0]


class OriginBundle(object):
    def __init__(self):
        self.db = xcon.server.xchange

    def create_bundle_slot(self, name):
        pass

    def add_to_bundle(self, entity_id, bundle_id, slot):

        OriginDbRef.add_db_id_reference("bundles",
                                        bundle_id,
                                        "master_bundle.{}".format(slot),
                                        entity_id,
                                        OriginShowQuery().get_branch_type,
                                        replace=True)
        return bundle_id

    def remove_bundle_slot(self, name):
        pass

    def update_bundle_slot(self, name):
        pass

    def update_master_bundle(self):
        pass

    def set_as_current(self, bundle_id, add_to_stream="main_stream"):

        OriginDbRef.add_db_id_reference(OriginShowQuery().get_branch_type,
                                        OriginId.db_entry_id(),
                                        "master_bundle.{}".format(add_to_stream),
                                        bundle_id,
                                        "bundles",
                                        replace=True)
        return bundle_id

    def set_slot_state(self, state):
        statuses = ["renderable", "non-renderable", "matte_object"]

        pass

    def db_validate_bundle(self):
        pass

    def db_health_check(self):
        pass

    def db_create_bundle_stream(self, name):
        try:
            asset_id = OriginDbPath().db_entry_path()
            cursor = self.db[OriginShowQuery().get_branch_type]
            db_path = OriginDbPath.origin_path(OriginDbPath.db_asset_master_bundle_path(), (name+"_"+"stream"))

            cursor.update_one({"_id": asset_id}, {"$set": {db_path:[]}})
            print("{} Bundle Stream  created!".format(name))
            return name

        except Exception as e:
            print("{} Error! Nothing Created!".format(e))

    def db_move_to_stream(self, from_stream, to_stream):
        try:
            task_path = OriginDbPath.db_task_pub()
            print(task_path)
            cursor = self.db[OriginShowQuery().get_branch_type]
            cursor.update_one({"_id": OriginId.db_entry_id()}, {"$unset": {task_path: 1}})
            cursor.update_one({"_id": OriginId.db_entry_id()}, {"$set": {task_path: {}}})
        except:
            pass

    def db_create_bundle(self):
        status = "PENDING-REVIEW"
        entity_tasks = OriginEntitiesQuery().get_tasks()
        version = OriginDBVersions().db_master_bundle_ver_increase()
        common_id = OriginId.db_master_bundle_id(version)
        set_display_name = "_".join([OriginEnvar.entry_name, "bundle"])

        save_content=dict(
            _id= common_id,
            show_name= OriginEnvar.show_name,
            entry_name= OriginEnvar.entry_name,
            category= OriginEnvar.category,
            branch= OriginEnvar.branch_name,
            display_name= set_display_name,
            artist= OriginUsers.get_current_user(),
            status= status,
            version= version,
            date= xnow.return_date(),
            time= xnow.return_time(),
            master_bundle=dict.fromkeys(entity_tasks,[])
        )

        master_bundle = self.db.bundles.insert_one(save_content)

        print("{0}, {1} has been published".format(set_display_name, version))
        return master_bundle.inserted_id


class OriginWorkSession(object):
    pass


class OriginTasksSync(object):
    def __init__(self):
        self.db = xcon.server.xchange

    @staticmethod
    def create_from_template():
        get_tasks_config = OriginDefaults().get_show_defaults(OriginDefaults().root_tasks)
        entity_tasks = list(get_tasks_config[0])
        save_elements_list = dict()
        for task in entity_tasks:
            task_definition = (get_tasks_config[0][task])
            task_pub_slots = (list(task_definition["pub_slots"].keys()))
            make_dictionary = dict.fromkeys(task_pub_slots, {})
            nest_slot = {task: make_dictionary}
            save_elements_list.update(nest_slot)

        return save_elements_list

    def capture_all(self):
        try:
            cursor = self.db[OriginShowQuery().get_branch_type]
            tasks_list = cursor.find({"_id": OriginId.db_entry_id()}, {'_id': 0, 'sync_tasks': 1})
            for elements in tasks_list:
                return (elements["sync_tasks"])
        except:
            pass

    def add(self, data={}):
        existing_sync_tasks = self.capture_all()
        return existing_sync_tasks.update(data)

    def add_sync_task(self, name):
        asset_id = OriginDbPath().db_entry_path()
        cursor = self.db[OriginShowQuery().get_branch_type]
        sync_task_db_path = OriginDbPath.origin_path(OriginDbPath.db_sync_task_path(), name)
        cursor.update_one({"_id": asset_id}, {"$set": {sync_task_db_path:{}}})
        print("{} Sync Tasks saved!".format(name))

    def add_sync_task_slot(self, name):
        asset_id = OriginId().db_entry_id()
        cursor = self.db[OriginShowQuery().get_branch_type]
        sync_task_db_path = OriginDbPath.origin_path(OriginDbPath.db_sync_slot_path(), name)
        cursor.update_one({"_id": asset_id}, {"$set": {sync_task_db_path: {}}})
        print("{} Sync Slot saved!".format(name))

    def publish_sync_state(self):
        existing_sync_tasks = self.capture_all()
        version = OriginDBVersions().db_sync_tasks_ver_increase()
        print (version)
        entity_id = OriginId.db_sync_tasks_id(version)

        entity_attributes = dict(
            _id= entity_id,
            show_name= OriginEnvar.show_name,
            entry_name= OriginEnvar.entry_name,
            category= OriginEnvar.category,
            version=version,
            sync_tasks= existing_sync_tasks,
            date= xnow.return_date(),
            time= xnow.return_time(),
            owner= getpass.getuser()

        )

        try:
            self.db.task_sync.insert_one(entity_attributes)

        except Exception as e:
            print("{} Error! Nothing Created!".format(e))

    def get_sync_task_slots(self):
        try:
            cursor = self.db[OriginShowQuery().get_branch_type]
            sync_task_db_path = OriginDbPath.origin_path(OriginDbPath.db_sync_slot_path())
            tasks_list = cursor.find({"_id": OriginId.db_entry_id()}, {'_id': 0, sync_task_db_path: 1})
            for elements in tasks_list:
                sync_task_values = list(elements["sync_tasks"].values())[0]
                sync_task_slots = list(sync_task_values.keys())
                return sync_task_slots
        except ValueError as vale:
            print(vale)


    # def update(self, data):
    #     update_sync = self.add(data)
    #     self.commit(update_sync)




if __name__ == "__main__":
    import pprint

    from origin_data_base.OriginEnvar import OriginEnvar, OriginOSEnvar

    OriginOSEnvar.os_root = "D:/PROJECTS"

    OriginEnvar.show_name = "Test"
    OriginEnvar.branch_name = "new_branch"
    OriginEnvar.category = "some_category"
    OriginEnvar.entry_name = "some_asset"
    OriginEnvar.task_name = "modeling"


    db_update = OriginUpdate()
    # db_update.task_imports_from(['testCCC','testB','testBBBBB'])
    # db_update.update_task_is_active(False)
    # db_update.update_task_pub_slot(['slot1', 'slot2', 'slot3'])
    # db_update.update_task_pub_slot_dict([{"proj":{}}])

    ocreate = OriginCreate()
    # ocreate.db_project(name="Test")
    # ocreate.db_show_branch(name="new_branch", branch_type=OriginBranchTypes().build)
    # ocreate.db_category(name="some_category", tasks_type=OriginTasksTypes().characters)
    # ocreate.db_asset(name="some_asset")
    # ocreate.db_task(name="dodo_FX")
    # ocreate.db_pub_slot(name="special_geo")

    #####TEST MULTI INSERT#######
    # asset_names = ["palm", "socca", "mocca"]
    # for asset in asset_names:
    #     ocreate.db_asset(name=asset)

    # get_tasks_config = OriginDefaults().get_show_defaults(OriginDefaults().root_tasks)
    # v = (get_tasks_config[0]["lidar"])
    # print(list(v["pub_slots"].keys()))



    # dbRef = ODBRef("sdxcgdsjkhfg", "sdfkgkdf").generate_dbref
    # deRef = ODBRef().deref(dbRef)
    # print(dbRef)

    pub = OriginPublish()
    pub.db_work_file_save("cache.abc")
    # m_pub = pub.db_publish()

    # existing_modeling_pub_slots = ['rend_geo', 'proxy_geo', 'utility', 'lidar', 'proj_geo', 'vport_mat', 'tex_object', 'curvature_map', 'ao_map', 'selection_map']
    # m_pub02 = pub.db_publish_sel()
    # print(m_pub)
    # pub.db_slot_publish("xxx")
    # pub.create_master_bundle()

    obundle = OriginBundle()
    # obundle.add_to_bundle("main_pub.Test.vegetation.tree.testy_palm.task_test.v0001",
    #                       "bundle.Test.vegetation.tree.testy_palm.v0001",
    #                       OriginEnvar().task_name)
    # bundle_id = obundle.db_create_bundle()
    # obundle.set_as_current("bundle.Test.vegetation.tree.testy_palm.v0001", "main_stream")
    # obundle.db_create_bundle_stream("RND")

    oq = OriginShowQuery()
    # tsk_cont = oq.get_entities_names(branch='vegetation', category="trees")
    # print(tsk_cont)


    ent_q = OriginEntitiesQuery()

    # pprint.pprint(tsks)
    # pprint.pprint(tsks_names)

    sync = OriginTasksSync()
    # synt_slots = sync.get_sync_task_slots()
    # print(synt_slots, "<<")
    # sync.publish_sync_state()
    # all_sync = sync.capture_all()
    # pprint.pprint (all_sync)

    opaths = OriginOutputPaths("v001", "render_geo", "cache.abc")

    odb = ODBRef()
    # get_all = odb.oderef('build,Test.vegetation.trees.testy_palm', "entry_name")
    # print (get_all)
    # cc = opaths.main_publish_path()
    # print (cc)

    odefaults = OriginDefaults()
    # odefaults.get_show_defaults("tasks")


