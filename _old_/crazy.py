import os
import json
from RND import xcg_config_old_not_used as gld

# {'show_db':[
    #     {'show_name':'show_name'},
    #     {'pivot':
    #          {'assets':[
    #         'asset_type':'asset_type',
    #         'asset_name':'asset_name',



db_name = {'content':[{'show':[{'show_name':'TEST_ME'}]},{'seq':[{'QQT':[{'shot_name':'123456'},{'shot_name':'123444'}]},{'DDF':[{'shot_name':'123456'},{'shot_name':'123444'}]}]},{'assets':[{'characters':[]},{'props':[]},{'environments':[]}]}]}



with open(os.path.join(gld.PROJECTS_ROOT, "test.json"), "w") as db:
    data = json.dump(db_name, db, indent=4, sort_keys=True)


with open(os.path.join(gld.PROJECTS_ROOT, "test.json"), "r") as db:
    data = json.load(db)



























# print(type(data))
# temp_item = []
# for item in data['content']:
#     temp_item.append(item)
#     for seq in temp_item['seq']:
#
#         try:
#             print seq
#         except:
#             pass
# print temp_item[2]
    # for cat in

# for item in data['show']:
#     print (item['name'])




# }
#             'asset_level':'asset_level'
# ]
#
#
#
#
#
#
#                  {'seq':[
#                      {'shot_name':'shot_name'},
#                      {'seq_name':'seq_name'},
#                      {'seq_name':'seq_name'},
#                      {'shots':[
#                          {'shot_name':'shot_name'},
#                          [
#                              {'seq_name': 'seq_name'},
#                              {'shot_name': 'shot_name'},
#                              {'shot_tasks': []}]},
#                      {'seq_name':[
#                          {'shot_name':
#                               ['content']}]},[
#                          {'shot_name':['content']}]},{'seq_name': [{'shot_name': ['content']}]}]}]
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#








# ###
# def create_xchange_db():
#     valid_db_keys = ['show', 'characters', 'props', 'environments', 'shot', ]
#
#     shows_db = {}
#
#
#     for entry in valid_db_keys:
#         shows_db[entry] = []
#         shows_db[entry].append([])
#
#     with open(os.path.join(gld.PROJECTS_ROOT,gld.DATA_BASE_NAME),"w") as db:
#         json.dump(shows_db, db)
#
#
# def update_xchange_db(db_key, *data):
#     valid_db_keys = ['show','characters','props','environments','shot',]
#     db_id = gld.DATA_BASE_NAME
#     db_location = os.listdir(os.path.join(gld.PROJECTS_ROOT))
#     print db_location
#     print db_id
#
#     if db_id not in db_location:
#         create_xchange_db()
#     else:
#         pass
#
#     if not db_key in valid_db_keys:
#         print "%s current db_key not valid" % db_key
#         print "Please these %s" % valid_db_keys
#     else:
#         with open (os.path.join(gld.PROJECTS_ROOT,gld.DATA_BASE_NAME),"r") as db:
#             shows_db = json.load(db)
#
#     shows_db[db_key]=data
#
#
#     update_db = json.dumps(shows_db)
#     with open(os.path.join(gld.PROJECTS_ROOT,gld.DATA_BASE_NAME),"w") as upd_db:
#         upd_db.write(update_db)
#         upd_db.close()
#
#
# def delete_xchange_db(db_key, *data):
#     valid_db_keys = ['show', 'seq', 'characters', 'props', 'environments', 'shot', ]
#
#     if not db_key in valid_db_keys:
#         print "%s current db_key not valid" % db_key
#         print "Please these %s" % valid_db_keys
#     else:
#         with open(os.path.join(gld.PROJECTS_ROOT, gld.DATA_BASE_NAME), "r") as db:
#             shows_db = json.load(db)
#
#             db_values_pick = shows_db.get(db_key)
#             data_convert = data[0]
#
#             try:
#                 db_values_pick.remove(data_convert)
#                 print "%s removed from %s" % (data_convert,db_key)
#
#             except:
#                 print "%s db item doesn't exist!" % data
#
#             update_db = json.dumps(shows_db)
#             with open(os.path.join(gld.PROJECTS_ROOT, gld.DATA_BASE_NAME), "w") as upd_db:
#                 upd_db.write(update_db)
#
#
#
#
#
#
# # create_xchange_db()
# update_xchange_db()
# # update_xchange_db('characters')
#
# # delete_xchange_db('seq')
# ###






























