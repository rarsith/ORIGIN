import json
import os
from RND.xcg_config_old_not_used import xcg_config as gld

db_example = [{'content':[{'show_name':'TST_show'},{'show_content':{'sequences':{"name":"TTT","shots":[{'name':'0010', 'frameIn':'1001','frameOut':'1001' },{'name':'0020', 'frameIn':'1001','frameOut':'1001' },{'name':'0030', 'frameIn':'1001','frameOut':'1001' }]}}}]}]



with open (os.path.join(gld.PROJECTS_ROOT, "PROJECT_DATA.json"), "w") as jdata:
    data_db = json.dump(db_example, jdata, indent=4, sort_keys=True)
    jdata.close()