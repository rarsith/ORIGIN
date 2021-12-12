import importlib
from origin_data_base import xcg_db_connection as xcon

from origin_utilities.origin_env import Project


class OriQuery():
    
    
    def __init__(self, db_collection='', show_name='', branch_name='', category_name='', entry_name='', task_name='' ):
        
        self.db_collection = db_collection
        self.show_name= show_name
        self.branch_name= branch_name
        self.category_name= category_name
        self.entry_name= entry_name
        self.task_name= task_name
        
        
        self.get_value()
    
    def 
    
    def get_value(self):
        db = xcon.server.xchange
        cursor = db.assets
        
        hint_path = ['tasks','modeling', 'pub_slots', 'AO_map']
        q_path = ".".join(hint_path)
        f_var = dict()
        show_name = "Test"
        entry_name = "hulk"
        
        
        find_var = {'show_name':'Test', 'entry_name':'hulk'}
        print(type(find_var))
        find_attr = {'_id':0, q_path:1}
        
        all_assets = cursor.find(find_var,find_attr)
        
        for each in list(all_assets):
            return each['tasks']

        
            
    # @property
    # def get_show_base_structure(self):
    #      try:
    #         db = xcon.server.xchange
    #         all_assets = db.show.find({"show_name": self.show_name, "active": True},
    #                                        {'_id': 0, 'structure': 1})
    #         for each in list(all_assets):
    #             return each['structure']

    #      except:
    #         pass
    
    # def get_result(self, *args, **kwargs):
    #     path = ".".join(args)
    #     print  (path)
        
    #     try:
    #         db = xcon.server.xchange
    #         all_assets = db.show.find({}, {"_id":0})
            
    #         for each in list(all_assets):
    #             return each

    #     except:
    #         pass
    
    # @classmethod
    # def get_x(cls, *args, **kwargs):
    #     return cls._get_result
    
    @classmethod
    def get_base_structure(cls, db_con):
        print ("Trying to use this shit")
        cls.db_collection = db_con
        return cls
        
    
    @classmethod
    def get_show_base_structure(cls, show_name):
         try:
            db = xcon.server.xchange
            all_assets = db.show.find({"show_name": show_name, "active": True},
                                           {'_id': 0, 'structure': 1})
            for each in list(all_assets):
                return each['structure']

         except:
            pass
        
if __name__ == "__main__":
    import pprint
    
    g = OriQuery()
    
    
    pprint.pprint (OriQuery().get_value())
    
    # g = OriQuery.get_result("structure", "sequences", show_name="Test")
    # pprint.pprint (g)