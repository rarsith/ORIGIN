import os

class OriginEnvar():

    @property
    def origin_id(self):
        return os.environ.get('ORIGIN_ID')

    @origin_id.setter
    def origin_id(self, origin_id):
        os.environ['ORIGIN_ID'] = origin_id

    @property
    def show_name(self):
        return os.environ.get('ORIGIN_PROJECT')

    @show_name.setter
    def show_name(self, project):
        os.environ['ORIGIN_PROJECT'] = project

    @property
    def branch_name(self):
        return os.environ.get('ORIGIN_PROJECT_BRANCH')

    @branch_name.setter
    def branch_name(self, branch):
        os.environ['ORIGIN_PROJECT_BRANCH'] = branch

    @property
    def category(self):
        return os.environ.get('ORIGIN_PROJECT_CATEGORY')

    @category.setter
    def category(self, category):
        os.environ['ORIGIN_PROJECT_CATEGORY'] = category

    @property
    def entry_name(self):
        return os.environ.get('ORIGIN_PROJECT_ENTITY')

    @entry_name.setter
    def entry_name(self, entity):
        os.environ['ORIGIN_PROJECT_ENTITY'] = entity

    @property
    def task_name(self):
        return os.environ.get('ORIGIN_ENTITY_TASK')

    @task_name.setter
    def task_name(self, task):
        os.environ['ORIGIN_ENTITY_TASK'] = task

    def taget_path(self, *args):
        qpath = '.'.join(args)
        return qpath

if __name__ == "__main__":
    from origin_data_base import xcg_db_connection as xcon

    g = OriginEnvar()
    g.show_name = 'Test'
    g.branch_name = 'assets'
    g.category = 'characters'
    g.entry_name = 'hulk'
    g.task_name = 'modeling'

    class OQuery():
        def select_db_entity(self):
            db = xcon.server.xchange
            cursor = db[g.branch_name]
            anchor = {"show_name":g.show_name, "category":g.category, "entry_name":g.entry_name}
            return cursor.find(anchor, {"_id":0})

        def q_entity_attr(self, q_attr):
            selection = self.select_db_entity()
            for attr in selection:
                return attr[q_attr]



    x = OQuery()
    y = x.q_entity_attr("master_bundle")
    print (y)

