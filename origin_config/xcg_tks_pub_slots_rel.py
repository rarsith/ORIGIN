from origin_config import xcg_slot_methods as xslot

# Assets

concept = {'img':{'type':'img','method':xslot.SLOTS_METHODS['m7'], 'used_by':[],'reviewable':True, 'active':True},
           'pdf':{'type':'scn','method':xslot.SLOTS_METHODS['m7'], 'used_by':[],'reviewable':True, 'active':True}}

sculpting = {'ref_geo':{'type':'geo','method':xslot.SLOTS_METHODS['m1'], 'used_by':[],'reviewable':False, 'active':True},
             'displ':{'type':'img','method':xslot.SLOTS_METHODS['m4'], 'used_by':[],'reviewable':True, 'active':True},
             'normal':{'type':'img','method':xslot.SLOTS_METHODS['m4'], 'used_by':[],'reviewable':False, 'active':True},
             'cavity':{'type':'img','method':xslot.SLOTS_METHODS['m4'], 'used_by':[],'reviewable':False, 'active':True}}

modeling = {'rend_geo':{'type':'geo','method':xslot.SLOTS_METHODS['m1'], 'used_by':[],'reviewable':True, 'active':True},
            'proxy_geo':{'type':'geo','method':xslot.SLOTS_METHODS['m1'], 'used_by':[],'reviewable':True, 'active':True},
            'utility':{'type':'geo','method':xslot.SLOTS_METHODS['m1'], 'used_by':[],'reviewable':False, 'active':True},
            'lidar':{'type':'geo','method':xslot.SLOTS_METHODS['m1'], 'used_by':[],'reviewable':False, 'active':True},
            'proj_geo':{'type':'geo','method':xslot.SLOTS_METHODS['m1'], 'used_by':[],'reviewable':False, 'active':True},
            'vport_mat':{'type':'scn','method':xslot.SLOTS_METHODS['m11'], 'used_by':[],'reviewable':False, 'active':True},
            'tex_object':{'type':'geo','method':xslot.SLOTS_METHODS['m1'], 'used_by':[],'reviewable':False, 'active':True},
            'curvature_map':{'type':'img','method':xslot.SLOTS_METHODS['m4'], 'used_by':[],'reviewable':True, 'active':True},
            'ao_map':{'type':'img','method':xslot.SLOTS_METHODS['m4'], 'used_by':[],'reviewable':True, 'active':True},
            'selection_map':{'type':'img','method':xslot.SLOTS_METHODS['m4'], 'used_by':[],'reviewable':True, 'active':True}}

detailpass = {'displ':{'type':'img','method':xslot.SLOTS_METHODS['m4'], 'used_by':[],'reviewable':True, 'active':True},
              'normal':{'type':'img','method':xslot.SLOTS_METHODS['m4'], 'used_by':[],'reviewable':False, 'active':True},
              'cavity':{'type':'img','method':xslot.SLOTS_METHODS['m4'], 'used_by':[],'reviewable':False, 'active':True}}

texturing = {'texture_set':{'type':'img','method':xslot.SLOTS_METHODS['m7'], 'used_by':[],'reviewable':True, 'active':True},
             'vport_tex':{'type':'img','method':xslot.SLOTS_METHODS['m7'],'used_by':[],'reviewable':True, 'active':True},
             'groom_maps':{'type':'img','method':xslot.SLOTS_METHODS['m7'], 'used_by':[],'reviewable':True, 'active':True},
             'util_maps':{'type':'img','method':xslot.SLOTS_METHODS['m7'], 'used_by':[],'reviewable':True, 'active':True}}

rigging = {'render_rig':{'type':'scn','method':xslot.SLOTS_METHODS['m6'], 'used_by':[],'reviewable':True, 'active':True},
           'proxy_rig':{'type':'scn','method':xslot.SLOTS_METHODS['m6'], 'used_by':[],'reviewable':True, 'active':True},
           'cmuscle_rig':{'type':'scn','method':xslot.SLOTS_METHODS['m6'], 'used_by':[],'reviewable':True, 'active':True},
           'util_rig':{'type':'scn','method':xslot.SLOTS_METHODS['m6'], 'used_by':[],'reviewable':False, 'active':True}}

