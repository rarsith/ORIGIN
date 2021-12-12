import os
import re
import getpass
import importlib

import origin_utilities.origin_env as oenv
importlib.reload(oenv)


###################################################
def get_curr_user():
    username = getpass.getuser()
    return username

###################################################
def save_path():
    proj_root = oenv.get_project()
    branch = oenv.get_branch()
    category = oenv.get_category()
    entity = oenv.get_entity()
    task = oenv.get_task()
    return os.path.join(proj_root, branch, category, entity, task)
    
###################################################
def next_file_version(folder_path):
    """
    On a given path, it gets the highest version number and it's returning the next available version number
    """
    all_files = list()
    get_files = os.listdir(folder_path)
    if not len(get_files)<1:
        for dirs in get_files:
            all_files.append(dirs)
        print (all_files)
        highest = max(all_files)
        get_digit = filter(None, re.split(r'(\d+)', highest))
        get_digit_list = (list(get_digit))
        
        return  "{0}{1:04d}".format(("v"),(int(get_digit_list[1])+1))
    else:
        return "{0}{1:04d}".format(("v"),(int(1)))
 
 ###################################################       
def wip_output_path():
    '''
    Outputs the complete saving path
    '''
    users = "users"
    who = get_curr_user()
    saving_path = save_path()
    path_to_output = os.path.join(saving_path, users, who,'')
    if not os.path.exists(path_to_output):
        os.makedirs(path_to_output)
    return path_to_output

###################################################
def publish_path():
    output = 'output'
    saving_path = save_path()
    path_to_ouput = os.path.join(saving_path, output) 
    if not os.path.exists(path_to_ouput):
        os.makedirs(path_to_ouput)

    version = next_file_version(path_to_ouput)
    path_to_file = os.path.join(path_to_ouput, version)
    os.makedirs(path_to_file)
    
    return path_to_file

###################################################       
def build_wip_file_name(saving_path):
    entity = oenv.get_entity()
    task = oenv.get_task()
    user_name = get_curr_user()
    version = next_file_version(saving_path)
    build_file_name = [entity, task , user_name, version]
    output_file = "_".join(build_file_name)

    return output_file