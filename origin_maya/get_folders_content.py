import os
import yaml
from functools import reduce

asset_name = "RSP_Talo_Plants"

input_textures_path = "/corky/projects/STB_100300/library/environments/rspTaLoEnv_aa/references/from_client/RSP_20210301a/plant"
output_textures_path = "/mnt/local/temp_storage/scratch/playblast_tool_testing"


pattern = "lod100"


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



def text_reformat(data):
    files_buffer = list()


    for each in data:
        get_file = os.path.split(each)

        if get_file[1].endswith(".abc"):
            for dirpaths, dirnames, filenames in os.walk(get_file[0]):
                get_subf_list = dirpaths.split("/")

                if pattern in get_subf_list:
                    files_buffer.append(each)
                    print (dirpaths)

    return files_buffer


def write_file(data, path_to_file):

    open(path_to_file, 'w').close()
    with open(path_to_file, 'w') as f:
        for content in data:
            f.writelines("%s\n" % content)
        f.close()


def main():
    yaml_file_name = asset_name + "foldersand_files.yaml"
    path_to_saved_list = os.path.join(output_textures_path, yaml_file_name)

    files_to_write = get_file_list(input_textures_path)
    reformat_list = text_reformat(files_to_write)
    write_file(reformat_list, path_to_saved_list)



main()