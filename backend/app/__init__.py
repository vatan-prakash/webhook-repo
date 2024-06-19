from flask import Flask
from flask import request, jsonify
from pymongo import MongoClient, errors
# from app.event_model import Event
# from datetime import datetime
from flask_cors import CORS, cross_origin
from datetime import datetime



app = Flask(__name__)
CORS(app, support_credentials=True)
# app.config.from_object('app.config.Config')

client = MongoClient('mongodb+srv://aman:jOL3wdvqr1c7NcU9@cluster0.bhjgn.mongodb.net/')
db = client['github_webhooks']
collection = db['events']

from datetime import datetime

class Event:
    def __init__(self, request_id, author, action, from_branch, to_branch, timestamp=None):
        self.request_id = request_id
        self.author = author
        self.action = action
        self.from_branch = from_branch
        self.to_branch = to_branch
        self.timestamp = timestamp or datetime.utcnow()

    def to_dict(self):
        return {
            'request_id': self.request_id,
            'author': self.author,
            'action': self.action,
            'from_branch': self.from_branch,
            'to_branch': self.to_branch,
            'timestamp': self.timestamp
        }



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
    if 'head_commit' in data and data['head_commit']['committer'] and data['head_commit']['committer']['name'] == 'GitHub':
        request_id = data['after']
        action = 'MERGE'
        author = data['sender']['login']
        to_branch = data['ref'].split('/')[-1]
        from_branch = data['head_commit']['message'].split('/')[1].split('/n')[0]
    elif 'pusher' in data:
        request_id = data['after']
        action = 'PUSH'
        author = data['pusher']['name']
        to_branch = data['ref'].split('/')[-1]
        from_branch = None
    elif 'pull_request' in data:  
        request_id = data['pull_request']['id']
        action = 'PULL_REQUEST'
        author = data['pull_request']['user']['login']
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
