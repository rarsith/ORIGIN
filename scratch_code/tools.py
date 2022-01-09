import pprint
from origin_data_base import origin_db_actions_new as oda
from origin_data_base.OriginEnvar import OriginEnvar
from origin_utilities.save_json import save_json



def add_to_dict(dict_to_add, add_to_dict):
    '''
    :param dict_to_add: Provide a dictionary to add to -->
    :param add_to_dict: ...this provided dictionary
    :return:
    '''


    iterator = list(add_to_dict)
    new_dictionary = dict.fromkeys(iterator, {})

    # print (new_dictionary, '<<<')

    store_new_dict = {}
    for k , v in add_to_dict.items():
        print (k)
        dict_to_add.update(add_to_dict[k])
        print (k, dict_to_add)
        store_new_dict.update(kdict_to_add)
        # print(dict_to_add)

        print (store_new_dict)
        # print(item, store_new_dict)

        # store_new_dict.update(dict_to_add)


        # print(dict_to_add)
        # full_dict = {item:dict_to_add}
        # new_dictionary[item]=dict_to_add
        # print (dict_to_add)
        # new_dictionary.update(full_dict)
    # print (store_new_dict)
    # return new_dictionary




if __name__ == '__main__':

    OriginEnvar.show_name = "Test"
    OriginEnvar.branch_name = "vegetation"
    OriginEnvar.category = "trees"
    OriginEnvar.entry_name = "new_palm_tree"
    OriginEnvar.task_name = "ooo_test"



    ent_q = oda.OriginEntitiesQuery()
    keys_to_add = {"used_in":"shots"}
    tsks = ent_q.get_tasks_full()

    tsks_names = list(tsks)

    ddd = add_to_dict(dict_to_add=keys_to_add, add_to_dict=tsks)

    # save_json("test_out.json", ddd)
    # pprint.pprint(ddd)

