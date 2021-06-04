import os
import yaml
import re
from functools import reduce

asset_name = "ropeDartba"

input_textures_path = "/corky/projects/STB_100300/Correspondence/MailIn/20210505_WTA_SharePack/WTA_20210504/_asset/ropedart/chrXiaLingWdr_ropeDart/texture_hero/"
output_textures_path = "/corky/projects/STB_100300/library/props/ropeDart_ba/textures/"

texture_set = "map1"
channel_name_index = 0
variation = "00"
udim_index = 1
extension_index = 1



def get_subfolders(path):
    all_files = list()
    for dirnames, subfolders, files in os.walk(path):
        for file_name in files:
            if file_name.endswith(".exr") or file_name.endswith(".tif"):
                rel_dir = os.path.relpath(dirnames, path)
                rel_file = os.path.join(rel_dir, file_name)
                all_files.append(rel_file)


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



def text_reformat(data):
    files_buffer = list()

    for each in data:
        get_file = os.path.split(each)


        if get_file[1].endswith(".exr") or get_file[1].endswith(".tif"):

            safe_file_name = get_file[1].replace(".", "_")
            safe_file_split = safe_file_name.split("_")
            channel_name = safe_file_split[channel_name_index]
            udim = if_udim(safe_file_split[udim_index])
            extension = safe_file_split[-1:][0]
            new_file_name = (" " + each + ": " + asset_name + "_" + texture_set + "_" + channel_name + "_" + variation + "_" + udim + "." + extension)

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
    yaml_file_name = asset_name + "_texture_ingest.yaml"
    path_to_saved_list = os.path.join(output_textures_path, yaml_file_name)

    files_to_write = get_subfolders(input_textures_path)
    reformat_list = text_reformat(files_to_write)
    write_file(reformat_list, path_to_saved_list)



main()