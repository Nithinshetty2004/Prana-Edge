from .models import Course, Enrollment, Chat

class CourseService:
    @staticmethod
    def create_course(course_data, created_by):
        if not course_data.get('course_name'):
            return {"error": "Course name is required"}, 400
        if Course.exists(course_data['course_name']):
            return {"error": "Course with this name already exists"}, 400
        result = Course.create(course_data, created_by)
        return {
            "message": "Course created successfully",
            "course_id": str(result.inserted_id)
        }, 201

    @staticmethod
    def get_all_courses():
        courses = Course.find_all_active()
        for course in courses:
            course['_id'] = str(course['_id'])
            course['created_at'] = course['created_at'].isoformat()
        return {"courses": courses}, 200

    @staticmethod
    def get_course_by_name(course_name):
        course = Course.find_by_name(course_name)
        if not course:
            return {"error": "Course not found"}, 404
        course['_id'] = str(course['_id'])
        course['created_at'] = course['created_at'].isoformat()
        return {"course": course}, 200

    @staticmethod
    def delete_course(course_name):
        result = Course.delete(course_name)
        if result.matched_count == 0:
            return {"error": "Course not found or already deleted"}, 404
        return {"message": "Course deleted successfully"}, 200

class EnrollmentService:
    @staticmethod
    def join_course(course_name, username):
        course = Course.find_by_name(course_name)
        if not course:
            return {"error": "Course not found"}, 404
        existing_enrollment = Enrollment.find_user_enrollment(course_name, username)
        if existing_enrollment and existing_enrollment.get('status') == 'active':
            return {"error": "Already enrolled in this course"}, 400
        current_enrollments = Enrollment.count_active_enrollments(course_name)
        if course.get('max_participants') and current_enrollments >= course['max_participants']:
            return {"error": "Course is full"}, 400
        Enrollment.create(course_name, username)
        return {"message": "Successfully enrolled in course"}, 200

    @staticmethod
    def get_course_enrollments(course_name):
        course = Course.find_by_name(course_name)
        if not course:
            return {"error": "Course not found"}, 404
        enrollments = Enrollment.get_enrolled_users(course_name)
        usernames = [enrollment['username'] for enrollment in enrollments]
        return {
            "course_name": course_name,
            "enrolled_users": usernames,
            "total_enrollments": len(usernames)
        }, 200

    @staticmethod
    def leave_course(course_name, username):
        result = Enrollment.deactivate_enrollment(course_name, username)
        if result.matched_count == 0:
            return {"error": "Enrollment not found"}, 404
        return {"message": "Successfully left the course"}, 200

    @staticmethod
    def get_user_courses(username):
        courses = Enrollment.get_user_courses(username)
        for course in courses:
            course['_id'] = str(course['_id'])
            course['created_at'] = course['created_at'].isoformat()
        return {
            "username": username,
            "enrolled_courses": courses
        }, 200

class ChatService:
    @staticmethod
    def add_message(course_name, username, message):
        course = Course.find_by_name(course_name)
        if not course:
            return {"error": "Course not found"}, 404
        if not message:
            return {"error": "Message cannot be empty"}, 400
        result = Chat.add_message(course_name, username, message)
        return {
            "message": "Message added successfully",
            "chat_id": str(result.inserted_id)
        }, 201

    @staticmethod
    def get_messages(course_name):
        course = Course.find_by_name(course_name)
        if not course:
            return {"error": "Course not found"}, 404
        messages = Chat.get_messages(course_name)
        formatted = [
            {
                "username": msg["username"],
                "message": msg["message"],
                "timestamp": msg["timestamp"].isoformat()
            }
            for msg in messages
        ]
        return {"course_name": course_name, "messages": formatted}, 200
