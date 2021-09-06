import os
import re
import getpass
import maya.cmds as cmds
import origin_data_base.xcg_db_actions as xac


proj_root = os.environ.get('XCG_PROJECTS_ROOT')
proj = os.environ.get('XCG_PROJECT')
br = os.environ.get('XCG_PROJECT_BRANCH')
cat = os.environ.get('XCG_PROJECT_CATEGORY')
ent = os.environ.get('XCG_PROJECT_ENTITY')
ent_task = os.environ.get('XCG_ENTITY_TASK')


def get_current_user():
    username = getpass.getuser()
    return username


def get_next_file_version(folder_path):
    all_files = list()
    get_files = os.listdir(folder_path)

    if not len(get_files)<1:
        for dirs in get_files:
            all_files.append(dirs)
        
        highest = max(all_files)
        get_digit = filter(None, re.split(r'(\d+)', highest))

        return  "{0}{1:04d}".format(("v"),(int(get_digit[1])+1))      

    else:
        return "{0}{1:04d}".format(("v"),(int(1)))



def create_work_folders():
    users = "users"
    who = get_current_user()
    path_to_output = os.path.join(proj_root, proj, br, cat, ent, ent_task, users, who,'')
    if not os.path.exists(path_to_output):
        os.makedirs(path_to_output)
    return path_to_output


def save_work_file(user_name, saving_path):
    version = get_next_file_version(saving_path)
    build_file_name = [ent, ent_task , user_name, version]
    output_file = "_".join(build_file_name)
    path_to_file = saving_path + output_file
    
    cmds.file(rename=path_to_file )
    cmds.file(save=True, type='mayaBinary' )
    print "Saved successfully: {1}{0}".format(output_file, saving_path )


def main():
    current_user = get_current_user()
    publish_to_folder = create_work_folders()
    
    save_work_file(current_user, publish_to_folder)
        
    cmds.select (cl=True)
    
if __name__ == '__main__':
    main()
    
    
        
    