# import cv2
# import numpy as np
# from ultralytics import YOLO
# from collections import OrderedDict
# import math

# # -----------------------------
# # Simple Centroid Tracker
# # -----------------------------
# class CentroidTracker:
#     def __init__(self, max_disappeared=40):
#         self.next_object_id = 0
#         self.objects = OrderedDict()
#         self.disappeared = OrderedDict()
#         self.max_disappeared = max_disappeared

#     def register(self, centroid):
#         self.objects[self.next_object_id] = centroid
#         self.disappeared[self.next_object_id] = 0
#         self.next_object_id += 1

#     def deregister(self, object_id):
#         del self.objects[object_id]
#         del self.disappeared[object_id]

#     def update(self, rects):
#         if len(rects) == 0:
#             for object_id in list(self.disappeared.keys()):
#                 self.disappeared[object_id] += 1
#                 if self.disappeared[object_id] > self.max_disappeared:
#                     self.deregister(object_id)
#             return self.objects

#         input_centroids = np.zeros((len(rects), 2), dtype="int")

#         for (i, (startX, startY, endX, endY)) in enumerate(rects):
#             cX = int((startX + endX) / 2.0)
#             cY = int((startY + endY) / 2.0)
#             input_centroids[i] = (cX, cY)

#         if len(self.objects) == 0:
#             for i in range(len(input_centroids)):
#                 self.register(input_centroids[i])
#         else:
#             object_ids = list(self.objects.keys())
#             object_centroids = list(self.objects.values())

#             D = np.linalg.norm(np.array(object_centroids)[:, np.newaxis] - input_centroids, axis=2)

#             rows = D.min(axis=1).argsort()
#             cols = D.argmin(axis=1)[rows]

#             used_rows = set()
#             used_cols = set()

#             for (row, col) in zip(rows, cols):
#                 if row in used_rows or col in used_cols:
#                     continue

#                 object_id = object_ids[row]
#                 self.objects[object_id] = input_centroids[col]
#                 self.disappeared[object_id] = 0

#                 used_rows.add(row)
#                 used_cols.add(col)

#             unused_rows = set(range(0, D.shape[0])).difference(used_rows)
#             unused_cols = set(range(0, len(input_centroids))).difference(used_cols)

#             if D.shape[0] >= len(input_centroids):
#                 for row in unused_rows:
#                     object_id = object_ids[row]
#                     self.disappeared[object_id] += 1
#                     if self.disappeared[object_id] > self.max_disappeared:
#                         self.deregister(object_id)
#             else:
#                 for col in unused_cols:
#                     self.register(input_centroids[col])

#         return self.objects


# # -----------------------------
# # Load YOLO Model
# # -----------------------------
# model = YOLO("yolov8n.pt")  # downloads automatically

# # Vehicle class IDs in COCO dataset
# VEHICLE_CLASSES = [2, 3, 5, 7]  # car, motorcycle, bus, truck

# # -----------------------------
# # Video Source
# # -----------------------------
# video_path = "video.mp4"  # Change to 0 for webcam
# cap = cv2.VideoCapture(video_path)

# tracker = CentroidTracker()

# # -----------------------------
# # Main Loop
# # -----------------------------
# while True:
#     ret, frame = cap.read()
#     if not ret:
#         break

#     results = model(frame)[0]

#     rects = []

#     for box in results.boxes:
#         cls_id = int(box.cls[0])
#         if cls_id in VEHICLE_CLASSES:
#             x1, y1, x2, y2 = map(int, box.xyxy[0])
#             rects.append((x1, y1, x2, y2))

#             cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

#     objects = tracker.update(rects)

#     for (object_id, centroid) in objects.items():
#         text = f"ID {object_id}"
#         cv2.putText(frame, text, (centroid[0] - 10, centroid[1] - 10),
#                     cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
#         cv2.circle(frame, (centroid[0], centroid[1]), 4, (0, 0, 255), -1)

