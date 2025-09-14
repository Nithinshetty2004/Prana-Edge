# train.py
from dataset_processor import process_dataset
from model_trainer import train_yoga_model
import matplotlib.pyplot as plt
import json

if __name__ == "__main__":
    dataset_path = "yoga_poses_dataset"  # Replace with your actual dataset path
    
    print("Processing dataset and extracting landmarks...")
    X, y, pose_dict = process_dataset(dataset_path)
    
    if len(X) == 0:
        print("No valid data was extracted from the dataset. Please check your images.")
        exit(1)
    
    print(f"Dataset processed. Found {len(X)} samples across {len(pose_dict)} classes.")
    
    inverse_pose_dict = {v: k for k, v in pose_dict.items()}
    with open("yoga_poses_classes.json", "w") as f:
        json.dump(inverse_pose_dict, f)
    
    print("Training model...")
    model, history, _ = train_yoga_model(X, y, pose_dict)
    
    print("Training complete!")
    
    plt.figure(figsize=(12, 4))
    plt.subplot(1, 2, 1)
    plt.plot(history.history['accuracy'], label='Training accuracy')
    plt.plot(history.history['val_accuracy'], label='Validation accuracy')
    plt.title('Model accuracy')
    plt.xlabel('Epoch')
    plt.ylabel('Accuracy')
    plt.legend()
    
    plt.subplot(1, 2, 2)
    plt.plot(history.history['loss'], label='Training loss')
    plt.plot(history.history['val_loss'], label='Validation loss')
    plt.title('Model loss')
    plt.xlabel('Epoch')
    plt.ylabel('Loss')
    plt.legend()
    
    plt.tight_layout()
    plt.savefig('training_history.png')
    plt.show()