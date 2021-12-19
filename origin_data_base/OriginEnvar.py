import os

class OriginEnvar():

    @property
    def origin_id(self):
        return os.environ.get('ORIGIN_ID')

    @origin_id.setter
    def origin_id(self, origin_id):
        os.environ['ORIGIN_ID'] = origin_id
        os.environ['ORIGIN_PROJECT'] = ''
        os.environ['ORIGIN_PROJECT_BRANCH'] = ''
        os.environ['ORIGIN_PROJECT_CATEGORY'] = ''
        os.environ['ORIGIN_PROJECT_ENTITY'] = ''
        os.environ['ORIGIN_ENTITY_TASK'] = ''

    @property
    def show_name(self):
        return os.environ.get('ORIGIN_PROJECT')

    @show_name.setter
    def show_name(self, project):
        os.environ['ORIGIN_PROJECT'] = project
        os.environ['ORIGIN_PROJECT_BRANCH'] = ''
        os.environ['ORIGIN_PROJECT_CATEGORY'] = ''
        os.environ['ORIGIN_PROJECT_ENTITY'] = ''
        os.environ['ORIGIN_ENTITY_TASK'] = ''

    @property
    def branch_name(self):
        return os.environ.get('ORIGIN_PROJECT_BRANCH')

    @branch_name.setter
    def branch_name(self, branch):
        os.environ['ORIGIN_PROJECT_BRANCH'] = branch
        os.environ['ORIGIN_PROJECT_CATEGORY'] = ''
        os.environ['ORIGIN_PROJECT_ENTITY'] = ''
        os.environ['ORIGIN_ENTITY_TASK'] = ''

    @property
    def category(self):
        return os.environ.get('ORIGIN_PROJECT_CATEGORY')

    @category.setter
    def category(self, category):
        os.environ['ORIGIN_PROJECT_CATEGORY'] = category
        os.environ['ORIGIN_PROJECT_ENTITY'] = ''
        os.environ['ORIGIN_ENTITY_TASK'] = ''

    @property
    def entry_name(self):
        return os.environ.get('ORIGIN_PROJECT_ENTITY')

    @entry_name.setter
    def entry_name(self, entity):
        os.environ['ORIGIN_PROJECT_ENTITY'] = entity
        os.environ['ORIGIN_ENTITY_TASK'] = ''

    @property
    def task_name(self):
        return os.environ.get('ORIGIN_ENTITY_TASK')

    @task_name.setter
    def task_name(self, task):
        os.environ['ORIGIN_ENTITY_TASK'] = task

    @property
    def task_imports_from(self):
        return os.environ.get('ORIGIN_TASK_IMP')

    @task_imports_from.setter
    def task_imports_from(self, imp_from):
        os.environ['ORIGIN_TASK_IMP'] = imp_from

    @property
    def task_pub(self):
        return os.environ.get('ORIGIN_TASK_PUB')

    @task_pub.setter
    def task_pub(self, pub):
        os.environ['ORIGIN_TASK_PUB'] = pub

    def taget_path(self, *args):
        qpath = '.'.join(args)
        return qpath


if __name__ == "__main__":
    from origin_data_base import xcg_db_connection as xcon

    g = OriginEnvar()
    # g.show_name = 'GUGU'
    # g.branch_name = 'origin_library'
    # g.category = 'airplanesXXX'
    # g.entry_name = '707'
    # g.task_name = 'modeling'
    # g.task_imports_from = 'concept'
    # g.task_imports_pub = 'render_geo'

    print(g.show_name)
    print(g.branch_name)
    print(g.category)
    print(g.entry_name)
    print(g.task_name)

    # class OQuery():
    #     def select_db_entity(self):
    #         db = xcon.server.xchange
    #         cursor = db[g.branch_name]
    #         anchor = {"show_name":g.show_name, "category":g.category, "entry_name":g.entry_name}
    #         return cursor.find(anchor, {"_id":0})
    #
    #     def q_entity_attr(self, q_attr):
    #         selection = self.select_db_entity()
    #         for attr in selection:
    #             return attr[q_attr]
    #
    #
    #
    # x = OQuery()
    # y = x.q_entity_attr("tasks")
    # print (y)

