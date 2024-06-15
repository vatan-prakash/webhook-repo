from pymongo import MongoClient
from app.config import Config
from app.event_model import Event

client = MongoClient(Config.MONGO_URI)
db = client[Config.MONGO_DBNAME]
collection = db['events']

def save_event(event):
    collection.insert_one(event.to_dict())

def get_latest_events(limit=10):
    events = list(collection.find().sort('timestamp', -1).limit(limit))
    for event in events:
        event['_id'] = str(event['_id'])
    return events
