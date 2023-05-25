import pymongo
import datetime

def findUserDetails(field, value, collection_name):
    """
    This function finds a document in the given collection based on the field and its value.

    Args:
        field (str): The field on which to search for the value.
        value: The value to look for in the specified field.
        collection_name (str): The name of the collection in which to search for the document.

    Returns:
        dict: The document that matches the search criteria or `None` if no document is found.
    """
    client = pymongo.MongoClient("")
    userData = {}
    db = client['turftown']
    collection = db[collection_name]
    document = collection.find_one({field: value}, {"fav_sports": 1, "fav_venues": 1, "sports_interest": 1, "followers": 1, "following": 1, "location": 1})
    # exclude the _id field from the document

    user_stats_collection = db['user_stats']
    user_stats_document = user_stats_collection.find_one({"user": document["_id"]}, {"user_id": 0})

    document.pop("_id")
    user_stats_document.pop("_id")
    user_stats_document.pop("user")

    userData = {
        "user_profile" : document,
        "user_stats" : user_stats_document
    }
    client.close()
    return userData

# function to get all the games happening in a games collection from now to 2 days from now by using the field booking_date : 2020-10-23T00:00:00.000+00:00
def getGamesByDays(num=2):

    client = pymongo.MongoClient("")
    db = client['turftown']
    collection = db['games']
    # get the current date and time
    current_date = datetime.datetime.now()
    # get the date after 2 days
    date_after_2_days = current_date + datetime.timedelta(days=num)

   # the schema for the date is 2020-10-23T00:00:00.000+00:00 and its in date type

    # find all the games that are happening from now to 2 days from now
    games = collection.find({"booking_date": {"$gte": current_date, "$lt": date_after_2_days}})
    # exclude the _id field from the document
    games_list = []
    for game in games:
        games_list.append(game)
    client.close()
    return games_list
