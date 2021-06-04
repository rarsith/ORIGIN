import pymongo
from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017')
db = client["acme"]
myCol = db["dbtable"]
print db
db.dbtable.find()



# SEED_DATA =[
#     {
#         'decade': '1970s',
#         'artist': 'Debby Boone',
#         'song': 'You Light Up My Life',
#         'weeksAtOne': 10
#     },
#     {
#         'decade': '1980s',
#         'artist': 'Olivia Newton-John',
#         'song': 'Physical',
#         'weeksAtOne': 10
#     },
#     {
#         'decade': '1990s',
#         'artist': 'Mariah Carey',
#         'song': 'One Sweet Day',
#         'weeksAtOne': 16
#     }
# ]

# result = db.dbtable.insert_many(SEED_DATA)
result = db.dbtable.find()
for each in result:
    for e in each:
        print result



