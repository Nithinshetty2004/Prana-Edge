import logging
import random
from backend.utils import calculate_angle

def get_tree_pose_feedback(pose_class, landmarks, first_time=False):
    """
    pose_class: predicted class from model
    landmarks: Mediapipe landmarks
    first_time: True for intro guidance, then False for live corrections
    """
    
    # 🎙️ Intro guidance
    if first_time:
        logging.info("Giving Tree Pose introduction")
        return [
            "Stand tall with feet together.",
            "Lift one foot and place it on the inner thigh of your opposite leg.",
            "Raise your arms overhead and bring your palms together in prayer position.",
            "Keep your body straight and balanced."
        ]

    # 🧠 If pose not detected
    if pose_class.lower() != "tree_pose":   # ✅ fixed class name
        logging.warning(f"Pose mismatch: expected treepose, got {pose_class}")
        return ["Please move into the tree pose."]

    feedback = []

    # ✅ Hands in prayer position (wrists close together)
    left_wrist = landmarks[15]
    right_wrist = landmarks[16]
    wrist_dist = abs(left_wrist.x - right_wrist.x) + abs(left_wrist.y - right_wrist.y)
    if wrist_dist > 0.08:  # relaxed tolerance
        feedback.append("Bring your palms together in prayer position.")

    # ✅ Arms raised straight above head
    left_arm_angle = calculate_angle(landmarks[11], landmarks[13], landmarks[15])
    right_arm_angle = calculate_angle(landmarks[12], landmarks[14], landmarks[16])
    nose_y = landmarks[0].y
    if (left_wrist.y > nose_y or right_wrist.y > nose_y or
        left_arm_angle < 150 or right_arm_angle < 150):
        feedback.append("Raise your arms straight above your head.")

    # ✅ Supporting leg straight
    left_leg_angle = calculate_angle(landmarks[23], landmarks[25], landmarks[27])
    right_leg_angle = calculate_angle(landmarks[24], landmarks[26], landmarks[28])
    if min(left_leg_angle, right_leg_angle) < 160:
        feedback.append("Keep your standing leg straight.")

    # ✅ Lifted leg check (one foot above ankle level)
    left_ankle_y = landmarks[27].y
    right_ankle_y = landmarks[28].y
    if abs(left_ankle_y - right_ankle_y) < 0.07:  # both feet too close in height
        feedback.append("Lift one foot and place it on your thigh.")

    # ✅ Hip balance
    left_hip_y = landmarks[23].y
    right_hip_y = landmarks[24].y
    if abs(left_hip_y - right_hip_y) > 0.12:  # small relaxation
        feedback.append("Balance your hips and keep them level.")

    # ✅ Spine upright (nose aligned with hips)
    nose_x = landmarks[0].x
    mid_hip_x = (landmarks[23].x + landmarks[24].x) / 2
    if abs(nose_x - mid_hip_x) > 0.1:
        feedback.append("Keep your body upright and avoid leaning sideways.")

    # ✅ If no corrections → encouragement
    if not feedback:
        positive_feedback = [
            "Nice work, you are steady in tree pose.",
            "Great balance, hold your pose.",
            "Perfect alignment, keep breathing calmly."
        ]
        feedback.append(random.choice(positive_feedback))

    logging.info(f"Tree Pose feedback: {feedback}")
    return feedback
