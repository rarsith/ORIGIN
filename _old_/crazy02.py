import os
import json
from RND import xcg_config_old_not_used as gld

# from benedict import benedict

    # {'show_db':[
    #     {'show_name':'show_name'},
    #     {'pivot':
    #          {'assets':[
    #         'asset_type':'asset_type',
    #         'asset_name':'asset_name',


# seq = [{'seq_name':'TestingTestin'},{'seq_res':'2k'},{'seq_lenght':'36'}]
db_name_clone = {'content':[{'show':[{'show_name':''}]},{'seq':[{'seq_name':'TestingTestin'},{'seq_res':'2k'},{'seq_lenght':'36'},]},{'assets':[{'characters':[]},{'props':[{'prop_name':''}]},{'environments':[{'env_name':''}]}]}]}
# for each_iter in db_name_clone.iteritems():
#     for elem_iter in each_iter:
#         print elem_iter

# db_name = {'content':[{'show_name':'THEFUCKINGAME','seq':[],'assets':[]}]}
#
#
#
with open(os.path.join(gld.PROJECTS_ROOT, "test.json"), "w") as db:
    data = json.dump(db_name_clone, db, indent=4, sort_keys=True)

# #



# print data_read
# data_read.update(content='foo')
# print data_read


def find_parent(key, dictionary):
    for k,v in dictionary.iteritems():
        if k==key:
            yield v
            # print v
        elif isinstance(v, dict):
            for result in find_parent(key, v):
                # print key
                # print v
                # print result
                yield result

        elif isinstance (v, list):
            for d in v:
                print d
                for result in find_parent(key, d):
                    # print key
                    # print d
                    # print result
                    yield result



value_data = list(find_parent('assets', db_name_clone))
# for each_item in value_data:
#     print value_data



#
# for k,v in data_read.iteritems():
#     print k,v
# hh = list(find_parent("assets", data_read))
# # print "NOW YOU ARE HERE"
# print hh
# assets = [{'characters':[]},{'props':[]},{'env':[]}]
# print assets[0]


# def get_index(list_to_search, item_in_list):
#     index_number = [i for i,j in zip(count(), list_to_search) if j == item_in_list]
#     return index_number
#
# # test = data_read['content'][0]['assets']
# #
# index_no = get_index(data_read, 'content')
# print index_no

#


# test = data_read['content']
# print type(test)
# print test
# test = data_read['content'][0]
# print type(test)
# print test
# test = data_read['content'][0]['assets']

# with open(os.path.join(gld.PROJECTS_ROOT, "test.json"), "r") as db:
#     data_read = json.load(db)
#
# test = data_read['content'][0]['assets'][0]['characters']
# print type(test)
# print test
#
# data_to_insert = {'name':'MORPH','type':'character','tasks':[],'lod':[]}
# if data_to_insert not in test:
#     test.append(data_to_insert)
# else:
#     print "Data Already Exists!! "
#
# print test
# print data_read
#
# with open(os.path.join(gld.PROJECTS_ROOT, "test.json"), "w") as db:
#     data = json.dump(data_read, db, indent=4, sort_keys=True)


# test = data_read['content'][0]['assets'][1]['props'].append({'character_name':'TERRIER'})
# test = data_read['content'][0]['assets'][1]['props'].append({'character_name':'GURATOR'})
# test = data_read['content'][0]['assets'][1]['props'].append({'character_name':'MANUAR'})
# print type(test)
# print test
# test = data_read['content'][0]['assets'][0].update({'unknown':'datator'})
# data_read.get('content').append({'number':'12345'})

























# d = benedict.from_json(os.path.join(gld.PROJECTS_ROOT, "test.json"))
# print d
# for each in d.get('content'):
#     for seq in each:
#         print seq
    # print each



# def find_key(obj, key):
#     if isinstance (obj, dict):
#         for u in iter_dict(obj, key, []):
#             yield u
#     elif isinstance(obj, list):
#         for u in iter_list(obj, key, []):
#             yield u
#
# def iter_dict(d, key, indices):
#     for k,v in d.items():
#         if k==key:
#             yield indices + [k], v
#         if isinstance(v, dict):
#             for v in iter_dict(v, key, indices + [k]):
#                 yield v
#         elif isinstance(v, list):
#             for v in iter_dict(v, key, indices + [k]):
#                 yield v
#
# def iter_list(seq, key, indices):
#     for k,v in enumerate(seq):
#         if isinstance(v, dict):
#             for v in iter_dict(v, key, indices + [k]):
#                 yield v
#         elif isinstance(v, list):
#             for v in iter_dict(v, key, indices + [k]):
#                 yield v

