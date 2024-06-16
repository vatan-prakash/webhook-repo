from pymongo import MongoClient
from app.config import Config
from app.event_model import Event


def save_event(db, event):
    db.events.insert_one(event.to_dict())

def get_latest_events(db, limit=10):
    events = list(db.events.find().sort('timestamp', -1).limit(limit))
    for event in events:
        event['_id'] = str(event['_id'])
    return events
