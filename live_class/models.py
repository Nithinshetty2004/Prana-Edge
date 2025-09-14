from datetime import datetime
from .database import courses_collection, enrollments_collection, chats_collection

class Course:
    @staticmethod
    def create(course_data, created_by):
        course = {
            "course_name": course_data.get('course_name'),
            "instructor": course_data.get('instructor'),
            "description": course_data.get('description'),
            "duration": course_data.get('duration'),
            "level": course_data.get('level'),
            "schedule": course_data.get('schedule'),
            "max_participants": course_data.get('max_participants'),
            "created_by": created_by,
            "created_at": datetime.utcnow(),
            "is_active": True
        }
        return courses_collection.insert_one(course)

    @staticmethod
    def find_by_name(course_name):
        return courses_collection.find_one({
            "course_name": course_name,
            "is_active": True
        })

    @staticmethod
    def find_all_active():
        return list(courses_collection.find({"is_active": True}))

    @staticmethod
    def exists(course_name):
        return courses_collection.find_one({"course_name": course_name}) is not None

    @staticmethod
    def delete(course_name):
        return courses_collection.update_one(
            {"course_name": course_name, "is_active": True},
            {"$set": {"is_active": False, "deleted_at": datetime.utcnow()}}
        )

class Enrollment:
    @staticmethod
    def create(course_name, username):
        enrollment = {
            "course_name": course_name,
            "username": username,
            "enrolled_at": datetime.utcnow(),
            "status": "active"
        }
        return enrollments_collection.insert_one(enrollment)

    @staticmethod
    def find_user_enrollment(course_name, username):
        return enrollments_collection.find_one({
            "course_name": course_name,
            "username": username
        })

    @staticmethod
    def count_active_enrollments(course_name):
        return enrollments_collection.count_documents({
            "course_name": course_name,
            "status": "active"
        })

    @staticmethod
    def get_enrolled_users(course_name):
        return list(enrollments_collection.find({
            "course_name": course_name,
            "status": "active"
        }))

    @staticmethod
    def deactivate_enrollment(course_name, username):
        return enrollments_collection.update_one(
            {
                "course_name": course_name,
                "username": username,
                "status": "active"
            },
            {
                "$set": {
                    "status": "inactive",
                    "left_at": datetime.utcnow()
                }
            }
        )

    @staticmethod
    def get_user_courses(username):
        enrollments = list(enrollments_collection.find({
            "username": username,
            "status": "active"
        }))
        course_names = [enrollment['course_name'] for enrollment in enrollments]
        return list(courses_collection.find({
            "course_name": {"$in": course_names},
            "is_active": True
        }))

class Chat:
    @staticmethod
    def add_message(course_name, username, message):
        chat = {
            "course_name": course_name,
            "username": username,
            "message": message,
            "timestamp": datetime.utcnow()
        }
        return chats_collection.insert_one(chat)

    @staticmethod
    def get_messages(course_name):
        return list(chats_collection.find({"course_name": course_name}).sort("timestamp", 1))
