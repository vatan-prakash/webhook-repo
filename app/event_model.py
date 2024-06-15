from datetime import datetime

class Event:
    def __init__(self, request_id, author, action_type, from_branch, to_branch, timestamp=None):
        self.request_id = request_id
        self.author = author
        self.action_type = action_type
        self.from_branch = from_branch
        self.to_branch = to_branch
        self.timestamp = timestamp or datetime.utcnow()

    def to_dict(self):
        return {
            'request_id': self.request_id,
            'author': self.author,
            'action_type': self.action_type,
            'from_branch': self.from_branch,
            'to_branch': self.to_branch,
            'timestamp': self.timestamp
        }
