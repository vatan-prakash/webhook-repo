from flask import Flask, g
from pymongo import MongoClient

app = Flask(__name__)
app.config.from_object('app.config.Config')

def get_db():
    if 'db' not in g:
        client = MongoClient(app.config['MONGO_URI'], connect=False)
        g.db = client[app.config['MONGO_DBNAME']]
    return g.db

@app.teardown_appcontext
def close_db(exception):
    db = g.pop('db', None)

    if db is not None:
        db.client.close()

from app import routes
