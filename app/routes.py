from flask import request, jsonify
from datetime import datetime
import uuid
from app import app
from app.models import save_event, get_latest_events
from app.event_model import Event

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