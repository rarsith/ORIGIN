import os
import yaml
import re
from functools import reduce

asset_name = "stpEucalyptusIronBarkTreeHeroba"

input_textures_path = "/corky/projects/STB_100300/library/props/stpEucalyptusIronBarkTreeHero_ba/_tmp/"
output_textures_path = "/corky/projects/STB_100300/library/props/stpEucalyptusIronBarkTreeHero_ba/textures/"

texture_set = "map1"
channel_name_index = 2
variation = "00"
udim_index = 4
extension_index = 1
relative_path_depth =  0 #Only use negative numbers OR 0 for zero depth


def get_file_list(path):
    all_files = list()

    list_of_files = os.listdir(path)

    for files in list_of_files:

        full_path = os.path.join(path, files)

        if os.path.isdir(full_path):
            all_files = all_files + get_file_list(full_path)

        else:
            all_files.append(full_path)

    return all_files


def join_path(data_list):
    return (reduce(os.path.join,data_list))


def if_udim(data):
    default_udim="1001"

    try:
        if type(int(data)):
            return data
    except:
        return default_udim


def get_path_depth(path, depth):

    subfolders = re.split('[\][/]',path)
    clean_list = filter(len, subfolders)

    if not depth>=0:
        folders_path = clean_list[depth:]
        create_path = reduce(os.path.join,folders_path)
        final_path = os.path.normcase(os.path.join('/', create_path,' '))

        return (final_path.split())[0]
    else:
        return ""



def text_reformat(data):
    files_buffer = list()
    path_depth = get_path_depth(input_textures_path, relative_path_depth)


    for each in data:

        get_file = os.path.split(each)
        print (get_file)

        if get_file[1].endswith(".exr") or get_file[1].endswith(".tif"):

            safe_file_name = get_file[1].replace(".", "_")
            safe_file_split = safe_file_name.split("_")
            channel_name = safe_file_split[channel_name_index]
            udim = if_udim(safe_file_split[udim_index])
            extension = safe_file_split[-1:][0]
            new_file_name = (" " + path_depth + get_file[1] + ": " + asset_name + "_" + texture_set + "_" + channel_name + "_" + variation + "_" + udim + "." + extension)

            print (">> ADJUSTED NAMING >> {0}".format(new_file_name))
            files_buffer.append(new_file_name)


    return files_buffer


def write_file(data, path_to_file):

    open(path_to_file, 'w').close()
    with open(path_to_file, 'w') as f:
        f.writelines("%s\n" % "replace:")
        for content in data:
            f.writelines("%s\n" % content)
        f.close()


def main():
    yaml_file_name = asset_name + "_texture_ingestT.yaml"
    path_to_saved_list = os.path.join(output_textures_path, yaml_file_name)

    files_to_write = get_file_list(input_textures_path)
    reformat_list = text_reformat(files_to_write)
    write_file(reformat_list, path_to_saved_list)



main()