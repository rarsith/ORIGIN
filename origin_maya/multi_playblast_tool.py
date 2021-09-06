import os
import re
import datetime
import maya.cmds as cmds

log=''

def logger(log_data):
    global log
    log += '\n{0}: {1}'.format(datetime.datetime.now(), log_data)
    with open('/home/arsithra/texstringAttr.log','w') as out:
        out.write(log)



def read_assets_list(file_on_disk):
    all_files = list()
    with open(file_on_disk, "r") as asset_list:
        file_content = asset_list.readlines()

        for line in file_content:
            current_place = line[:-1]
            all_files.append(current_place)

    return all_files


def get_file_name(data, extension=True):
    if not extension:
        get_file = os.path.split(data)
        clean_name = get_file[1].replace(".", "_")

        get_name = clean_name.split("_")
        new_name = "_".join(get_name[:-1])
        return new_name
    else:
        get_file = os.path.split(data)
        return get_file[1]


def get_file_path(data):
    get_file = os.path.split(data)
    return get_file[0]


def inject_path(path):
    return path


def get_next_version(folder_path):
    all_files = list()
    get_files = os.listdir(folder_path)

    if not len(get_files)<1:
        for dirs in get_files:
            all_files.append(dirs)
        highest = max(all_files)
        get_digit = filter(None, re.split(r'(\d+)', highest))
        return "{0}{1:04d}".format(('v'), int(get_digit[1])+1)
    else:
        return "{0}{1:04d}".format(('v'), int(1))


def playblast_path_compile(it_path):

    playblast_folder = get_file_name(it_path,  extension=False)
    print (playblast_folder)

    item_path = get_file_path(it_path)
    print (item_path)
    playblast_folder_path = os.path.join(item_path, playblast_folder,'')
    try:
        os.makedirs(playblast_folder_path)
    except:
        pass
    playblast_path = os.path.join(playblast_folder_path, playblast_folder)

    return playblast_path





def main(list_to_playblast, start_frame, end_frame, save_path):

    for each in list_to_playblast:
        get_version = get_next_version(save_path)
        img_seq_folder = get_file_name(each, extension=False)
        playblast_path = os.path.join(save_path, get_version, img_seq_folder)


        cmds.file(f=1,new=1)
        cmds.file(each, i=True, type="Alembic",  ignoreVersion=True, mergeNamespacesOnClash=False, ns=each)

        cmds.rangeControl(minRange=start_frame, maxRange=end_frame)
        cmds.playbackOptions (min=start_frame, max=end_frame)

        playblast_cam = cmds.camera (focalLength=55, lensSqueezeRatio=1, horizontalFilmAperture=1.4173, horizontalFilmOffset=0, verticalFilmAperture=0.9449, nearClipPlane=0.1, farClipPlane=10000, orthographic=0, orthographicWidth=30, zoom=1)

        cmds.lookThru (playblast_cam)
        cmds.viewFit (fitFactor = 0.65)

        cmds.playblast  (viewer=False, fmt="image", f=playblast_path, st=start_frame, et=end_frame, clearCache=True, showOrnaments=False, offScreen=True, fp=4, percent=100, compression="jpg",	 quality=70, fo=True, widthHeight=(960, 540)	)
        logger("{0} is file: {1}".format(get_version, each))
        print ("Done playblasting version {0} of {1}".format(get_version, each))

if __name__ == "__main__":

    save_path = '/corky/projects/STB_100300/exchange/radu/TRESS_PLAYBLASTS02/'
    assets_to_playblast = "/mnt/local/temp_storage/scratch/playblast_tool_testing/animated_vegetation_list.txt"

    start_frame = 1
    end_frame = 2

    get_each_asset = read_assets_list(assets_to_playblast)


    main(get_each_asset, start_frame, end_frame, save_path )