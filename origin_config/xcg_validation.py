from origin_config import xcg_tks_pub_slots as xpubs

VALID_ASSET_DEFAULT_TASKS = ['concept','sculpting','modeling','texturing','rigging','groom','cfx_setup','fx_setup','surfacing','facs',]
VALID_SHOT_DEFAULT_TASKS = ['animation','cfx','fx','cam_track','light_rend','compositing','plateio','body_track','shot_sculpt','comp','paint','roto','retime','repo']
VALID_DB_ENTITIES = ['db_root','db_group','db_descriptor']
VALID_ENTITIES = ['ROOT','GROUP','SUBGROUP']
VALID_ASSETS_CATEGORIES = ['characters', 'props', 'environments']
VALID_SHOTS_CATEGORIES = ['shots', 'sequences']
VALID_SHOTS_TYPES = ['vfx', 'fullcg']

VALID_TASK_STATUSES = ["NOT-STARTED", "IN-PROGRESS", "ON-HOLD", "SKIP", "PENDING-REVIEW", "TWEAK", "FINAL"]

VALID_SHOW_BRANCHES = ['assets', 'shots', 'sequences', None, '']

VALID_SHOW_SPECS = [{'show_code':'', 'show_longname':'','show_type':'vfx'}]

VALID_ASSET_TASKS_SCHEMA = {  'concept':            {'active': True, 'status': 'NOT-STARTED', 'artist': 'None', 'imports_from': {}, 'pub_slots': xpubs.concept},
                              'sculpting':          {'active': True, 'status': 'NOT-STARTED', 'artist': 'None', 'imports_from': {'concept': {}}, 'pub_slots': xpubs.sculpting},
                              'modeling':           {'active': True, 'status': 'NOT-STARTED', 'artist': 'None', 'imports_from': {'concept': {}, 'sculpting': {}}, 'pub_slots': xpubs.modeling},
                              'texturing':          {'active': True, 'status': 'NOT-STARTED', 'artist': 'None', 'imports_from': {'modeling': {}}, 'pub_slots': xpubs.texturing},
                              'rigging':            {'active': True, 'status': 'NOT-STARTED', 'artist': 'None', 'imports_from': {'modeling': {}, 'facs': {}}, 'pub_slots': xpubs.rigging},
                              'groom':              {'active': True, 'status': 'NOT-STARTED', 'artist': 'None', 'imports_from': {'modeling': {}, 'texturing': {}}, 'pub_slots': xpubs.groom},
                              'cfx_set':            {'active': True, 'status': 'NOT-STARTED', 'artist': 'None', 'imports_from': {'modeling': {}, 'groom': {}}, 'pub_slots': xpubs.cfx_setup},
                              'fx_set':             {'active': True, 'status': 'NOT-STARTED', 'artist': 'None', 'imports_from': {'modeling': {}}, 'pub_slots': xpubs.fx_setup},
                              'surfacing':          {'active': True, 'status': 'NOT-STARTED', 'artist': 'None', 'imports_from': {'modeling': {}, 'texturing': {}, 'groom': {}}, 'pub_slots': xpubs.surfacing},
                              'facs':               {'active': True, 'status': 'NOT-STARTED', 'artist': 'None', 'imports_from': {'modeling': {}, 'texturing': {}}, 'pub_slots': xpubs.facs}}


VALID_ASSET_TASKS_SCHEMA_CHARACTERS = {  'concept':            {'active': True, 'status': 'NOT-STARTED', 'artist': 'None', 'imports_from': {}, 'pub_slots': xpubs.concept},
                              'sculpting':          {'active': True, 'status': 'NOT-STARTED', 'artist': 'None', 'imports_from': {'concept': {}}, 'pub_slots': xpubs.sculpting},
                              'modeling':           {'active': True, 'status': 'NOT-STARTED', 'artist': 'None', 'imports_from': {'concept': {}, 'sculpting': {}}, 'pub_slots': xpubs.modeling},
                              'texturing':          {'active': True, 'status': 'NOT-STARTED', 'artist': 'None', 'imports_from': {'modeling': {}}, 'pub_slots': xpubs.texturing},
                              'rigging':            {'active': True, 'status': 'NOT-STARTED', 'artist': 'None', 'imports_from': {'modeling': {}, 'facs': {}}, 'pub_slots': xpubs.rigging},
                              'groom':              {'active': True, 'status': 'NOT-STARTED', 'artist': 'None', 'imports_from': {'modeling': {}, 'texturing': {}}, 'pub_slots': xpubs.groom},
                              'cfx_set':            {'active': True, 'status': 'NOT-STARTED', 'artist': 'None', 'imports_from': {'modeling': {}, 'groom': {}}, 'pub_slots': xpubs.cfx_setup},
                              'fx_set':             {'active': True, 'status': 'NOT-STARTED', 'artist': 'None', 'imports_from': {'modeling': {}}, 'pub_slots': xpubs.fx_setup},
                              'surfacing':          {'active': True, 'status': 'NOT-STARTED', 'artist': 'None', 'imports_from': {'modeling': {}, 'texturing': {}, 'groom': {}}, 'pub_slots': xpubs.surfacing},
                              'facs':               {'active': True, 'status': 'NOT-STARTED', 'artist': 'None', 'imports_from': {'modeling': {}, 'texturing': {}}, 'pub_slots': xpubs.facs}}

