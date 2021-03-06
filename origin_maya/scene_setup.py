import os
import importlib
import maya.cmds as cmds

import origin_maya.utils.xcg_maya_utils as mutils
importlib.reload(mutils)

import origin_data_base.xcg_db_actions as xac
importlib.reload(xac)




proj_root = os.environ.get('ORIGIN_PROJECTS_ROOT')
proj = os.environ.get('ORIGIN_PROJECT')
br = os.environ.get('ORIGIN_PROJECT_BRANCH')
cat = os.environ.get('ORIGIN_PROJECT_CATEGORY')
ent = os.environ.get('ORIGIN_PROJECT_ENTITY')
ent_task = os.environ.get('ORIGIN_ENTITY_TASK')

# vv = os.path.join(proj_root, proj, br, cat, ent, ent_task)

def get_db_pub_slots():
    pub_slots = xac.get_pub_slots(proj, br, cat, ent, ent_task)
    return pub_slots.keys()


def get_pub_slot_property(slot_name, slot_property):
    pub_type = xac.get_pub_slots(proj, br, cat, ent, ent_task)
    return pub_type[slot_name][slot_property]


def create_pub_slots_grp(parent, grp_name):
    prefix = "PBS_"
    sufix = "_GRP"
    name_compile = prefix+grp_name+sufix
    if name_compile not in mutils.get_outliner():
        cmds.group(em=True, p=parent, n=prefix+grp_name+sufix)
    
    return name_compile
        
def create_root_group():
    root_group = "SCENE"
    if root_group not in mutils.get_outliner():
        root_group = cmds.group(em=True, n="SCENE")
        return root_group

def create_branch_group(parent):
    branch_grp_name = os.environ.get('ORIGIN_PROJECT_BRANCH')
    if branch_grp_name.upper() not in mutils.get_outliner():
        branch_group = cmds.group(em=True, p=parent, n=branch_grp_name.upper())
        return branch_group

def create_task_group(parent):
    task_grp_name = os.environ.get('ORIGIN_ENTITY_TASK')
    if task_grp_name.upper() not in mutils.get_outliner():
        task_group = cmds.group(em=True, p=parent, n=task_grp_name.upper())
        return task_group

def create_entry_group(entry, parent):
    if entry not in mutils.get_outliner():
        root_group = cmds.group(em=True, p=parent, n=entry)
        return root_group


def main():
    outliner = mutils.get_outliner()
    g = get_db_pub_slots()
    scene_root = create_root_group()
    task_group = create_task_group(parent=scene_root)
    branch_group = create_branch_group(parent=task_group)
    
    asset_root = create_entry_group(ent, parent=branch_group)
   
    for each in g:
        slot_type = get_pub_slot_property(each, 'type')
        accept_type = ['geo', 'scn', 'csh']
        if slot_type in accept_type:
            pub_slot = create_pub_slots_grp(ent, each)
            mutils.create_entry_attr(pub_slot, "origin_name", str(each))
        
    cmds.select (cl=True)
    
if __name__ == '__main__':
    get_db_pub_slots()
    
    main()
    
    
        
    