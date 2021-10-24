import os


def create_publish_folders():
    output = 'output'
    path_to_ouput = os.path.join(proj_root, proj, br, cat, ent, ent_task, output)
    if not os.path.exists(path_to_ouput):
        os.makedirs(path_to_ouput)

    version = get_highest_folder_version(path_to_ouput)
    path_to_file = os.path.join(proj_root, proj, br, cat, ent, ent_task, output, version)

    os.makedirs(path_to_file)
    return path_to_file
    

def get_highest_folder_version(folder_path):
    all_folders = list()
    get_folders = os.listdir(folder_path)

    if not len(get_folders)<1:
        for dirs in get_folders:
            all_folders.append(dirs)
        
        highest = max(all_folders)
        get_digit = filter(None, re.split(r'(\d+)', highest))
        get_digit_list = (list(get_digit))
        
        return  "{0}{1:04d}".format(("v"),(int(get_digit_list[1])+1))      

    else:
        return "{0}{1:04d}".format(("v"),(int(1)))
        

def get_next_file_version(folder_path):
    all_files = list()
    get_files = os.listdir(folder_path)

    if not len(get_files)<1:
        for dirs in get_files:
            all_files.append(dirs)
        
        highest = max(all_files)
        get_digit = filter(None, re.split(r'(\d+)', highest))
        get_digit_list = (list(get_digit))
        
        return  "{0}{1:04d}".format(("v"),(int(get_digit_list[1])+1))      

    else:
        return "{0}{1:04d}".format(("v"),(int(1)))