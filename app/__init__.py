from flask import Flask
from flask import request, jsonify
from pymongo import MongoClient, errors
from app import app
from app.event_model import Event
from datetime import datetime

app = Flask(__name__)
app.config.from_object('app.config.Config')

client = MongoClient(app.config['MONGO_URI'])
db = client[app.config['MONGO_DBNAME']]
collection = db['events']


def save_event(event):
    collection.insert_one(event.to_dict())

def get_latest_events(limit=10):
    events = list(collection.find().sort('timestamp', -1).limit(limit))
    for event in events:
        event['_id'] = str(event['_id'])
    return events

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    event = {}
    print(data)
    if 'pusher' in data:
        request_id = data['after']
        action = 'PUSH'
        author = data['pusher']['name']
        to_branch = data['ref'].split('/')[-1]
        from_branch = None
    elif 'pull_request' in data:
        action = 'PULL_REQUEST'
        author = data['pull_request']['user']['login']
        from_branch = data['pull_request']['head']['ref']
        to_branch = data['pull_request']['base']['ref']
    elif 'action' in data and data['action'] == 'closed' and data['pull_request']['merged']:
        action = 'MERGE'
        author = data['sender']['login']
        from_branch = data['pull_request']['head']['ref']
        to_branch = data['pull_request']['base']['ref']
    else:
        return jsonify({'message': 'Unsupported event'}), 400 
    timestamp = datetime.utcnow()

    event = Event(request_id, author, action, from_branch, to_branch, timestamp)
    save_event(event)
    
    return jsonify({'message': 'Event received'}), 200

@app.route('/events', methods=['GET'])
def get_events():
    events = get_latest_events()
    return jsonify(events)
@app.route('/', methods=['GET'])
def hello():
    return "Hello, World!"
