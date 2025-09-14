import mediapipe as mp
import numpy as np
import cv2  # for preprocessing

# Initialize Mediapipe pose detector
mp_pose = mp.solutions.pose
pose = mp_pose.Pose(
    static_image_mode=True,
    model_complexity=2,              # higher accuracy
    min_detection_confidence=0.3,    # lower threshold for tough lighting
    min_tracking_confidence=0.3
)

def preprocess_frame(image_bgr):
    """Normalize brightness/contrast to help Mediapipe in variable lighting."""
    # Convert to YUV and equalize histogram of Y (luminance) channel
    yuv = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2YUV)
    yuv[:, :, 0] = cv2.equalizeHist(yuv[:, :, 0])
    normalized = cv2.cvtColor(yuv, cv2.COLOR_YUV2BGR)

    # Resize to consistent size (helps detection stability)
    normalized = cv2.resize(normalized, (640, 480))

    # Optional: auto brightness boost if frame is too dark
    mean_brightness = np.mean(normalized)
    if mean_brightness < 60:  # adjust threshold if needed
        factor = 120.0 / (mean_brightness + 1e-6)
        normalized = np.clip(normalized * factor, 0, 255).astype(np.uint8)

    return normalized

def extract_landmarks(image):
    """Extracts flattened + structured landmarks from an input BGR frame."""
    # Step 1: Preprocess for consistent lighting
    image_bgr = preprocess_frame(image)

    # Step 2: Convert to RGB for Mediapipe
    image_rgb = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2RGB)
    results = pose.process(image_rgb)

    # Step 3: Handle detection failure
    if not results.pose_landmarks:
        print("⚠️ No pose detected after preprocessing.")
        return None, None

    # Step 4: Extract landmarks
    landmarks = results.pose_landmarks.landmark
    flat_landmarks = []
    for lm in landmarks:
        flat_landmarks.extend([lm.x, lm.y, lm.z, lm.visibility])

    print(f"✅ Pose detected: {len(landmarks)} landmarks extracted.")
    print(f"   Nose (id=0) coords: x={landmarks[0].x:.3f}, y={landmarks[0].y:.3f}, vis={landmarks[0].visibility:.2f}")

    return np.array(flat_landmarks), landmarks