groom = {'groom_set':{'type':'csh','method':xslot.SLOTS_METHODS['m6'], 'used_by':[],'reviewable':True, 'active':True},
         'guides':{'type':'csh','method':xslot.SLOTS_METHODS['m6'], 'used_by':[],'reviewable': 'False', 'active':True}}

surfacing = {'look_dev':{'type':'cfg','method':xslot.SLOTS_METHODS['m6'], 'used_by':[],'reviewable':True, 'active':True}}

cfx_setup = {'cloth_setup':{'type':'scn','method':xslot.SLOTS_METHODS['m6'], 'used_by':[],'reviewable':False, 'active':True},
             'fur_setup':{'type':'scn','method':xslot.SLOTS_METHODS['m6'], 'used_by':[],'reviewable':False, 'active':True},
             'feathers_setup':{'type':'scn','method':xslot.SLOTS_METHODS['m6'], 'used_by':[],'reviewable':False, 'active':True}}

fx_setup = {'bgeo':{'type':'geo','method':xslot.SLOTS_METHODS['m6'], 'used_by':[],'reviewable':False, 'active':True},
            'vdb':{'type':'csh','method':xslot.SLOTS_METHODS['m6'], 'used_by':[],'reviewable':False, 'active':True}}

# Shots
plateio = {'master':{'type':'img','method':xslot.SLOTS_METHODS['m7'], 'used_by':[],'reviewable':False, 'active':True},
           'vport':{'type':'img','method':xslot.SLOTS_METHODS['m7'], 'used_by':[],'reviewable':False, 'active':True}}

cam_track ={'distortion':{'type':'cfg','method':xslot.SLOTS_METHODS['m12'], 'used_by':[],'reviewable':False, 'active':True},
            'shot_cam':{'type':'csh','method':xslot.SLOTS_METHODS['m2'], 'used_by':[],'reviewable':False, 'active':True},
            'HO':{'type':'csh','method':xslot.SLOTS_METHODS['m1'], 'used_by':[],'reviewable':False, 'active':True},
            'locators':{'type':'img','method':xslot.SLOTS_METHODS['m1'], 'used_by':[],'reviewable':False, 'active':True},
            'wit_cam_01':{'type':'csh','method':xslot.SLOTS_METHODS['m2'], 'used_by':[],'reviewable':False, 'active':True},
            'wit_cam_02':{'type':'csh','method':xslot.SLOTS_METHODS['m2'], 'used_by':[],'reviewable':False, 'active':True},
            'wit_cam_03':{'type':'csh','method':xslot.SLOTS_METHODS['m2'], 'used_by':[],'reviewable':False, 'active':True},
            'wit_cam_04':{'type':'csh','method':xslot.SLOTS_METHODS['m2'], 'used_by':[],'reviewable':False, 'active':True},
            'wit_cam_05':{'type':'csh','method':xslot.SLOTS_METHODS['m2'], 'used_by':[],'reviewable':False, 'active':True}}

body_track = {'rend_geo':{'type':'csh','method':xslot.SLOTS_METHODS['m2'], 'used_by':[],'reviewable':True, 'active':True},
              'proxy_geo':{'type':'csh','method':xslot.SLOTS_METHODS['m2'], 'used_by':[],'reviewable':True, 'active':True},
              'util_geo':{'type':'csh','method':xslot.SLOTS_METHODS['m2'], 'used_by':[],'reviewable':False, 'active':True},
              'util_rig':{'type':'csh','method':xslot.SLOTS_METHODS['m2'], 'used_by':[],'reviewable':False, 'active':True},
              'anm_crv':{'type':'cfg','method':xslot.SLOTS_METHODS['m8'], 'used_by':[],'reviewable':False, 'active':True}}

