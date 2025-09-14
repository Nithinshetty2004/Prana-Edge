# model_trainer.py
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout
from tensorflow.keras.utils import to_categorical
from sklearn.model_selection import train_test_split

def create_model(input_shape, num_classes):
    model = Sequential([
        Dense(128, input_shape=(input_shape,), activation='relu'),
        Dropout(0.2),
        Dense(64, activation='relu'),
        Dropout(0.2),
        Dense(num_classes, activation='softmax')
    ])
    
    model.compile(
        optimizer='adam',
        loss='categorical_crossentropy',
        metrics=['accuracy']
    )
    
    return model

def train_yoga_model(X, y, pose_dict, test_size=0.2, epochs=50, batch_size=32):
    num_classes = len(pose_dict)
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=42)
    
    y_train_categorical = to_categorical(y_train, num_classes=num_classes)
    y_test_categorical = to_categorical(y_test, num_classes=num_classes)
    
    model = create_model(X_train.shape[1], num_classes)
    
    history = model.fit(
        X_train, y_train_categorical,
        validation_data=(X_test, y_test_categorical),
        epochs=epochs,
        batch_size=batch_size,
        verbose=1
    )
    
    test_loss, test_acc = model.evaluate(X_test, y_test_categorical)
    print(f"Test accuracy: {test_acc:.4f}")
    
    model.save("yoga_pose_model.h5")
    print("Model saved as yoga_pose_model.h5")
    
    return model, history, pose_dict