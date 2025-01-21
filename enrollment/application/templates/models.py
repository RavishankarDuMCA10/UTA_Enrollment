import flask
from application import mongo
from werkzeug.security import generate_password_hash, check_password_hash
from pymongo import errors

class User():
    def __init__(self, user_id, first_name, last_name, email, password):
        self.user_id = user_id
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password
        self.create_unique_index()

    def create_unique_index(self):
        mongo.db.user.create_index(['user_id', 1], unique=True)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def get_password(self, password):
        return check_password_hash(self.password, password)

    def save(self):
        """Save the user to the MongoDB collection"""
        user_data = {
            "user_id": self.user_id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "password": self.password
        }

        try:
            # Insert user into the collection
            mongo.db.user.insert_one(user_data)
        except errors.DuplicateKeyError:
            print(f"Error: The user_id: {self.user_id} already exists.")

class Course():
    def __init__(self, course_id, title, description, credits, term):
        self.course_id = course_id
        self.title = title
        self.description = description
        self.credits = credits
        self.term = term

        self.create_unique_index()

    def create_unique_index(self):
        mongo.db.user.create_index(['course_id', 1], unique=True)
        
    def save(self):
        """Save the course to the MongoDB collection"""
        course_data = {
            "course_id" : self.course_id,
            "title" : self.title,
            "description" : self.description,
            "credits" : self.credits,
            "term" : self.term
        }
        
        try:
            # Insert course into the collection
            mongo.db.course.insert_one(course_data)
        except errors.DuplicateKeyError:
            print(f"Error: The user_id: {self.course_id} already exists.")

class Enrollment():
    def __init__(self, user_id, course_id):
        self.user_id = user_id
        self.course_id = course_id                

    def save(self):
        """Save the Enrollment to the MongoDB collection"""
        enrollment_data = {
            "user_id": self.user_id,
            "course_id" : self.course_id            
        }

        mongo.db.enrollment.insert_one(enrollment_data)