layout = {'positions':{'type':'cfg','method':xslot.SLOTS_METHODS['m9'], 'used_by':[],'reviewable':False, 'active':True},
          'content':{'type':'cfg','method':xslot.SLOTS_METHODS['m13'], 'used_by':[],'reviewable':False, 'active':True},
          'shot_cam':{'type':'csh','method':xslot.SLOTS_METHODS['m2'], 'used_by':[],'reviewable':False, 'active':True},
          'anm_crv':{'type':'cfg','method':xslot.SLOTS_METHODS['m8'], 'used_by':[],'reviewable':False, 'active':True},
          'proj_geo':{'type':'csh','method':xslot.SLOTS_METHODS['m2'], 'used_by':[],'reviewable':False, 'active':True},
          'tags':{'type':'cfg','method':xslot.SLOTS_METHODS['m13'], 'used_by':[],'reviewable':False, 'active':True}}

animation = {'rend_geo':{'type':'csh','method':xslot.SLOTS_METHODS['m2'], 'used_by':[],'reviewable':True, 'active':True},
          'proxy_geo':{'type':'csh','method':xslot.SLOTS_METHODS['m2'], 'used_by':[],'reviewable':True, 'active':True},
          'util_geo':{'type':'csh','method':xslot.SLOTS_METHODS['m2'], 'used_by':[],'reviewable':False, 'active':True},
          'util_rig':{'type':'csh','method':xslot.SLOTS_METHODS['m2'], 'used_by':[],'reviewable':False, 'active':True},
          'anm_crv':{'type':'cfg','method':xslot.SLOTS_METHODS['m8'], 'used_by':[],'reviewable':False, 'active': 'True'},
          'shot_cam': {'type': 'csh', 'method':xslot.SLOTS_METHODS['m2'], 'used_by':[],'reviewable': False, 'active': True}}

cfx ={'rend_geo':{'type':'csh','method':xslot.SLOTS_METHODS['m2'], 'used_by':[],'reviewable':True, 'active':True},
      'proxy_geo':{'type':'csh','method':xslot.SLOTS_METHODS['m2'], 'used_by':[],'reviewable':True, 'active':True}}

fx = {'rend_geo':{'type':'img','method':xslot.SLOTS_METHODS['m7'], 'used_by':[],'reviewable':True, 'active':True},
      'light_geo':{'type':'csh','method':xslot.SLOTS_METHODS['m2'], 'used_by':[],'reviewable':True, 'active':True},
      'vdb':{'type':'csh','method':xslot.SLOTS_METHODS['m6'], 'used_by':[],'reviewable':True, 'active':True}}

shot_sculpt = {'rend_geo':{'type':'csh','method':xslot.SLOTS_METHODS['m2'], 'used_by':[],'reviewable':True, 'active':True}}

lighting_and_rendering = {'render_set':{'type':'img','method':xslot.SLOTS_METHODS['m7'], 'used_by':[],'reviewable':True, 'active':True}}

roto ={'roto_out':{'type':'img','method':xslot.SLOTS_METHODS['m7'], 'used_by':[],'reviewable':True, 'active':True}}

paint = {'paint_out':{'type':'img','method':xslot.SLOTS_METHODS['m7'], 'used_by':[],'reviewable':True, 'active':True}}

compositing = {'comp_out':{'type':'img','method':xslot.SLOTS_METHODS['m7'], 'used_by':[],'reviewable':True, 'active':True}}

retime = {'retime_crv':{'type':'cfg','method':xslot.SLOTS_METHODS['m8'], 'used_by':[],'reviewable':True, 'active':True},
          'retime_img':{'type':'img','method':xslot.SLOTS_METHODS['m7'], 'used_by':[],'reviewable':True, 'active':True}}

repo = {'repo_data':{'type':'cfg','method':xslot.SLOTS_METHODS['m13'], 'used_by':[],'reviewable':True, 'active':True}}




