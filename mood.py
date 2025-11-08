# mood_detector_gui.py
"""
Simple Mood Detector GUI using webcam + pre-trained FER model.
Requirements: opencv-python, fer, Pillow, numpy
Run: python mood_detector_gui.py
"""

import cv2
import threading
import time
import numpy as np
from deepface import DeepFace
result = DeepFace.analyze(frame, actions=['emotion'])
from PIL import Image, ImageTk
import tkinter as tk
from tkinter import messagebox

class MoodDetectorApp:
    def __init__(self, window, window_title, camera_index=0):
        self.window = window
        self.window.title(window_title)
        self.camera_index = camera_index

        # Detector (pre-trained)
        self.detector = FER(mtcnn=True)  # mtcnn=True improves face detection accuracy

        # Video capture and control
        self.cap = None
        self.running = False
        self.frame = None

        # GUI elements
        self.video_label = tk.Label(window)
        self.video_label.pack()

        control_frame = tk.Frame(window)
        control_frame.pack(pady=6)

        self.start_btn = tk.Button(control_frame, text="Start Camera", width=15, command=self.start_camera)
        self.start_btn.grid(row=0, column=0, padx=5)

        self.stop_btn = tk.Button(control_frame, text="Stop Camera", width=15, command=self.stop_camera, state=tk.DISABLED)
        self.stop_btn.grid(row=0, column=1, padx=5)

        self.snap_btn = tk.Button(control_frame, text="Snapshot", width=15, command=self.snapshot, state=tk.DISABLED)
        self.snap_btn.grid(row=0, column=2, padx=5)

        # status label
        self.status_label = tk.Label(window, text="Status: Idle", fg="blue")
        self.status_label.pack(pady=4)

        # close handling
        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)

    def start_camera(self):
        if self.running:
            return
        try:
            self.cap = cv2.VideoCapture(self.camera_index)
            if not self.cap.isOpened():
                messagebox.showerror("Error", "Cannot open webcam. Check camera index or permissions.")
                return
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open camera: {e}")
            return

        self.running = True
        self.start_btn.config(state=tk.DISABLED)
        self.stop_btn.config(state=tk.NORMAL)
        self.snap_btn.config(state=tk.NORMAL)
        self.status_label.config(text="Status: Running", fg="green")

        # start thread for video capture & detection
        self.thread = threading.Thread(target=self.video_loop, daemon=True)
        self.thread.start()

    def stop_camera(self):
        if not self.running:
            return
        self.running = False
        # allow thread to stop
        time.sleep(0.2)
        if self.cap:
            self.cap.release()
            self.cap = None
        self.start_btn.config(state=tk.NORMAL)
        self.stop_btn.config(state=tk.DISABLED)
        self.snap_btn.config(state=tk.DISABLED)
        self.status_label.config(text="Status: Stopped", fg="orange")
        # clear image
        self.video_label.config(image='')

    def snapshot(self):
        if self.frame is None:
            return
        # save current frame as PNG
        filename = f"snapshot_{int(time.time())}.png"
        cv2.imwrite(filename, cv2.cvtColor(self.frame, cv2.COLOR_RGB2BGR))
        messagebox.showinfo("Snapshot", f"Saved to {filename}")

    def video_loop(self):
        # loop reading frames and running fer detection
        while self.running and self.cap and self.cap.isOpened():
            ret, frame = self.cap.read()
            if not ret:
                break

            # Resize for speed (optional)
            frame = cv2.resize(frame, (640, 480))

            # FER expects RGB images (not BGR)
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # Detect emotions (returns list of dicts)
            try:
                faces = self.detector.detect_emotions(rgb_frame)
            except Exception as e:
                # in rare cases detector may throw; skip frame
                faces = []

            # Draw bounding boxes and labels
            for face in faces:
                (x, y, w, h) = face["box"]
                # correct negative or out-of-bounds boxes
                x, y = max(0, x), max(0, y)
                w, h = max(0, w), max(0, h)
                # find highest-scoring emotion
                emotions = face["emotions"]
                if emotions:
                    emotion, score = max(emotions.items(), key=lambda item: item[1])
                    label = f"{emotion} {score:.2f}"
                else:
                    label = "Unknown"

                # draw rectangle + label on RGB frame (we will convert to ImageTk later)
                cv2.rectangle(rgb_frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
                cv2.putText(rgb_frame, label, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

            # keep the latest frame for snapshot, convert to PIL for Tkinter
            self.frame = rgb_frame.copy()
            img = Image.fromarray(rgb_frame)
            imgtk = ImageTk.PhotoImage(image=img)

            # update GUI image (must keep reference to avoid GC)
            self.video_label.imgtk = imgtk
            self.video_label.configure(image=imgtk)

            # small delay
            time.sleep(0.03)

        # cleanup when loop ends
        if self.cap:
            self.cap.release()

    def on_closing(self):
        # stop camera gracefully
        self.running = False
        time.sleep(0.2)
        try:
            if self.cap:
                self.cap.release()
        except:
            pass
        self.window.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = MoodDetectorApp(root, "AI Mood Detector (Camera + FER)")
    root.mainloop()
