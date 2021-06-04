import sqlite3
import os
from RND import xcg_config_old_not_used as gld

conn = sqlite3.connect(os.path.join(gld.PROJECTS_ROOT,('TST_Project.db')))
cur = conn.cursor()




#
# c.execute ("""CREATE TABLE _sequences (seq_name, show_name)""")
# cur.execute ("""CREATE TABLE _shots (seq_name, shot_name, frameIn INTEGER, frameOut INTEGER, status text, assignee text)""")
conn.execute ("""CREATE TABLE _assets (asset_name, asset_type, asset_lod, show_name)""")
# #
# conn.commit()
# print "Tables created!"
#
#
#
#
# #######
# many_shots = [
#
#     ('TRT','0010','1001','1001','NOT-STARTED','Johnra'),
#     ('TRT','0020','1001','1001','NOT-STARTED','wohnra'),
#     ('TRT','0030','1001','1001','NOT-STARTED','sohnra'),
#     ('TRT','0040','1001','1001','NOT-STARTED','gohnra')
#
# ]
# cur.executemany ("INSERT INTO _shots VALUES (?,?,?,?,?,?)", many_shots)
# #######
# many_assets = [
#
#     ('hulk','character','hero','TRT'),
#     ('fuzzy','character','mid','TRT'),
#     ('knife','props','mid','TRT'),
#     ('forest','env','hero','TRT')
#
# ]
# cur.executemany ("INSERT INTO _assets VALUES (?,?,?,?)", many_assets)
# #######
# many_seq = [
#
#     ('TFG','TRT'),
#     ('MMK','TRT'),
#     ('TTR','TRT'),
#     ('AAS','TRT'),
#
# ]
# cur.executemany ("INSERT INTO _sequences VALUES (?,?)", many_seq)


# SELECTING ENTRIES
# cur.execute("select rowid, * from _shots")
# cur.execute("select  * from _shots where shot_name='0010'")
# cur.execute("select  * from _shots where shot_name LIKE '%10'")

# MAKING CHANGES/UPDATES TO ENTRIES
# cur.execute("select rowid, * from _shots")
# cur.execute ("""UPDATE _shots  SET status ='STARTED' WHERE assignee='Johnra' """)
# cur.execute("select rowid, * from _shots")



# DELETING RECORDS #
# cur.execute ("DELETE from   _sequences ")


# DELETING A TABLE #

#cur.execute ("DROP TABLE _shots")



# checker
# cur.execute("select * from _assets")
items = cur.fetchall()
for item in items:
    print item


conn.commit()
conn.close()







# Datatypes for SQLite
# NULL
# INTEGER
# REAL
# TEXT
# BLOB (stored as is: image file, music file)