VALID_ASSET_TASKS_SCHEMA_PROPS = {  'concept':            {'active': True, 'status': 'NOT-STARTED', 'artist': 'None', 'imports_from': {}, 'pub_slots': xpubs.concept},
                              'sculpting':          {'active': True, 'status': 'NOT-STARTED', 'artist': 'None', 'imports_from': {'concept': {}}, 'pub_slots': xpubs.sculpting},
                              'modeling':           {'active': True, 'status': 'NOT-STARTED', 'artist': 'None', 'imports_from': {'concept': {}, 'sculpting': {}}, 'pub_slots': xpubs.modeling},
                              'texturing':          {'active': True, 'status': 'NOT-STARTED', 'artist': 'None', 'imports_from': {'modeling': {}}, 'pub_slots': xpubs.texturing},
                              'rigging':            {'active': True, 'status': 'NOT-STARTED', 'artist': 'None', 'imports_from': {'modeling': {}, 'facs': {}}, 'pub_slots': xpubs.rigging},
                              'groom':              {'active': True, 'status': 'NOT-STARTED', 'artist': 'None', 'imports_from': {'modeling': {}, 'texturing': {}}, 'pub_slots': xpubs.groom},
                              'cfx_set':            {'active': True, 'status': 'NOT-STARTED', 'artist': 'None', 'imports_from': {'modeling': {}, 'groom': {}}, 'pub_slots': xpubs.cfx_setup},
                              'fx_set':             {'active': True, 'status': 'NOT-STARTED', 'artist': 'None', 'imports_from': {'modeling': {}}, 'pub_slots': xpubs.fx_setup},
                              'surfacing':          {'active': True, 'status': 'NOT-STARTED', 'artist': 'None', 'imports_from': {'modeling': {}, 'texturing': {}, 'groom': {}}, 'pub_slots': xpubs.surfacing},
                              }

VALID_ASSET_TASKS_SCHEMA_ENVIRONMENTS = {  'concept':            {'active': True, 'status': 'NOT-STARTED', 'artist': 'None', 'imports_from': {}, 'pub_slots': xpubs.concept},
                              'scattering':           {'active': True, 'status': 'NOT-STARTED', 'artist': 'None', 'imports_from': {'concept': {}, 'sculpting': {}}, 'pub_slots': xpubs.modeling},
                              'surfacing':          {'active': True, 'status': 'NOT-STARTED', 'artist': 'None', 'imports_from': {'modeling': {}, 'texturing': {}, 'groom': {}}, 'pub_slots': xpubs.surfacing},
                              }

VALID_ASSET_TASKS_SCHEMA_VEHICLES = {  'concept':            {'active': True, 'status': 'NOT-STARTED', 'artist': 'None', 'imports_from': {}, 'pub_slots': xpubs.concept},
                              'sculpting':          {'active': True, 'status': 'NOT-STARTED', 'artist': 'None', 'imports_from': {'concept': {}}, 'pub_slots': xpubs.sculpting},
                              'modeling':           {'active': True, 'status': 'NOT-STARTED', 'artist': 'None', 'imports_from': {'concept': {}, 'sculpting': {}}, 'pub_slots': xpubs.modeling},
                              'texturing':          {'active': True, 'status': 'NOT-STARTED', 'artist': 'None', 'imports_from': {'modeling': {}}, 'pub_slots': xpubs.texturing},
                              'rigging':            {'active': True, 'status': 'NOT-STARTED', 'artist': 'None', 'imports_from': {'modeling': {}, 'facs': {}}, 'pub_slots': xpubs.rigging},
                              'cfx_set':            {'active': True, 'status': 'NOT-STARTED', 'artist': 'None', 'imports_from': {'modeling': {}, 'groom': {}}, 'pub_slots': xpubs.cfx_setup},
                              'fx_set':             {'active': True, 'status': 'NOT-STARTED', 'artist': 'None', 'imports_from': {'modeling': {}}, 'pub_slots': xpubs.fx_setup},
                              'surfacing':          {'active': True, 'status': 'NOT-STARTED', 'artist': 'None', 'imports_from': {'modeling': {}, 'texturing': {}, 'groom': {}}, 'pub_slots': xpubs.surfacing}}

