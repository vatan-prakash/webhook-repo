from flask import Flask
from pymongo import MongoClient

app = Flask(__name__)
app.config.from_object('app.config.Config')

client = MongoClient(app.config['MONGO_URI'], connect=False)
db = client[app.config['MONGO_DBNAME']]

from app import routes
