from origin_data_base import xcg_db_connection as xcon



def db_content_summary(show_name, object_type):
    """Returns the content of the assets or the shots, paired with the parent category/sequence.
    To be used to create arrays of dictionaries to be queried for the existence of an item."""
    valid_object_types = ['assets','shots','sequences','show', 'publishes']
    db = xcon.server.xchange
    items_in_collection = []
    if object_type not in valid_object_types:
        print ("Invalid category. Try one of these {}" .format(valid_object_types))

    elif object_type == "show":
        cursor = db.show
        items = cursor.find({}, {"_id": 0, "show_name":1})
        for item in items:
            items_in_collection.append(item)

    elif object_type == "assets":
        cursor = db.assets
        items = cursor.find({"show_name":show_name}, {"_id": 0, "entry_name": 1, "category":1, "show_name":1})
        for item in items:
            items_in_collection.append(item)

    elif object_type == "sequences":
        cursor = db.sequences
        items = cursor.find({"show_name":show_name}, {"_id": 0, "entry_name": 1, "show_name":show_name})
        for item in items:
            items_in_collection.append(item)

    elif object_type == "publishes":
        cursor = db.publishes
        items = cursor.find({"show_name":show_name}, {"_id": 0, "show_name":1, "entity_name":1, "published_by":1, "version":1, "category":1})
        for item in items:
            items_in_collection.append(item)

    return items_in_collection