VALID_ASSET_TASKS_SCHEMA_BUILDINGS = {  'concept':            {'active': True, 'status': 'NOT-STARTED', 'artist': 'None', 'imports_from': {}, 'pub_slots': xpubs.concept},
                              'sculpting':          {'active': True, 'status': 'NOT-STARTED', 'artist': 'None', 'imports_from': {'concept': {}}, 'pub_slots': xpubs.sculpting},
                              'modeling':           {'active': True, 'status': 'NOT-STARTED', 'artist': 'None', 'imports_from': {'concept': {}, 'sculpting': {}}, 'pub_slots': xpubs.modeling},
                              'texturing':          {'active': True, 'status': 'NOT-STARTED', 'artist': 'None', 'imports_from': {'modeling': {}}, 'pub_slots': xpubs.texturing},
                              'rigging':            {'active': True, 'status': 'NOT-STARTED', 'artist': 'None', 'imports_from': {'modeling': {}, 'facs': {}}, 'pub_slots': xpubs.rigging},
                              'cfx_set':            {'active': True, 'status': 'NOT-STARTED', 'artist': 'None', 'imports_from': {'modeling': {}, 'groom': {}}, 'pub_slots': xpubs.cfx_setup},
                              'fx_set':             {'active': True, 'status': 'NOT-STARTED', 'artist': 'None', 'imports_from': {'modeling': {}}, 'pub_slots': xpubs.fx_setup},
                              'surfacing':          {'active': True, 'status': 'NOT-STARTED', 'artist': 'None', 'imports_from': {'modeling': {}, 'texturing': {}, 'groom': {}}, 'pub_slots': xpubs.surfacing},
                              }

VALID_ASSET_TASKS_SCHEMA_VEGETATION = {  'concept':            {'active': True, 'status': 'NOT-STARTED', 'artist': 'None', 'imports_from': {}, 'pub_slots': xpubs.concept},
                              'sculpting':          {'active': True, 'status': 'NOT-STARTED', 'artist': 'None', 'imports_from': {'concept': {}}, 'pub_slots': xpubs.sculpting},
                              'modeling':           {'active': True, 'status': 'NOT-STARTED', 'artist': 'None', 'imports_from': {'concept': {}, 'sculpting': {}}, 'pub_slots': xpubs.modeling},
                              'texturing':          {'active': True, 'status': 'NOT-STARTED', 'artist': 'None', 'imports_from': {'modeling': {}}, 'pub_slots': xpubs.texturing},
                              'rigging':            {'active': True, 'status': 'NOT-STARTED', 'artist': 'None', 'imports_from': {'modeling': {}, 'facs': {}}, 'pub_slots': xpubs.rigging},
                              'groom':              {'active': True, 'status': 'NOT-STARTED', 'artist': 'None', 'imports_from': {'modeling': {}, 'texturing': {}}, 'pub_slots': xpubs.groom},
                              'cfx_set':            {'active': True, 'status': 'NOT-STARTED', 'artist': 'None', 'imports_from': {'modeling': {}, 'groom': {}}, 'pub_slots': xpubs.cfx_setup},
                              'fx_set':             {'active': True, 'status': 'NOT-STARTED', 'artist': 'None', 'imports_from': {'modeling': {}}, 'pub_slots': xpubs.fx_setup},
                              'surfacing':          {'active': True, 'status': 'NOT-STARTED', 'artist': 'None', 'imports_from': {'modeling': {}, 'texturing': {}, 'groom': {}}, 'pub_slots': xpubs.surfacing},
                              }


