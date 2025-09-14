from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token
from pymongo import MongoClient
from urllib.parse import quote_plus
import re
from datetime import datetime

# Blueprint
auth_bp = Blueprint("auth", __name__)

# MongoDB connection
username = quote_plus("user1")
password = quote_plus("nithin@12.A")
uri = f"mongodb+srv://{username}:{password}@prana-db.nthkhs7.mongodb.net/prana_db?retryWrites=true&w=majority"
client = MongoClient(uri)

db = client["prana_db"]
users_collection = db["users"]

# Email regex for validation
EMAIL_REGEX = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

def validate_email(email: str) -> bool:
    return re.match(EMAIL_REGEX, email) is not None

def validate_password(password: str) -> tuple[bool, str]:
    """
    Password must:
    - Be at least 8 characters
    - Contain uppercase, lowercase, number, special character
    """
    if len(password) < 8:
        return False, "Password must be at least 8 characters long"
    if not re.search(r"[A-Z]", password):
        return False, "Password must contain at least one uppercase letter"
    if not re.search(r"[a-z]", password):
        return False, "Password must contain at least one lowercase letter"
    if not re.search(r"[0-9]", password):
        return False, "Password must contain at least one number"
    if not re.search(r"[@$!%*?&]", password):
        return False, "Password must contain at least one special character (@$!%*?&)"
    return True, "Valid password"


# ---------------- REGISTER ----------------
@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    # Email validation
    if not email or not validate_email(email):
        return jsonify({"message": "Invalid email format"}), 400
    
    # Password validation
    is_valid, msg = validate_password(password)
    if not is_valid:
        return jsonify({"message": msg}), 400

    # Check if user already exists
    if users_collection.find_one({"email": email}):
        return jsonify({"message": "User already exists"}), 409

    # Store hashed password
    hashed_password = generate_password_hash(password)
    hashed_password = generate_password_hash(password)
    users_collection.insert_one({
        "email": email,
        "password": hashed_password,
        "is_premium": False,                 # ✅ Not premium initially
        "created_at": datetime.utcnow()      # ✅ Trial starts now
    })

    return jsonify({"message": "User registered successfully"}), 201


# ---------------- LOGIN ----------------
@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    # Find user
    user = users_collection.find_one({"email": email})
    if not user or not check_password_hash(user["password"], password):
        return jsonify({"message": "Invalid credentials"}), 401

    # Create JWT token
    token = create_access_token(identity=email)
    return jsonify({"access_token": token}), 200
