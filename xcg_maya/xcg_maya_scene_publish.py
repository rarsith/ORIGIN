import os
import re
import maya.cmds as cmds
import xcg_maya.xcg_maya_etc.xcg_maya_utils as moutils
import xcg_data_base.xcg_db_actions as xac
import xcg_utilities.xcg_user_utils as xut



proj_root = os.environ.get('XCG_PROJECTS_ROOT')
show_name = os.environ.get('XCG_PROJECT')
branch_name = os.environ.get('XCG_PROJECT_BRANCH')
category_name = os.environ.get('XCG_PROJECT_CATEGORY')
entity_name = os.environ.get('XCG_PROJECT_ENTITY')
entity_task = os.environ.get('XCG_ENTITY_TASK')


def get_slot_with_content(root_group):
    list_content = list()
    get_content = cmds.listRelatives(root_group)
    
    for each in get_content:
        not_empty = cmds.listRelatives(each)
        
        if not_empty:
            list_content.append(each)
    
    return list_content


def get_scene_pub_slots():
    pub_slots = xac.get_pub_slots(show_name, branch_name, category_name, entity_name, entity_task)
    return pub_slots.keys()


def get_pub_slot_property(slot_name, slot_property):
    pub_type = xac.get_pub_slots(show_name, branch_name, category_name, entity_name, entity_task)
    return pub_type[slot_name][slot_property]


def get_highest_folder_version(folder_path):
    all_folders = list()
    get_folders = os.listdir(folder_path)

    if not len(get_folders)<1:
        for dirs in get_folders:
            all_folders.append(dirs)
        
        highest = max(all_folders)
        get_digit = filter(None, re.split(r'(\d+)', highest))
        return  "{0}{1:04d}".format(("v"),(int(get_digit[1])+1))      

    else:
        return "{0}{1:04d}".format(("v"),(int(1)))

def create_publish_folders():
    output = 'output'
    path_to_ouput = os.path.join(proj_root, show_name, branch_name, category_name, entity_name, entity_task, output)
    if not os.path.exists(path_to_ouput):
        os.makedirs(path_to_ouput)

    version = get_highest_folder_version(path_to_ouput)
    path_to_file = os.path.join(proj_root, show_name, branch_name, category_name, entity_name, entity_task, output, version)

    os.makedirs(path_to_file)
    return path_to_file

def get_entry_attr(object_name, attr_name):
    attribute_capture = str(object_name +'.'+ attr_name)
    return cmds.getAttr(attribute_capture)


def publish_slot(slot_name, publish_path):
    valid_slot = get_slot_with_content(entity_name)
    if valid_slot:
        for each in valid_slot:
            get_db_name = get_entry_attr(each, "xcg_name")
            if slot_name == get_db_name:
                start = 1
                end = 1
                root = "PBS_" + slot_name + "_GRP"
                output_file = slot_name + '.abc'
                alembic_path = os.path.join(publish_path, slot_name, output_file)
                os.makedirs(os.path.join(publish_path, slot_name))
                #command = ("-frameRange " + str(start) + " " + str(end) + " -root " + root + " -uvWrite -worldSpace " + " -file " + alembic_path)
                command = "-frameRange {0} {1} -root {2} -uvWrite -worldSpace -file {3}".format(str(start), str(end), root, alembic_path)
                cmds.AbcExport ( j = command )


def main():
    
    g = get_scene_pub_slots()
    valid = get_slot_with_content(entity_name)
    
    publish_to_folder = create_publish_folders()
    current_user = xut.get_current_user()
    
    for each in g:
        slot_type = get_pub_slot_property(each, 'method')
        if slot_type=='sf_csh':
            
            publish_slot(each, publish_to_folder)
            
    components = xac.get_pub_slots(show_name, branch_name, category_name, entity_name, entity_task)
    main_publish = xac.db_publish(show_name, branch_name, category_name, entity_name, entity_task, branch_name, "0012", "PENDING-REVIEW")
    
    for slot in components:
        secondary_publish = xac.pub_slot_publish(show_name, branch_name, category_name, entity_name, entity_task, slot)
        xac.add_db_id_reference("publishes", main_publish, "publishing_slots", secondary_publish)
         
    cmds.select (cl=True)
    print ("Version {0} has been published".format(publish_to_folder))
    
if __name__ == '__main__':
    main()
    
    
        
    