VALID_SHOT_TASKS_SCHEMA ={  'plateio':                  {'active': True, 'status': 'NOT-STARTED', 'artist': 'None', 'imports_from': {}, 'pub_slots': xpubs.plateio, 'subtask': {}},
                            'cam_track':                {'active': True, 'status': 'NOT-STARTED', 'artist': 'None', 'imports_from': {'plateio': {}}, 'pub_slots': xpubs.cam_track},
                            'body_track':               {'active': True, 'status': 'NOT-STARTED', 'artist': 'None', 'imports_from': {'cam_track': {}, 'plateio': {}}, 'pub_slots': xpubs.body_track},
                            'layout':                   {'active': True, 'status': 'NOT-STARTED', 'artist': 'None', 'imports_from': {'cam_track': {}, 'plateio': {}}, 'pub_slots': xpubs.layout},
                            'animation':                {'active': True, 'status': 'NOT-STARTED', 'artist': 'None', 'imports_from': {'cam_track': {}, 'plateio': {}}, 'pub_slots': xpubs.animation},
                            'cfx':                      {'active': True, 'status': 'NOT-STARTED', 'artist': 'None', 'imports_from': {'animation': {}, 'body_track': {}, 'cam_track': {}, 'layout': {}}, 'pub_slots': xpubs.cfx},
                            'fx':                       {'active': True, 'status': 'NOT-STARTED', 'artist': 'None', 'imports_from': {'animation': {}, 'body_track': {}, 'cam_track': {}, 'layout': {}, 'plateio': {}}, 'pub_slots': xpubs.fx},
                            'shot_sculpt':              {'active': True, 'status': 'NOT-STARTED', 'artist': 'None', 'imports_from': {'animation': {}, 'body_track': {}, 'cam_track': {}, 'layout': {}, 'plateio': {}}, 'pub_slots': xpubs.shot_sculpt},
                            'light_rend':               {'active': True, 'status': 'NOT-STARTED', 'artist': 'None', 'imports_from': {'animation': {}, 'body_track': {}, 'cam_track': {}, 'layout': {}, 'plateio': {}, 'fx': {}, 'cfx': {}}, 'pub_slots': xpubs.lighting_and_rendering},
                            'roto':                     {'active': True, 'status': 'NOT-STARTED', 'artist': 'None', 'imports_from': {'plateio': {}, 'cam_track': {}}, 'pub_slots': xpubs.roto},
                            'paint':                    {'active': True, 'status': 'NOT-STARTED', 'artist': 'None', 'imports_from': {'plateio': {}, 'cam_track': {}}, 'pub_slots': xpubs.paint},
                            'compositing':              {'active': True, 'status': 'NOT-STARTED', 'artist': 'None', 'imports_from': {'retime': {}, 'repo': {}, 'light_rend': {}, 'paint': {}, 'roto': {}}, 'pub_slots': xpubs.compositing},
                            'retime':                   {'active': True, 'status': 'NOT-STARTED', 'artist': 'None', 'imports_from': {'plateio': {}}, 'pub_slots':xpubs.retime},
                            'repo':                     {'active': True, 'status': 'NOT-STARTED', 'artist': 'None', 'imports_from': {'cam_track': {}, 'plateio': {}}, 'pub_slots': xpubs.repo}}

ASSETS_TASKS_DEPENDENCIES = {'concept':'',
                             'sculpting':'',
                             'modeling':'',
                             'texturing':'',
                             'rigging':'',
                             'groom':'',
                             'cfx_set':'',
                             'fx_set':'',
                             'surfacing':'',
                             'facs':''}

SHOTS_TASKS_DEPENDENCIES = {'plateio':'',
                            'cam_track':['retime', 'layout'],
                            'body_track':'',
                            'layout':'',
                            'animation':['shot_sculpt'],
                            'cfx':['shot_sculpt'],
                            'fx':'',
                            'shot_sculpt':'',
                            'light_rend':['repo'],
                            'roto':'',
                            'paint':'',
                            'compositing':'',
                            'retime':'',
                            'repo':''}

SLOTS_TYPES = ['abc', 'tex', 'vdb', 'bgeo', 'ptc', 'rend', 'exr', 'mat', 'pbr','img','scn', 'geo', 'csh', 'cfg']

SLOTS_METHODS = {'m1':'sf_csh',
                 'm2':'mf_csh',
                 'm3':'sf_geo',
                 'm4':'geo_bake',
                 'm5':'geo_sim',
                 'm6':'scn_exp',
                 'm7':'img_exp',
                 'm8':'anm_crv',
                 'm9':'scatter',
                 'm10':'p_exp',
                 'm11':'assign_exp',
                 'm12':'cfg_scn_exp',
                 'm13':'cfg_exp'}

DEFAULT_SHOT_DEFINITION = {'full_range_in':'ingest plates',
                           'full_range_out':'ingest plates',
                           'frame_in': '1001',
                           'frame_out': '1001',
                           'handles_head': '8',
                           'handles_tail': '8',
                           'preroll': '10',
                           'shot_type': 'vfx',
                           'cut_in':'',
                           'cut_out':'',
                           'frame_rate': '24',
                           'motion_blur_high': 0.25,
                           'motion_blur_low': -0.25,
                           'res_x': 'ingest plates',
                           'res_y': 'ingest plates'}

DEFAULT_ASSET_DEFINITION = {'asset_lod':'hero',
                            'assembly':False}
