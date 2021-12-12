import os
import sys

class Project():
    def __init__(self, test_var):
        self.test_var = test_var
    
    @classmethod
    def project(cls):
        return (os.environ.get('ORIGIN_PROJECT')) 

    @classmethod
    def get_project_full_path(cls):
        projects_root = os.environ.get('ORIGIN_PROJECTS_ROOT')
        curr_project = os.environ.get('ORIGIN_PROJECT')
    
        return (os.path.join(projects_root, curr_project))

    @classmethod
    def get_branch(cls):
        return (os.environ.get('ORIGIN_PROJECT_BRANCH'))

    @classmethod
    def get_category(cls):
        return (os.environ.get('ORIGIN_PROJECT_CATEGORY'))

    @classmethod
    def get_entity(cls):
        return (os.environ.get('ORIGIN_PROJECT_ENTITY'))

    @classmethod
    def get_task(cls):
        return (os.environ.get('ORIGIN_ENTITY_TASK'))
        
    @classmethod
    def change_test_var(cls, change_to):
        cls.test_var = change_to
        print (cls.test_var)
        return cls.test_var
    
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
    


if __name__ == "__main__":
   
    j = Project.get_entity()
    Project.change_test_var("kaka")
    print(j)