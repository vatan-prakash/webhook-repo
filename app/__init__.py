from flask import Flask
from pymongo import MongoClient

app = Flask(__name__)
app.config.from_object('app.config.Config')

def get_mongo_client():
    return MongoClient(app.config['MONGO_URI'])

client = get_mongo_client()
db = client[app.config['MONGO_DBNAME']]

from app import routes
