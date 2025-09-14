from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from .services import CourseService, EnrollmentService, ChatService

live_class_bp = Blueprint('live_class', __name__)

@live_class_bp.route('/courses', methods=['POST'])
@jwt_required()
def create_course():
    current_user = get_jwt_identity()
    data = request.get_json()
    response, status_code = CourseService.create_course(data, current_user)
    return jsonify(response), status_code

@live_class_bp.route('/courses', methods=['GET'])
@jwt_required()
def get_all_courses():
    response, status_code = CourseService.get_all_courses()
    return jsonify(response), status_code

@live_class_bp.route('/courses/<course_name>', methods=['GET'])
@jwt_required()
def get_course_by_name(course_name):
    response, status_code = CourseService.get_course_by_name(course_name)
    return jsonify(response), status_code

@live_class_bp.route('/courses/<course_name>', methods=['DELETE'])
@jwt_required()
def delete_course(course_name):
    response, status_code = CourseService.delete_course(course_name)
    return jsonify(response), status_code

@live_class_bp.route('/courses/<course_name>/join', methods=['POST'])
@jwt_required()
def join_course(course_name):
    current_user = get_jwt_identity()
    response, status_code = EnrollmentService.join_course(course_name, current_user)
    return jsonify(response), status_code

@live_class_bp.route('/courses/<course_name>/enrollments', methods=['GET'])
@jwt_required()
def get_course_enrollments(course_name):
    response, status_code = EnrollmentService.get_course_enrollments(course_name)
    return jsonify(response), status_code

@live_class_bp.route('/courses/<course_name>/leave', methods=['DELETE'])
@jwt_required()
def leave_course(course_name):
    current_user = get_jwt_identity()
    response, status_code = EnrollmentService.leave_course(course_name, current_user)
    return jsonify(response), status_code

@live_class_bp.route('/my-courses', methods=['GET'])
@jwt_required()
def get_my_courses():
    current_user = get_jwt_identity()
    response, status_code = EnrollmentService.get_user_courses(current_user)
    return jsonify(response), status_code

@live_class_bp.route('/courses/<course_name>/chat', methods=['POST'])
@jwt_required()
def add_chat_message(course_name):
    current_user = get_jwt_identity()
    data = request.get_json()
    message = data.get("message")
    response, status_code = ChatService.add_message(course_name, current_user, message)
    return jsonify(response), status_code

@live_class_bp.route('/courses/<course_name>/chat', methods=['GET'])
@jwt_required()
def get_chat_messages(course_name):
    response, status_code = ChatService.get_messages(course_name)
    return jsonify(response), status_code
