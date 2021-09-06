from origin_data_base import xcg_db_connection as xcon


def get_show_defaults(show_name, category, default_type):
    db = xcon.server.xchange
    query_path = "show_defaults" + "." + (category + "_" + default_type)
    category_tasks = db.show.find({"show_name": show_name, "active": True},
                              {'_id': 0, query_path: 1})

    for data in category_tasks:
        return data["show_defaults"][(category + "_" + default_type)]

def get_tasks_package(show_name, branch_category, parent_category, entry_name):
    try:
        entry_tasks = dict()
        if branch_category == None or parent_category == None:
            return
        else:
            # create/connect to show database
            db = xcon.server.xchange
            cursor = db[branch_category]
            tasks_list = cursor.find({"show_name": show_name, "category": parent_category, "entry_name": entry_name}, {'_id':0, 'tasks':1})
            for elements in tasks_list:
                entry_tasks.update(elements)

            return list(entry_tasks.values())[0]
    except:
        pass


def update_category_tasks(show_name, category, default_type, data_to_insert):
    db = xcon.server.xchange

    data_insert = "show_defaults" + "." + (category + "_" + default_type)
    db.show.update_one({"show_name": show_name, "active": True},{"$set":{data_insert:data_to_insert}})








if __name__ == '__main__':

    import pprint

    # g = get_show_defaults("Test", "characters", "tasks")
    # pprint.pprint(g)

    tt = get_tasks_package("Test", "assets", "environments", "cave")
    update_category_tasks("Test", "environments", "tasks", tt)
    pprint.pprint (tt)

    g = get_show_defaults("Test", "environments", "tasks")
    pprint.pprint(g)