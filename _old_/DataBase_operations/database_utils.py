import os
import sqlite3
from sqlite3 import Error as sqError
from xcg_config import xcg_validation as xet


def db_connect(db_path, db_name):
    """Creates, if not created already, OR connects to a database, given a path and a database name"""
    try:
        conn = sqlite3.connect(os.path.join(db_path, (db_name)))
        print "connected to %s database" % db_name

        return conn


    except sqError as e:
        print(e)



def create_table(db_path, db_name, table_name):
    """inserts Table in selected database: given a path, database name and the table to be inserted name"""
    try:
        conn = db_connect(db_path, db_name)
        cur = conn.cursor()
        sql = 'create table if not exists ' + table_name + ' (id integer)'
        cur.execute(sql)
    except sqError as e:
        print (e)

    return table_name


def db_define_column_schema(**kwargs):
    data_list = {}
    data_list.update(kwargs)

    return data_list


def add_table_columns(db_path, db_name, table_name, column_def):
    """given a database and a table, add columns schema. Works best when a list is used to define the entries in a for loop, passing the var in column_def"""
    try:
        conn = db_connect(db_path, db_name)
        cur = conn.cursor()
        sql = 'alter table ' + table_name + ' add column' + column_def
        cur.execute(sql)
    except sqError as e:
        print (e)

    return table_name, column_def



def db_insert(db_name, db_table, item_id):
    pass
def db_update():
    pass

def create_task(task_name):
    pass

def link_task(task_name, outputs_to, inputs_from):
    pass

def add_entity_specification(spec_name, spec_value):
    pass

def create_entry(type, name, parent):
    pass

def define_bundle(entry_name):
    pass

def get_path(entity_name):
    pass

def assign_asset_to_shot(asset_name, seq_name, shot_name):
    pass

def assign_task_to_bundle():
    pass



# db_connect(xcg.PROJECTS_ROOT, 'TST_Project.db')
# create_table(xcg.PROJECTS_ROOT, 'TST_Project.db', 'MyNewFuckingTable')
# try:
#     for eeach in valid_shot_tasks:
#         add_table_columns(xcg.PROJECTS_ROOT, 'TST_Project.db', 'MyNewFuckingTable', (' ' + eeach))
# except:
#     print"nnonon"
#     pass

