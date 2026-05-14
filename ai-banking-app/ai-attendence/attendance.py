import cv2
import pandas as pd
from datetime import datetime
from database import Database
from face_engine import FaceEngine

class AttendanceSystem:

    def __init__(self):

        self.db = Database()

        self.engine = FaceEngine()

        self.marked = set()

    def mark_attendance(self, name):

        if name in self.marked:
            return

        now = datetime.now()

        date = now.strftime("%Y-%m-%d")
        time = now.strftime("%H:%M:%S")

        self.db.insert_attendance(name, date, time)

        attendance_data = {
            "Name": [name],
            "Date": [date],
            "Time": [time]
        }

        df = pd.DataFrame(attendance_data)

        try:
            old = pd.read_csv("attendance.csv")
            df = pd.concat([old, df], ignore_index=True)

        except:
            pass

        df.to_csv("attendance.csv", index=False)

        self.marked.add(name)

        print(f"{name} attendance marked")

    def run(self):

        cap = cv2.VideoCapture(0)

        while True:

            ret, frame = cap.read()

            if not ret:
                break

            results = self.engine.recognize(frame)

            for name, (top, right, bottom, left) in results:

                color = (0, 255, 0)

                if name == "Unknown":
                    color = (0, 0, 255)

                cv2.rectangle(
                    frame,
                    (left, top),
                    (right, bottom),
                    color,
                    2
                )

                cv2.putText(
                    frame,
                    name,
                    (left, top - 10),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.8,
                    color,
                    2
                )

                if name != "Unknown":
                    self.mark_attendance(name)

            cv2.imshow("AI Attendance System", frame)

            key = cv2.waitKey(1)

            if key == ord("q"):
                break

        cap.release()
        cv2.destroyAllWindows()
        self.db.close()