
from application.templates.models import User

def course_list(user_id):
    user_object = User()
    classes = list(user_object.aggregate([
            {
                '$lookup': {
                    'from': 'enrollment', 
                    'localField': 'id', 
                    'foreignField': 'user_id', 
                    'as': 'r1'
                }
            }, {
                '$unwind': {
                    'path': '$r1', 
                    'includeArrayIndex': 'r1_id', 
                    'preserveNullAndEmptyArrays': False
                }
            }, {
                '$lookup': {
                    'from': 'course', 
                    'localField': 'r1.courseID', 
                    'foreignField': 'courseID', 
                    'as': 'r2'
                }
            }, {
                '$unwind': {
                    'path': '$r2', 
                    'preserveNullAndEmptyArrays': False
                }
            }, {
                '$match': {
                    'id': user_id
                }
            }, {
                '$sort': {
                    'courseID': 1
                }
            }
        ]))
    return classes