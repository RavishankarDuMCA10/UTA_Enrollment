import os

class Config(object):
    SECRET_KY = os.environ.get('FLASK_SECRET_KEY') or "secret_string"

    # MONGODB_SETTINGS = { 'MONGO_URI' : 'UTA_Enrollment' }
    # MONGO_URI = "mongodb://localhost:27017/UTA_Enrollment"