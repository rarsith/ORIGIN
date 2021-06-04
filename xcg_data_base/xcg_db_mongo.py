from xcg_data_base import xcg_db_connection as xcon

def get_collections():
    db = xcon.server.xchange
    existing_collections = db.list_collection_names()

    return existing_collections





