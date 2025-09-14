from flask import Flask, request, jsonify
from flask_cors import CORS
import cv2
import numpy as np
import base64
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity
from live_class import live_class_bp
from datetime import datetime, timedelta

# Authentication routes
from user_interface.auth_routes import auth_bp

# Pose modules
from backend.predictor import predict_pose
from backend.pose_estimator import extract_landmarks

# Nutrition module
from nutrition_guide.nutrition_engine import NutritionEngine

# Health analyzers
from diet_sleep_tracker.diet_analyzer import analyze_diet
from diet_sleep_tracker.sleep_analyzer import analyze_sleep

# Import users_collection from your database module
from user_interface.auth_routes import users_collection  # Make sure this path is correct

app = Flask(__name__)
CORS(app)

# 🔑 Secret for signing JWT (use environment variable in production)
app.config["JWT_SECRET_KEY"] = "super-secret-key"
jwt = JWTManager(app)

# Register login/register blueprint
app.register_blueprint(auth_bp)

# Register live class blueprint
app.register_blueprint(live_class_bp)

nutrition_engine = NutritionEngine()


# ===== YOGA POSE PREDICTION ENDPOINT =====
@app.route("/predict_frame", methods=["POST"])
@jwt_required()   # 🔒 Protect this route
def predict_frame():
    current_user = get_jwt_identity()
    user = users_collection.find_one({"email": current_user})

    if not user:
        return jsonify({"error": "User not found"}), 404

    # ✅ Check if user is premium or still in free trial
    if not user.get("is_premium", False):
        created_at = user.get("created_at")
        if not created_at:
            return jsonify({"error": "User trial info missing"}), 403

        # Convert created_at to datetime if needed
        if isinstance(created_at, str):
            created_at = datetime.fromisoformat(created_at)

        if datetime.utcnow() > created_at + timedelta(days=1):
            # ❌ Trial expired
            return jsonify({
                "error": "Trial expired. Please upgrade to premium.",
                "payment_url": "https://rzp.io/rzp/8jKeOewG"  # 🔗 Placeholder
            }), 403

    # ✅ Process pose prediction
    data = request.get_json()
    if not data or 'image' not in data or 'pose_name' not in data:
        return jsonify({"error": "Image and pose_name are required"}), 400

    pose_name = data['pose_name']

    try:
        image_data = base64.b64decode(data['image'].split(',')[1])
        npimg = np.frombuffer(image_data, np.uint8)
        image = cv2.imdecode(npimg, cv2.IMREAD_COLOR)
    except Exception as e:
        return jsonify({"error": f"Failed to decode image: {str(e)}"}), 500

    landmarks_flat, landmarks_struct = extract_landmarks(image)
    if landmarks_flat is None:
        return jsonify({"pose": "no_pose_detected", "feedback": ["No human pose detected."]})

    pose_class, feedback = predict_pose(landmarks_flat, landmarks_struct, pose_name)

    return jsonify({
        "user": current_user,
        "pose": pose_class,
        "feedback": feedback
    })

# ===== NUTRITION RECOMMENDATION ENDPOINT =====
@app.route('/api/nutrition_recommendation', methods=['POST'])
@jwt_required()
def get_nutrition_recommendation():
    current_user = get_jwt_identity()  # ✅ Who is asking

    data = request.json
    required_fields = ['height', 'weight', 'age', 'gender', 'activity_level']
    missing_fields = [field for field in required_fields if not data.get(field)]

    if missing_fields:
        return jsonify({'error': f'Missing required fields: {", ".join(missing_fields)}'}), 400

    try:
        height = float(data['height'])
        weight = float(data['weight'])
        age = int(data['age'])
        gender = data['gender']
        activity_level = data['activity_level']
        diseases = data.get('diseases', [])

        recommendations = nutrition_engine.get_recommendations(
            height=height,
            weight=weight,
            age=age,
            gender=gender,
            activity_level=activity_level,
            diseases=diseases
        )
        return jsonify({
            "user": current_user,
            "recommendations": recommendations
        })

    except ValueError as ve:
        return jsonify({'error': f'Invalid data format: {str(ve)}'}), 400


# ===== HEALTH STATUS ENDPOINT =====
@app.route('/api/health_status', methods=['POST'])
@jwt_required()
def get_health_status():
    current_user = get_jwt_identity()

    data = request.json
    required_fields = ['height', 'weight', 'age', 'gender']
    missing_fields = [field for field in required_fields if not data.get(field)]

    if missing_fields:
        return jsonify({'error': f'Missing required fields: {", ".join(missing_fields)}'}), 400

    try:
        height = float(data['height'])
        weight = float(data['weight'])
        age = int(data['age'])
        gender = data['gender']
        diseases = data.get('diseases', [])

        health_info = nutrition_engine.calculate_health_metrics(height, weight)
        return jsonify({
            "user": current_user,
            "health_info": health_info
        })

    except ValueError as ve:
        return jsonify({'error': f'Invalid data format: {str(ve)}'}), 400


# ===== DIET TRACKING ENDPOINT =====
@app.route('/track_diet', methods=['POST'])
@jwt_required()
def track_diet():
    current_user = get_jwt_identity()

    data = request.json
    try:
        meals = data.get('meals', [])
        water_intake = data.get('water_intake', 0)
        calories = data.get('calories', 0)
        protein = data.get('protein', 0)
        carbs = data.get('carbs', 0)
        fats = data.get('fats', 0)

        analysis = analyze_diet(meals, water_intake, calories, protein, carbs, fats)
        return jsonify({
            "user": current_user,
            "analysis": analysis
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 400


# ===== SLEEP TRACKING ENDPOINT =====
@app.route('/track_sleep', methods=['POST'])
@jwt_required()
def track_sleep():
    current_user = get_jwt_identity()

    data = request.json
    try:
        hours = data.get('hours', 0)
        quality = data.get('quality', 0)
        sleep_time = data.get('sleep_time', '')
        wake_time = data.get('wake_time', '')
        interruptions = data.get('interruptions', 0)

        analysis = analyze_sleep(hours, quality, sleep_time, wake_time, interruptions)
        return jsonify({
            "user": current_user,
            "analysis": analysis
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.before_request
def log_headers():
    print("HEADERS:", dict(request.headers))

if __name__ == "__main__":
    app.run(debug=True)
