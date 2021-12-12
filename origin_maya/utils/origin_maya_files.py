import importlib


import origin_utilities.origin_os as oos
importlib.reload(oos)

import origin_utilities.origin_env as oenv
importlib.reload(oenv)

def save_maya_file():
    path_to_folder = oos.wip_output_path()
    file_name = oos.build_wip_file_name(path_to_folder)
    full_path = path_to_folder + file_name
    
    cmds.file(rename=full_path )
    cmds.file(save=True, type='mayaBinary' )
    cmds.select (cl=True)
    
    print ("Saved successfully: {1}{0}".format(file_name, path_to_folder ))



if __name__ == "__main__":

    save_maya_file()