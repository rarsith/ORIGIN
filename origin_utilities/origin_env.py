import os
import sys
    
def project():
    return (os.environ.get('ORIGIN_PROJECT'))

def get_project():
    projects_root = os.environ.get('ORIGIN_PROJECTS_ROOT')
    curr_project = os.environ.get('ORIGIN_PROJECT')
    
    return (os.path.join(projects_root, curr_project))
    
def get_branch():
    return (os.environ.get('ORIGIN_PROJECT_BRANCH'))

def get_category():
    return (os.environ.get('ORIGIN_PROJECT_CATEGORY'))
    
def get_entity():
    return (os.environ.get('ORIGIN_PROJECT_ENTITY'))

def get_task():
    return (os.environ.get('ORIGIN_ENTITY_TASK'))