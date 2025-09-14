# utils.py
import os
import cv2
import numpy as np
import mediapipe as mp
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout
from tensorflow.keras.utils import to_categorical

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

def extract_landmarks(image):
    with mp_pose.Pose(static_image_mode=True, min_detection_confidence=0.5) as pose:
        results = pose.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
        
        if not results.pose_landmarks:
            return None, None
        
        landmarks = results.pose_landmarks.landmark
        flat = []
        for lm in landmarks:
            flat.extend([lm.x, lm.y, lm.z, lm.visibility])
        
        return np.array(flat), landmarks  # return flat + structured


def calculate_angle(a, b, c):
    """
    Calculates the angle between three Mediapipe landmarks.
    b = vertex point
    Returns angle in degrees.
    """
    a = np.array([a.x, a.y])
    b = np.array([b.x, b.y])
    c = np.array([c.x, c.y])

    ba = a - b
    bc = c - b

    cosine_angle = np.dot(ba, bc) / (np.linalg.norm(ba) * np.linalg.norm(bc) + 1e-6)
    angle = np.degrees(np.arccos(np.clip(cosine_angle, -1.0, 1.0)))
    return angle
