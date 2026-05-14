import face_recognition
import os
import cv2
import numpy as np

class FaceEngine:

    def __init__(self, students_path="students"):
        self.students_path = students_path
        self.known_encodings = []
        self.known_names = []

        self.load_students()

    def load_students(self):

        for file in os.listdir(self.students_path):

            path = os.path.join(self.students_path, file)

            image = face_recognition.load_image_file(path)

            encodings = face_recognition.face_encodings(image)

            if len(encodings) > 0:

                encoding = encodings[0]

                self.known_encodings.append(encoding)

                name = os.path.splitext(file)[0]
                self.known_names.append(name)

    def recognize(self, frame):

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        locations = face_recognition.face_locations(rgb)
        encodings = face_recognition.face_encodings(rgb, locations)

        results = []

        for face_encoding, face_location in zip(encodings, locations):

            matches = face_recognition.compare_faces(
                self.known_encodings,
                face_encoding
            )

            face_distances = face_recognition.face_distance(
                self.known_encodings,
                face_encoding
            )

            best_match = np.argmin(face_distances)

            name = "Unknown"

            if matches[best_match]:
                name = self.known_names[best_match]

            results.append((name, face_location))

        return results