# test

# for t in find_key(db_name, 'assets'):
#     print t


















def db_insert(parent, db_update):
    for each in stt:
        for elem in each:
            print type(elem)
            print elem.update(parent=db_update)
            print elem
    print "THis has been done"
    # return elem













#####################START#########################


def read_json_file(file_path, file_name):
    with open(os.path.join(file_path , file_name+".json"), "r") as jsonFile:
        file_content = json.load(jsonFile)
    return file_content


def write_json_file(dataToWrite, file_path, file_name):
    with open(os.path.join(file_path, file_name + ".json"), "w") as jsonFile:
        json.dump(dataToWrite, jsonFile, indent=2)

    return file_name


def create_db(database_name):
    path_to_root = gld.PROJECTS_ROOT

    existing_shows = []
    for path in os.listdir(gld.PROJECTS_ROOT):
        if "." in path:
            parts = path.split(".")
            existing_shows.append(parts[0])

    if database_name not in existing_shows:
        root_db = {'content':[{'show_name':database_name},{'is_active':'Yes'}]}
        with open(os.path.join(path_to_root, database_name + ".json"), "w") as jsonFile:
            json.dump(root_db, jsonFile, indent=2)
        print "%s ROOT FILE has been successfully created!" % database_name
    else:
        print"%s ROOT FILE already exists! Please specify another name" % database_name


def update_active_shows():
    path_to_root = gld.PROJECTS_ROOT

    existing_shows = []
    for path in os.listdir(gld.PROJECTS_ROOT):
        if "." in path:
            parts = path.split(".")
            if "_" in path:
                parts = path.split("_")
                existing_shows.append(parts[0])


    read_json_file(path_to_root, "allShows")
    update_all = {}
    update_all['shows'] = []
    update_all['shows'].append(existing_shows)
    write_json_file(update_all,path_to_root, "allShows")


def shows_index_db(name='allShows'):
    path_to_root = os.listdir(gld.PROJECTS_ROOT)
    file_name = name + ".json"

    if file_name not in path_to_root:
        data = [{'shows': []}]
        write_json_file(data, path_to_root, name)


    else:
        print "%s DATABASE already Exists, no need to recreate!" % name

def create_root(name):
    path_to_root = gld.PROJECTS_ROOT
    create_db(name)
    return name

def find_parent(key, dictionary):
    for k,v in dictionary.iteritems():
        if k==key:
            yield v
        elif isinstance(v, dict):
            for result in find_parent(key, v):
                yield result
        elif isinstance (v, list):
            for d in v:
                for result in find_parent(key, d):
                    yield result

def create_entity(show_name, parent, type, name):
    projects_root = os.listdir(os.path.join(gld.PROJECTS_ROOT))
    print projects_root
    valid_types = ['group','item']
    entity_type = []
    parented_to = parent
    parent_location = list(find_parent(parent, show_name))
    update_db = []
    write_json_file(update_db, projects_root, show_name)


# create_entity('TOTO_show', "content", "group", "assets")


# entity = access_entity(type, )
# pass




# create_root('KOKO_show')
# shows_index_db()
# update_active_shows()















def access_entity(entity_root, entity_type):
    selected_entity = []
    db_access = data_read['content']
    for root_groups in db_access:

        try:
            for show_data in root_groups[entity_root]:

                try:
                    for ent_name in show_data[entity_type]:
                        selected_entity.append(ent_name)

                except:
                    pass

        except:
            pass
    print selected_entity
    return selected_entity





# selected_entity = {}
# db_access = data_read['content']
#
# for root_groups in db_access:
#
#     try:
#         for show_data in root_groups['assets']:
#
#             try:
#                 for ent_name in show_data['characters']:
#                     ent_name.update(ch_name='NEW')
#                     selected_entity.update(ent_name)
#                     print ent_name
#
#
#
#
#             except:
#
#                 pass
#
#     except:
#
#         pass
#
# print selected_entity






# access_entity("seq","seq_name")






# for item in data_read:
#     print item
#
#     for seq in data_read[item]:



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






























