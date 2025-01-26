import flask
from application import mongo
from werkzeug.security import generate_password_hash, check_password_hash
from pymongo import ASCENDING, errors

class User():
    def __init__(self, id=None, first_name=None, last_name=None, email=None, password=None):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password

    def create_unique_index(self):
        mongo.db.user.create_index(['id', 1], unique=True)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def get_password(self, user_db_password, password):
        if not user_db_password:
            print(f"not self.password: {user_db_password}")
            return False
        return check_password_hash(user_db_password, password)

    def save(self):

        if not self.id or not self.first_name or not self.last_name or not self.email or not self.password:
            print("Error: User attributes are not fully set.")
            return
        
        """Save the user to the MongoDB collection"""
        user_data = {
            "id": self.id,
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
    
    def getUser(self, email):
        users_collection = mongo.db['user']
        return users_collection.find_one({'email': email})
    
    def getUserWithId(self, id):
        users_collection = mongo.db['user']
        return users_collection.find_one({'id': id})
    
    def getUsers(self):
        users_collection = mongo.db['user']
        try:
            all_users = list(users_collection.find())
        except errors.CollectionInvalid:
            print(f"Error: Unable to get all users.")
        return all_users
    
    def aggregate(self, pipeline):
        users_collection = mongo.db['user']
        return list(users_collection.aggregate(pipeline))

class Course():
    def __init__(self, courseID=None, title=None, description=None, credits=None, term=None):
        self.courseID = courseID
        self.title = title
        self.description = description
        self.credits = credits
        self.term = term

    def create_unique_index(self):
        mongo.db.user.create_index(['courseID', 1], unique=True)
        
    def save(self):
        """Save the course to the MongoDB collection"""
        course_data = {
            "courseID" : self.courseID,
            "title" : self.title,
            "description" : self.description,
            "credits" : self.credits,
            "term" : self.term
        }
        
        try:
            # Insert course into the collection
            mongo.db.course.insert_one(course_data)
        except errors.DuplicateKeyError:
            print(f"Error: The course_id: {self.courseID} already exists.")
    
    def getCourses(self, sort_by=None):
        course_collection = mongo.db['course']
        try:
            if sort_by is None:
                all_courses = list(course_collection.find())
            else:
                all_courses = list(course_collection.find().sort(sort_by, ASCENDING))
        except errors.CollectionInvalid:
            print(f"Error: Unable to get all courses.")
        return all_courses

class Enrollment():
    def __init__(self, user_id=None, courseID=None):
        self.user_id = user_id
        self.courseID = courseID                

    def save(self):
        """Save the Enrollment to the MongoDB collection"""
        enrollment_data = {
            "user_id": self.user_id,
            "courseID" : self.courseID            
        }
        try:
            # Insert course into the collection
            mongo.db.enrollment.insert_one(enrollment_data)
        except errors.DuplicateKeyError:
            print(f"Error: The course_id: {self.courseID} already exists.")
    
    def getEnrollments(self):
        enrollment_collection = mongo.db['enrollment']
        try:
            all_enrollments = list(enrollment_collection.find())
        except errors.CollectionInvalid:
            print(f"Error: Unable to get all enrollments.")
        return all_enrollments
    
    def getEnrollment(self, user_id, courseID):
        enrollment_collection = mongo.db['enrollment']
        return enrollment_collection.find_one({'user_id': user_id, 'courseID':courseID})