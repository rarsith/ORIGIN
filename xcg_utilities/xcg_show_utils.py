import os
from RND import xcg_config_old_not_used as xconfig
from xcg_config import xcg_validation as xvalid
from xcg_utilities import xcg_tools as xtools


def create_task(show_name, entry_name, entry_type, task_name, inputs_from, artist_name, task_status='NOT-STARTED'):
    buffer = {}
    buffer[task_name] = [{'status': 'NOT-STARTED', 'assigned_artist': None}]
    for ass_task in VALID_ASSET_DEFAULT_TASKS:
        buffer[ass_task] = ({'status': 'NOT-STARTED', 'assigned_artist': None})
def create_entry(show_name, entry_name, entry_type, entry_category):

    entry_root = os.path.join(xconfig.PROJECTS_ROOT, show_name, entry_category)

    sequences_root = os.path.join(xconfig.PROJECTS_ROOT, show_name, 'sequences')
    assets_root = os.path.join(xconfig.PROJECTS_ROOT, show_name, 'assets')
    if entry_type not in xvalid.VALID_ENTRY_CATEGORY:
        print "Please provide a valid entry type. Use one of these %s" % xvalid.VALID_ENTRY_CATEGORY
    else:
        if entry_type == 'character':
            pass
        elif entry_type == 'prop':
            pass
        elif entry_type == 'environment':
            pass
        elif entry_type == 'shot':
            pass
        elif entry_type == 'sequence':
            pass
    """Navigate to the sequences folder of the mentioned show"""

    print sequences_root
    """Check if seq_name exists, if yes, print error"""
    current_directory = os.listdir(sequences_root)
    if seq_name in current_directory:
        print "Sequence %s already exist! Please check the input" % seq_name
    else:
        try:
            path = os.path.join(sequences_root, seq_name)
            os.makedirs(path)
            print "Sequence %s created successfully" % seq_name
        except OSError as error:
            print "Directory '%s' can not be created" % seq_name


#     TODO: database update with the artist assignment
def start_task(show_name, entry_name, entry_type, entry_category, task_name, artist_name):
    valid_assets_categories = xvalid.VALID_ASSETS_CATEGORIES
    valid_shots_categories = xvalid.VALID_SHOTS_CATEGORIES
    show_root = os.path.join(xconfig.PROJECTS_ROOT, show_name)
    selected_category = []

    # Check if the selected show exists
    if show_name not in os.listdir(xconfig.PROJECTS_ROOT):
        print "Please select an existing show"
    else:
        pass

    # Check if the selected category is a valid one, if not....warn!
    if entry_category and entry_type not in (valid_assets_categories + valid_shots_categories):
        print "Wrong category specified! Check input!"

    # Check if the entry type is in the assets or sequences branch of the project
    elif entry_category and entry_type in valid_assets_categories:
        selected_category.append(os.path.join(show_root, 'assets'))

    elif entry_category and entry_type in valid_shots_categories:
        selected_category.append(os.path.join(show_root, 'sequences'))

    else:
        print "It didn't Work! Check the Damn code!"

    entry_path = os.path.join(selected_category[0], entry_category, entry_name, task_name)

    # Check if specified asset exists, if True, halt
    if entry_name not in os.listdir(os.path.join(selected_category[0], entry_category)):
        print "%s does not exist! Please check your input!" % entry_name
    elif task_name not in os.listdir(os.path.join(selected_category[0], entry_category, entry_name)):
        print "%s task does not exist! Please create it!" % task_name
    else:
        try:
            os.makedirs(os.path.join(entry_path, artist_name))
            print "%s has started the %s task" % (artist_name, task_name)
        except OSError as error:
            print"%s already assigned to the %s task. Please check input!" % (artist_name, task_name)


