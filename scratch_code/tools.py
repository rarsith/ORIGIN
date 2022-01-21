import pprint
from origin_data_base import origin_db_actions_new as oda
from origin_data_base.OriginEnvar import OriginEnvar
from origin_utilities.save_json import save_json



def add_to_dict(dict_root, dict_to_add, add_to_dict):
    '''
    :param dict_to_add: Provide a dictionary to add to -->
    :param add_to_dict: ...this provided dictionary
    :return:
    '''

    store_new_dict = []
    # k, v = add_to_dict.items()
    # dict_to_add.update(add_to_dict[k])
    # store_new_dict[k]=dict_to_add
    # print (store_new_dict)
    for k , v in add_to_dict.items():
        print (k, v)
        dict_to_add.update(add_to_dict[k])

        c = [k, dict_to_add]
        print ("<<", str(c))


        # print(store_new_dict)


        # print(dict_to_add)


        # print(item, store_new_dict)

        # store_new_dict.update(dict_to_add)


        # print(dict_to_add)
        # full_dict = {item:dict_to_add}
        # new_dictionary[item]=dict_to_add
        # print (dict_to_add)
        # new_dictionary.update(full_dict)
    # print (store_new_dict)
    return store_new_dict




if __name__ == '__main__':

    OriginEnvar.show_name = "Test"
    OriginEnvar.branch_name = "vegetation"
    OriginEnvar.category = "trees"
    OriginEnvar.entry_name = "superPalm"
    OriginEnvar.task_name = "ooo_test"



    ent_q = oda.OriginEntitiesQuery()
    keys_to_add = {"used_in":"shots"}
    tsks = ent_q.get_tasks_full()

    tsks_names = list(tsks)

    ddd = add_to_dict(dict_root="root", dict_to_add=keys_to_add, add_to_dict=tsks)

    # save_json("test_out.json", ddd)
    pprint.pprint(ddd)
    # dd = {}
    # bb = {'used_in': 'shots', 'active': True, 'status': 'NOT-STARTED', 'artist': 'None', 'imports_from': {}, 'pub_slots': {'special_geo': {'type': '', 'method': '', 'used_by': [], 'source': {}, 'reviewable': True, 'active': True}}}
    # cc = {'used_in': 'shots', 'active': False, 'status': 'NOT-STARTED', 'artist': 'None', 'imports_from': {}, 'pub_slots': {'special_geo': {'type': '', 'method': '', 'used_by': [], 'source': {}, 'reviewable': True, 'active': True}}}
    # dd["ooo_test"]= bb
    # dd["mm"]=cc
    # print (dd, "<<<<")


