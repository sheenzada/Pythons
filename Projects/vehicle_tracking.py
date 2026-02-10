import cv2
import numpy as np
from ultralytics import YOLO
from scipy.optimize import linear_sum_assignment
from filterpy.kalman import KalmanFilter

# ================= SORT TRACKER =================

def iou(bb_test, bb_gt):
    xx1 = np.maximum(bb_test[0], bb_gt[0])
    yy1 = np.maximum(bb_test[1], bb_gt[1])
    xx2 = np.minimum(bb_test[2], bb_gt[2])
    yy2 = np.minimum(bb_test[3], bb_gt[3])
    w = np.maximum(0., xx2 - xx1)
    h = np.maximum(0., yy2 - yy1)
    wh = w * h
    return wh / ((bb_test[2]-bb_test[0])*(bb_test[3]-bb_test[1])
                 + (bb_gt[2]-bb_gt[0])*(bb_gt[3]-bb_gt[1]) - wh)

class KalmanBoxTracker:
    count = 0

    def __init__(self, bbox):
        self.kf = KalmanFilter(dim_x=7, dim_z=4)
        self.kf.F = np.array([
            [1,0,0,0,1,0,0],
            [0,1,0,0,0,1,0],
            [0,0,1,0,0,0,1],
            [0,0,0,1,0,0,0],
            [0,0,0,0,1,0,0],
            [0,0,0,0,0,1,0],
            [0,0,0,0,0,0,1]
        ])
        self.kf.H = np.array([
            [1,0,0,0,0,0,0],
            [0,1,0,0,0,0,0],
            [0,0,1,0,0,0,0],
            [0,0,0,1,0,0,0]
        ])
        self.kf.x[:4] = bbox.reshape((4,1))
        self.time_since_update = 0
        self.id = KalmanBoxTracker.count
        KalmanBoxTracker.count += 1

    def update(self, bbox):
        self.time_since_update = 0
        self.kf.update(bbox)

    def predict(self):
        self.time_since_update += 1
        self.kf.predict()
        return self.kf.x[:4].reshape((4,))

class Sort:
    def __init__(self, max_age=10, iou_threshold=0.3):
        self.trackers = []
        self.max_age = max_age
        self.iou_threshold = iou_threshold

    def update(self, dets):
        trks = np.zeros((len(self.trackers), 4))
        for t, trk in enumerate(trks):
            trks[t] = self.trackers[t].predict()

        matched, unmatched_dets, unmatched_trks = associate_detections_to_trackers(
            dets, trks, self.iou_threshold)

        for m in matched:
            self.trackers[m[1]].update(dets[m[0], :4])

        for i in unmatched_dets:
            self.trackers.append(KalmanBoxTracker(dets[i, :4]))

        i = len(self.trackers)
        for trk in reversed(self.trackers):
            i -= 1
            if trk.time_since_update > self.max_age:
                self.trackers.pop(i)

        ret = []
        for trk in self.trackers:
            d = trk.kf.x[:4].reshape((4,))
            ret.append(np.concatenate((d, [trk.id])))
        return np.array(ret)

def associate_detections_to_trackers(detections, trackers, iou_threshold):
    if len(trackers) == 0:
        return [], np.arange(len(detections)), []

    iou_matrix = np.zeros((len(detections), len(trackers)), dtype=np.float32)
    for d in range(len(detections)):
        for t in range(len(trackers)):
            iou_matrix[d,t] = iou(detections[d], trackers[t])

    matched_indices = linear_sum_assignment(-iou_matrix)
    matched_indices = np.array(list(zip(*matched_indices)))

    unmatched_detections = []
    for d in range(len(detections)):
        if d not in matched_indices[:,0]:
            unmatched_detections.append(d)

    unmatched_trackers = []
    for t in range(len(trackers)):
        if t not in matched_indices[:,1]:
            unmatched_trackers.append(t)

    matches = []
    for m in matched_indices:
        if iou_matrix[m[0], m[1]] < iou_threshold:
            unmatched_detections.append(m[0])
            unmatched_trackers.append(m[1])
        else:
            matches.append(m.reshape(1,2))

    if len(matches) == 0:
        matches = np.empty((0,2), dtype=int)
    else:
        matches = np.concatenate(matches, axis=0)

    return matches, np.array(unmatched_detections), np.array(unmatched_trackers)

# ================= MAIN PROGRAM =================

model = YOLO("yolov8n.pt")
tracker = Sort()

VEHICLE_CLASSES = [2, 3, 5, 7]  # car, motorcycle, bus, truck

cap = cv2.VideoCapture("traffic.mp4")  # use 0 for webcam

while True:
    ret, frame = cap.read()
    if not ret:
        break

    detections = []

    results = model(frame)[0]

    for box in results.boxes:
        cls = int(box.cls[0])
        conf = float(box.conf[0])

        if cls in VEHICLE_CLASSES and conf > 0.4:
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            detections.append([x1, y1, x2, y2])

    detections = np.array(detections)

    tracks = tracker.update(detections)

    for track in tracks:
        x1, y1, x2, y2, track_id = map(int, track)
        cv2.rectangle(frame, (x1,y1), (x2,y2), (0,255,0), 2)
        cv2.putText(frame, f"ID {track_id}", (x1, y1-10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,255,0), 2)

    cv2.imshow("Vehicle Detection & Tracking", frame)

    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
