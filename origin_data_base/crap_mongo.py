from bson import ObjectId
from bson.dbref import DBRef
from origin_data_base import xcg_db_connection as xcon

db = xcon.server.xchange

# clean up
# db.owners.remove()
# db.tasks.remove()


# owners and tasks
# db.owners.insert_one({"name":"Jim"})
# db.tasks.insert_many([
#     {"name": "read"},
#     {"name": "sleep"}
# ])
#
# # update jim with tasks: reading and sleeping
# reading_task = db.tasks.find_one({"name": "read"})
# sleeping_task = db.tasks.find_one({"name": "sleep"})
#
# jim_update = db.owners.find_one({"name": "Jim"})
# jim_update["tasks"] = [
#     DBRef(collection = "tasks", id = reading_task["_id"]),
#     DBRef(collection = "tasks", id = sleeping_task["_id"])
# ]
#
# db.owners.save(jim_update)

# get jim fresh again and display his tasks
fresh_jim = db.owners.find_one({"name":"Jim"})
print ("Jim's tasks are:")
for task in fresh_jim["tasks"]:
    print (task)
    print (db.dereference(task)["name"])