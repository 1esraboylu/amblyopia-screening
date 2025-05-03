import tkinter as tk
from tkinter import simpledialog
import cv2
import math
import csv
from datetime import datetime
from threading import Thread

# Load Haar cascades
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_eye.xml")

# Global variables
running = False
asymmetry_detected = False
user_name = ""

def calc_distance(p1, p2):
    return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

def run_test():
    global running, asymmetry_detected, user_name
    asymmetry_counter = 0
    asymmetry_threshold = 15
    consecutive_limit = 5
    asymmetry_detected = False

    cap = cv2.VideoCapture(0)

    while running and cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        persistent_asymmetry = False

        for (x, y, w, h) in faces:
            roi_gray = gray[y:y + h, x:x + w]
            roi_color = frame[y:y + h, x:x + w]
            eyes = eye_cascade.detectMultiScale(roi_gray)
            eye_centers = []

            for (ex, ey, ew, eh) in eyes:
                center_x = ex + ew // 2
                center_y = ey + eh // 2
                eye_centers.append((center_x, center_y))
                cv2.rectangle(roi_color, (ex, ey), (ex + ew, ey + eh), (0, 255, 0), 2)

            if len(eye_centers) == 2:
                vertical_diff = abs(eye_centers[0][1] - eye_centers[1][1])
                horizontal_diff = abs(eye_centers[0][0] - eye_centers[1][0])

                cv2.putText(frame, f"V diff: {vertical_diff}px | H diff: {horizontal_diff}px", (10, 30),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 0), 2)

                if vertical_diff > asymmetry_threshold and horizontal_diff > 40:
                    cv2.putText(frame, "Please look straight at the camera", (10, 60),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 165, 255), 2)
                    asymmetry_counter = 0
                elif vertical_diff > asymmetry_threshold:
                    asymmetry_counter += 1
                else:
                    asymmetry_counter = 0

                if asymmetry_counter >= consecutive_limit:
                    persistent_asymmetry = True
                    asymmetry_detected = True
                    cv2.putText(frame, "⚠️ Persistent asymmetry detected!", (10, 90),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

        cv2.imshow("Amblyopia Screening", frame)
        if cv2.waitKey(1) & 0xFF == 27:
            break

    cap.release()
    cv2.destroyAllWindows()

    # Save result to CSV
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("test_results.csv", mode="a", newline="") as result_file:
        writer = csv.writer(result_file)
        writer.writerow([timestamp, user_name, "Yes" if asymmetry_detected else "No"])

def start_test():
    global running, user_name
    user_name = simpledialog.askstring("User Name", "Enter your name:")
    if not user_name:
        return
    running = True
    Thread(target=run_test).start()

def stop_test():
    global running
    running = False
    result_label.config(
        text="Test Result: " + ("⚠️ Persistent Asymmetry Detected" if asymmetry_detected else "✅ Looks Normal")
    )

# GUI Setup
window = tk.Tk()
window.title("Amblyopia Screening App")
window.geometry("300x250")

start_button = tk.Button(window, text="Start Test", command=start_test, width=20, height=2, bg="green", fg="white")
start_button.pack(pady=15)

stop_button = tk.Button(window, text="Finish Test", command=stop_test, width=20, height=2, bg="red", fg="white")
stop_button.pack(pady=15)

result_label = tk.Label(window, text="", font=("Arial", 14))
result_label.pack(pady=15)

window.mainloop()
