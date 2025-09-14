import tensorflow as tf
import numpy as np
import json
import logging
from backend.utils import calculate_angle
from backend.pose_feedback import (
    get_tree_pose_feedback,   
)

model = tf.keras.models.load_model("backend/yoga_pose_model.h5")

with open("backend/yoga_poses_classes.json") as f:
    class_names = json.load(f)

# Dispatch table for feedback functions
POSE_FEEDBACK_MAP = {
    "treepose": get_tree_pose_feedback,
}

def build_feature_vector(flat, landmarks):
    """Hybrid vector: landmarks + angles (same as in training)"""
    angles = []
    try:
        # Arms
        angles.append(calculate_angle(landmarks[11], landmarks[13], landmarks[15]))
        angles.append(calculate_angle(landmarks[12], landmarks[14], landmarks[16]))
        # Legs
        angles.append(calculate_angle(landmarks[23], landmarks[25], landmarks[27]))
        angles.append(calculate_angle(landmarks[24], landmarks[26], landmarks[28]))
        # Torso
        angles.append(calculate_angle(landmarks[11], landmarks[23], landmarks[25]))
        angles.append(calculate_angle(landmarks[12], landmarks[24], landmarks[26]))
    except Exception as e:
        logging.error(f"Error computing angles: {e}")
        return np.array(flat)  # fallback if landmarks missing
    
    return np.concatenate([flat, np.array(angles, dtype=np.float32)])


def predict_pose(flat, landmarks, selected_pose, first_time=False):
    """
    flat: flattened Mediapipe landmarks (132 values)
    landmarks: structured landmarks (for feedback)
    selected_pose: pose chosen by user in frontend
    first_time: whether to give intro guidance
    """

    # 🛠️ Debug: log landmark info
    if not landmarks:
        logging.warning("⚠️ No landmarks passed into predict_pose.")
    else:
        logging.info(f"Received {len(landmarks)} landmarks for feedback.")
        logging.debug(f"Nose coords: x={landmarks[0].x:.3f}, y={landmarks[0].y:.3f}")

    # ✅ Build hybrid feature vector (same as training)
    feature_vector = build_feature_vector(flat, landmarks)
    input_data = np.expand_dims(feature_vector, axis=0)

    # ✅ Model prediction
    predictions = model.predict(input_data, verbose=0)
    class_id = int(np.argmax(predictions))
    pose_class = class_names[str(class_id)]
    logging.info(f"Predicted pose: {pose_class} (prob={predictions[0][class_id]:.2f})")

    # ✅ Feedback based on structured landmarks
    feedback_fn = POSE_FEEDBACK_MAP.get(selected_pose.lower())
    if feedback_fn:
        feedback = feedback_fn(pose_class, landmarks, first_time=first_time)
    else:
        feedback = [f"No feedback logic for {selected_pose}."]

    return pose_class, feedback
