class DbActions(object):

    jojo = "huhu"


    def __init__(self):
        self.show_name = ""

    def active_show(self):
        return self.show_name


    def rename_proj(self, new_name=""):
        self.show_name = new_name


db_act = DbActions()
db_act.show_name = "kuku"
print (db_act.active_show())
db_act.rename_proj("jojo")
print (db_act.active_show())
print (db_act.jojo)