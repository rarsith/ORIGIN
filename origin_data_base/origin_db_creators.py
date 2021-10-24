import getpass
from origin_utilities.date_time import OriginDateTime
from origin_data_base import origin_templates as otmp
from origin_data_base import xcg_db_connection as xcon
from origin_data_base import origin_db_validators as oval
xnow = OriginDateTime()



def create_show(show_name, code_name, show_type):
    # create/connect to show database
    # TODO, need checking if show already exists, if True then halt
    get_items = oval.db_content_summary(show_name, "show")
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
                                 "shots_definition":otmp.entry_definition("shot"),
                                 "characters_tasks":otmp.tasks_schema("character"),
                                 "props_tasks":otmp.tasks_schema("prop"),
                                 "environments_tasks":otmp.tasks_schema("environment"),
                                 "shots_tasks":otmp.tasks_schema("shot")},
                "active": True,
                "date": xnow.return_date(),
                "time": xnow.return_time(),
                "owner":getpass.getuser(),
                "show_type":show_type
            }
        )
        print ("{} show created!".format(show_name))