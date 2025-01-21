from flask import Flask, jsonify
from config import Config
# from flask_mongoengine import MongoEngine
from flask_pymongo import PyMongo

app = Flask(__name__)
app.config.from_object(Config)

app.config["MONGO_URI"] = "mongodb://localhost:27017/UTA_Enrollment"
app.config["SECRET_KEY"] = Config.SECRET_KY
app.config['DEBUG'] = True
mongo = PyMongo(app)

from application import routes