def create_asset(show_name, asset_name, asset_category, asset_lod='hero', assembly=False):
    asset_default_tasks = xvalid.VALID_ASSET_TASKS
    asset_tasks_schema = xvalid.VALID_ASSET_TASKS_SCHEMA
    valid_assets_categories = xvalid.VALID_ASSETS_CATEGORIES
    valid_shots_categories = xvalid.VALID_SHOTS_CATEGORIES

    show_root = os.path.join(xconfig.PROJECTS_ROOT, show_name)
    assets_root = os.path.join(xconfig.PROJECTS_ROOT, show_name, 'assets')
    category_root = os.path.join(assets_root, asset_category)

    """Check if assets root exists, if False, create it ('assets'), if True, continue"""
    if assets_root not in os.listdir(show_root):
        try:
            os.makedirs(assets_root)
        except OSError as error:
            pass
    else:
        pass

    """Check if assets category is valid, if False, halt"""
    if asset_category not in valid_assets_categories:
        print "%s not a valid asset category!" % asset_category
        print "Please use one of these %s" % valid_shots_categories
        """Check if assets category exists, if False, create it, if True, continue"""
    else:
        pass

    if asset_category not in os.listdir(assets_root):
        os.makedirs(category_root)
    else:
        pass

    """Check if asset_name exists in asset_category, if True, error, if False, create it and continue"""
    if asset_name in os.listdir(category_root):
        print "%s already exists! Please check your input" % asset_name
    else:
        try:
            asset_path = os.path.join(category_root, asset_name)
            os.makedirs(asset_path)
            xtools.write_json(asset_name, 'specs', asset_path, asset_lod=asset_lod, assembly=assembly)
            xtools.write_json(asset_name, 'tasks_linking', asset_path, linking=asset_tasks_schema)

            task_mem = xtools.write_json(asset_name, 'tasks', asset_path, tasks=asset_default_tasks)

            # make a function out of this
            items = task_mem.iteritems()
            tasks_extract = []

            for k, v in items:
                for tasks in v:
                    for keys, values in tasks.iteritems():
                        tasks_extract.append(keys)
            for each_task in tasks_extract:
                add_task = os.path.join(asset_path, each_task)
                os.makedirs(add_task)

            print "Asset %s created successfully" % asset_name
        except OSError as error:
            print "Directory '%s' can not be created" % asset_name


def create_sequence(show_name, seq_name):
    show_root = os.path.join(xconfig.PROJECTS_ROOT, show_name)
    sequences_root = os.path.join(xconfig.PROJECTS_ROOT, show_name, 'sequences')

    """Check id 'sequences' folder exists, if False, create and continue"""
    if sequences_root not in os.listdir(show_root):
        try:
            os.makedirs(sequences_root)
        except OSError as error:
            pass
    else:
        pass

    """Check if seq_name exists, if yes, print error"""
    current_directory = os.listdir(sequences_root)
    if seq_name in current_directory:
        print "Sequence %s already exist! Please check the input" % seq_name
    else:
        try:
            path = os.path.join(sequences_root, seq_name)
            os.makedirs(path)
            print "Sequence %s created successfully" % seq_name
        except OSError as error:
            print "Directory '%s' can not be created" % seq_name


def create_shot(show_name, shot_name, seq_name, tasks='shot_default', entity_status='NOT-STARTED', frame_in='1001', frame_out='1001', resx='res_default_x', resy='res_default_y', retime=None, repo=None, frame_rate='24', shot_type='vfx', motion_blur='(0.25),(-0.25)'):
    shot_default_tasks = xvalid.VALID_SHOT_TASKS
    shot_tasks_schema = xvalid.VALID_SHOT_TASKS_SCHEMA

    """Navigate to the sequences folder of the mentioned show"""
    sequences_root = os.path.join(xconfig.PROJECTS_ROOT, show_name, 'sequences')

    """Check if seq_name exists"""
    current_directory = os.listdir(sequences_root)
    selected_sequences_root = os.path.join(xconfig.PROJECTS_ROOT, show_name, 'sequences', seq_name)
    print selected_sequences_root
    """Check if shot_name exists"""
    current_selected_sequence = os.listdir(selected_sequences_root)
    if seq_name not in current_directory:
        print "Sequence %s does not exist! Please choose an existing one" % seq_name
    elif shot_name in current_selected_sequence:
        print "Shot %s already exists! Please check the input" % shot_name
    else:
        try:
            shot_path = os.path.join(sequences_root, seq_name, shot_name)
            os.makedirs(shot_path)

            xtools.write_json(shot_name, 'specs', shot_path, seq_name=seq_name, tasks=tasks, entity_status=entity_status, frame_in=frame_in, frame_out=frame_out, resx=resx, resy=resy, retime=retime, repo=repo, frame_rate=frame_rate, shot_type=shot_type, motion_blur=motion_blur)
            xtools.write_json(shot_name, 'tasks_linking', shot_path, linking=shot_tasks_schema)
            shot_tasks = xtools.write_json(shot_name, 'tasks', shot_path, tasks=shot_default_tasks)

            # make a function out of this
            items = shot_tasks.iteritems()
            tasks_extract = []

            for k, v in items:
                for tasks in v:
                    for keys, values in tasks.iteritems():
                        tasks_extract.append(keys)
            for each_task in tasks_extract:
                add_task = os.path.join(shot_path, each_task)
                os.makedirs(add_task)

            print "Shot %s created successfully" % shot_name
        except OSError as error:
            print "Directory '%s' can not be created" % shot_name











# create_sequence('TST_show', 'SPR')
# create_asset('TST_show','hulk','characters')
# create_shot('TST_show', '0888', 'SPR')
# start_task('TST_show','hulk', 'asset', 'characters','texturing','arsithra')
# start_task('TST_show','0120', 'shot', 'SPR','animation','arsithra')











