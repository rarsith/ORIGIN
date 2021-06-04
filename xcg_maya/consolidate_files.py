import os
import yaml
from functools import reduce

def resolve_symlinks(input_path, destination_folder):

    for path, dirs, files in os.walk(input_path):

        for x in files:
            if x.endswith(".exr"):

                files_to_check = os.path.join(path, x)
                is_link = os.path.islink(files_to_check)


                if is_link:
                    real_path = os.path.realpath(files_to_check)

                    get_actual_file_name = os.path.split(real_path)

                    #get_parent_folder = os.path.split(get_actual_file_name[0])
                    #print get_parent_folder

                    #output_folder = os.path.join(destination_folder, get_parent_folder[1])
                    #print output_folder

                    get_end_path = os.path.join(destination_folder, get_actual_file_name[1])
                    #print get_end_path

                    if os.path.exists(get_end_path):
                        print ("File {0} already exists in the destination folder!".format(get_actual_file_name[1]))

                    else:
                        os.system ("rsync -ar --progress --exclude='*.tx' --exclude='*.jpg' --exclude='*.json' {0} {1}".format(real_path, destination_folder))

                else:
                    get_file_name = os.path.split(files_to_check)
                    print (get_file_name)
                    print (destination_folder)
                    print (files_to_check, "<<")
                    build_destination = os.path.join(destination_folder, get_file_name[1])

                    if os.path.exists(build_destination):
                        print ("File {0} already exists in the destination folder!".format(get_file_name[1]))

                    else:
                        os.system ("rsync -ar --progress --exclude='*.tx' --exclude='*.jpg' --exclude='*.json' {0} {1}".format(files_to_check, destination_folder))




multi_source_paths = {
    "source_folder" : "/corky/projects/STB_100300/library/props/stpEucalyptusIronBarkTree_ba/textures/versions/texture_set_v003/"
}


destination_folder = "/corky/projects/STB_100300/library/props/stpEucalyptusIronBarkTreeHero_ba/_tmp"


for k,v in multi_source_paths.items():
    resolve_symlinks(v, destination_folder)