#     cv2.imshow("Vehicle Tracking", frame)

#     if cv2.waitKey(1) & 0xFF == ord("q"):
#         break

# cap.release()
# cv2.destroyAllWindows()






import cv2
import numpy as np
from ultralytics import YOLO
from collections import OrderedDict

# -----------------------------
# Simple Centroid Tracker
# -----------------------------
class CentroidTracker:
    def __init__(self, max_disappeared=40):
        self.next_object_id = 0
        self.objects = OrderedDict()
        self.disappeared = OrderedDict()
        self.max_disappeared = max_disappeared

    def register(self, centroid):
        self.objects[self.next_object_id] = centroid
        self.disappeared[self.next_object_id] = 0
        self.next_object_id += 1

    def deregister(self, object_id):
        del self.objects[object_id]
        del self.disappeared[object_id]

    def update(self, rects):
        if len(rects) == 0:
            for object_id in list(self.disappeared.keys()):
                self.disappeared[object_id] += 1
                if self.disappeared[object_id] > self.max_disappeared:
                    self.deregister(object_id)
            return self.objects

        input_centroids = np.zeros((len(rects), 2), dtype="int")
        for i, (x1, y1, x2, y2) in enumerate(rects):
            input_centroids[i] = ((x1 + x2)//2, (y1 + y2)//2)

        if len(self.objects) == 0:
            for centroid in input_centroids:
                self.register(centroid)
        else:
            object_ids = list(self.objects.keys())
            object_centroids = list(self.objects.values())

            D = np.linalg.norm(np.array(object_centroids)[:, np.newaxis] - input_centroids, axis=2)
            rows = D.min(axis=1).argsort()
            cols = D.argmin(axis=1)[rows]

            used_rows = set()
            used_cols = set()
            for row, col in zip(rows, cols):
                if row in used_rows or col in used_cols:
                    continue
                object_id = object_ids[row]
                self.objects[object_id] = input_centroids[col]
                self.disappeared[object_id] = 0
                used_rows.add(row)
                used_cols.add(col)

            unused_rows = set(range(D.shape[0])) - used_rows
            unused_cols = set(range(len(input_centroids))) - used_cols

            if D.shape[0] >= len(input_centroids):
                for row in unused_rows:
                    object_id = object_ids[row]
                    self.disappeared[object_id] += 1
                    if self.disappeared[object_id] > self.max_disappeared:
                        self.deregister(object_id)
            else:
                for col in unused_cols:
                    self.register(input_centroids[col])

        return self.objects

# -----------------------------
# Load YOLO Model
# -----------------------------
model = YOLO("yolov8n.pt")  # YOLOv8 small model

# Vehicle class IDs in COCO dataset (car, motorcycle, bus, truck)
VEHICLE_CLASSES = [2, 3, 5, 7]

# -----------------------------
# Video Source
# -----------------------------
video_path = r"e:\friends\VID_20251101_124200.mp4"  # Replace with your video path
# video_path = 0  # Use this line for webcam

cap = cv2.VideoCapture(video_path)
if not cap.isOpened():
    print("Error: Cannot open video or webcam.")
    exit()

tracker = CentroidTracker()

# -----------------------------
# Main Loop
# -----------------------------
while True:
    ret, frame = cap.read()
    if not ret:
        print("End of video or cannot read frame.")
        break

    results = model(frame)[0]
    rects = []

    for box in results.boxes:
        cls_id = int(box.cls[0])
        if cls_id in VEHICLE_CLASSES:
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            rects.append((x1, y1, x2, y2))
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

    objects = tracker.update(rects)

    for object_id, centroid in objects.items():
        cv2.putText(frame, f"ID {object_id}", (centroid[0]-10, centroid[1]-10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
        cv2.circle(frame, (centroid[0], centroid[1]), 4, (0, 0, 255), -1)

    cv2.imshow("Vehicle Tracking", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
