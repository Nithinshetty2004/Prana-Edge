from utils import extract_landmarks, calculate_angle
import os
import cv2
import numpy as np

def process_dataset(dataset_path):
    X, y = [], []
    
    pose_types = os.listdir(dataset_path)
    pose_dict = {pose_type: idx for idx, pose_type in enumerate(pose_types)}
    
    for pose_type in pose_types:
        pose_path = os.path.join(dataset_path, pose_type)
        if not os.path.isdir(pose_path):
            continue

        for file_name in os.listdir(pose_path):
            file_path = os.path.join(pose_path, file_name)

            # ---- Images ----
            if file_path.lower().endswith(('.png', '.jpg', '.jpeg')):
                img = cv2.imread(file_path)
                if img is None:
                    continue
                flat, landmarks = extract_landmarks(img)
                if flat is not None:
                    feature_vector = build_feature_vector(flat, landmarks)
                    X.append(feature_vector)
                    y.append(pose_dict[pose_type])

            # ---- Videos ----
            elif file_path.lower().endswith(('.mp4', '.avi', '.mov')):
                cap = cv2.VideoCapture(file_path)
                frame_count = 0
                while cap.isOpened():
                    ret, frame = cap.read()
                    if not ret:
                        break
                    frame_count += 1
                    if frame_count % 5 != 0:  # sample every 5th frame
                        continue
                    flat, landmarks = extract_landmarks(frame)
                    if flat is not None:
                        feature_vector = build_feature_vector(flat, landmarks)
                        X.append(feature_vector)
                        y.append(pose_dict[pose_type])
                cap.release()

    # ✅ Ensure uniform shape
    X = np.array(X, dtype=np.float32)
    y = np.array(y)
    return X, y, pose_dict


def build_feature_vector(flat, landmarks):
    """Combine raw landmarks + selected joint angles into one vector"""
    angles = []
    # Arms
    angles.append(calculate_angle(landmarks[11], landmarks[13], landmarks[15]))  # left arm
    angles.append(calculate_angle(landmarks[12], landmarks[14], landmarks[16]))  # right arm
    # Legs
    angles.append(calculate_angle(landmarks[23], landmarks[25], landmarks[27]))  # left leg
    angles.append(calculate_angle(landmarks[24], landmarks[26], landmarks[28]))  # right leg
    # Torso
    angles.append(calculate_angle(landmarks[11], landmarks[23], landmarks[25]))  # left hip
    angles.append(calculate_angle(landmarks[12], landmarks[24], landmarks[26]))  # right hip

    # ✅ Flatten into hybrid vector
    return np.concatenate([flat, np.array(angles, dtype=np.float32)])
