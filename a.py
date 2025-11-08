"""Real-time emotion detection using a pretrained FER2013 CNN model."""

import argparse
import os
import time

import cv2
import numpy as np
from tensorflow.keras.models import load_model

EMOTION_LABELS = [
    "Angry",
    "Disgust",
    "Fear",
    "Happy",
    "Neutral",
    "Sad",
    "Surprise",
]


def load_face_detector() -> cv2.CascadeClassifier:
    cascade_path = cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
    detector = cv2.CascadeClassifier(cascade_path)
    if detector.empty():
        raise RuntimeError("Unable to load Haar cascade from OpenCV data directory.")
    return detector


def preprocess_face(face: np.ndarray) -> np.ndarray:
    # FER2013 models typically expect grayscale, but yours needs RGB
    # Try direct RGB resize without grayscale conversion
    resized = cv2.resize(face, (48, 48))
    normalized = resized.astype("float32") / 255.0
    return np.expand_dims(normalized, axis=0)


def draw_prediction(
    frame: np.ndarray,
    box: tuple[int, int, int, int],
    label: str,
    confidence: float,
    color: tuple[int, int, int] = (0, 255, 0),
) -> None:
    x, y, w, h = box
    frame_h, frame_w = frame.shape[:2]

    cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)

    text = f"{label}: {confidence * 100:.1f}%"
    text_size, baseline = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 0.7, 2)
    text_x = max(0, min(x, frame_w - text_size[0]))
    default_text_y = y - 10
    if default_text_y > text_size[1]:
        text_y = default_text_y
    else:
        text_y = min(frame_h - baseline - 5, y + h + text_size[1] + 10)
    cv2.putText(frame, text, (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2, cv2.LINE_AA)

    bar_width = min(200, max(60, frame_w - text_x - 10))
    bar_height = 18
    bar_y = y + h + 8
    if bar_y + bar_height + baseline > frame_h:
        bar_y = max(10, y - bar_height - 12)

    start = (text_x, bar_y)
    end = (text_x + bar_width, bar_y + bar_height)
    cv2.rectangle(frame, start, end, (80, 80, 80), 1)
    filled = int(bar_width * np.clip(confidence, 0.0, 1.0))
    cv2.rectangle(frame, start, (text_x + filled, bar_y + bar_height), color, -1)


def run(model_path: str, confidence_threshold: float, camera_index: int) -> None:
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Model file not found: {model_path}")

    model = load_model(model_path)
    face_detector = load_face_detector()

    cap = cv2.VideoCapture(camera_index)
    if not cap.isOpened():
        raise RuntimeError("Unable to open webcam. Check camera permissions and index.")

    print("Press 'q' to quit, 's' to save the current frame.")
    frame_counter = 0
    fps = 0.0
    last_time = time.time()

    try:
        while True:
            success, frame = cap.read()
            if not success:
                print("Warning: Unable to read frame from webcam.")
                break

            frame = cv2.flip(frame, 1)
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = face_detector.detectMultiScale(
                gray,
                scaleFactor=1.2,
                minNeighbors=5,
                minSize=(80, 80)
            )

            for (x, y, w, h) in faces:
                face_roi = frame[y:y+h, x:x+w]
                try:
                    # Your FER2013 model prediction
                    face_input = preprocess_face(face_roi)
                    predictions = model.predict(face_input, verbose=0)[0]
                    index = int(np.argmax(predictions))
                    confidence = float(predictions[index])
                    label = EMOTION_LABELS[index]
                    
                    # Show all predictions to debug bias
                    debug_text = " | ".join([f"{EMOTION_LABELS[i]}: {predictions[i]*100:.0f}%" for i in range(len(EMOTION_LABELS))])
                    cv2.putText(frame, debug_text, (10, frame.shape[0] - 20), 
                               cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 1)
                    
                    color = (0, 255, 0) if confidence > 0.4 else (0, 255, 255)
                    draw_prediction(frame, (x, y, w, h), label, confidence, color=color)
                except Exception as err:
                    print(f"Error: {err}")

            frame_counter += 1
            if frame_counter >= 10:
                now = time.time()
                elapsed = now - last_time
                if elapsed > 0:
                    fps = frame_counter / elapsed
                frame_counter = 0
                last_time = now

            cv2.putText(frame, f"FPS: {fps:.1f}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            cv2.imshow("Emotion Detection", frame)

            key = cv2.waitKey(1) & 0xFF
            if key == ord("q"):
                break
            if key == ord("s"):
                filename = f"snapshot_{int(time.time())}.png"
                cv2.imwrite(filename, frame)
                print(f"Saved {filename}")
    finally:
        cap.release()
        cv2.destroyAllWindows()


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Real-time emotion detection from webcam feed.")
    parser.add_argument("--model", default="fer2013_emotion_cnn.h5", help="Path to the trained Keras model.")
    parser.add_argument(
        "--threshold",
        type=float,
        default=0.3,
        help="Minimum confidence considered reliable (still shows lower values with '(?)').",
    )
    parser.add_argument("--camera", type=int, default=0, help="Webcam index to use.")
    return parser.parse_args()


def main() -> None:
    args = parse_arguments()
    run(model_path=args.model, confidence_threshold=args.threshold, camera_index=args.camera)


if __name__ == "__main__":
    main()