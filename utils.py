import copy
import pickle
import cv2
import matplotlib.pyplot as plt
import numpy as np
import sys

def centering(hand_landmarks, center=[0, 0, 0]):
    # center = [hand_landmarks.landmark[0].x, hand_landmarks.landmark[0].y, hand_landmarks.landmark[0].z]
    # center = [0.5, 0.5, hand_landmarks.landmark[0].z]
    # center = [0.5, 0.5, 0]
    x = hand_landmarks.landmark[0].x - center[0]
    y = hand_landmarks.landmark[0].y - center[1]
    z = hand_landmarks.landmark[0].z - center[2]
    for k in range(len(hand_landmarks.landmark)):
        hand_landmarks.landmark[k].x -= x
        hand_landmarks.landmark[k].y -= y
        hand_landmarks.landmark[k].z -= z 

def normalize_2_points(ref, mov, dist):
    v = mov - ref # direction
    v = dist * (v / np.linalg.norm(v)) # length times unit vector
    return v

def get_vec(lm):
    return np.array([lm.x, lm.y, lm.z])

def normalize(hand_landmarks, dists):
    orig_hl = copy.deepcopy(hand_landmarks)
    for t in dists:
        dirct = normalize_2_points(get_vec(orig_hl.landmark[t[0]]), get_vec(orig_hl.landmark[t[1]]), dists[t])
        hand_landmarks.landmark[t[1]].x = hand_landmarks.landmark[t[0]].x + dirct[0]
        hand_landmarks.landmark[t[1]].y = hand_landmarks.landmark[t[0]].y + dirct[1]
        hand_landmarks.landmark[t[1]].z = hand_landmarks.landmark[t[0]].z + dirct[2]

def change_normalize_order():
    with open('NORMAL_HAND_SPACE.pkl', 'rb') as f:
        dists = pickle.load(f)
    new_dist = dict()
    for t in [(0, 1), (1, 2), (2, 3), (3, 4), (0, 5), (5, 6), (6, 7), (7, 8), (0, 17), (17, 18), (18, 19), (19, 20), (17, 13), (13, 14), (14, 15), (15, 16), (13, 9), (9, 10), (10, 11), (11, 12)]:
        new_dist[t] = dists[t]
    
    with open('NORMAL_HAND_SPACE.pkl', 'wb') as f:
        pickle.dump(new_dist, f)

def coco_labels():
    coco_classes = np.asarray([
    '__background__', 'person', 'bicycle', 'car', 'motorcycle', 'airplane', 'bus',
    'train', 'truck', 'boat', 'traffic light', 'fire hydrant', 'N/A', 'stop sign',
    'parking meter', 'bench', 'bird', 'cat', 'dog', 'horse', 'sheep', 'cow',
    'elephant', 'bear', 'zebra', 'giraffe', 'N/A', 'backpack', 'umbrella', 'N/A', 'N/A',
    'handbag', 'tie', 'suitcase', 'frisbee', 'skis', 'snowboard', 'sports ball',
    'kite', 'baseball bat', 'baseball glove', 'skateboard', 'surfboard', 'tennis racket',
    'bottle', 'N/A', 'wine glass', 'cup', 'fork', 'knife', 'spoon', 'bowl',
    'banana', 'apple', 'sandwich', 'orange', 'broccoli', 'carrot', 'hot dog', 'pizza',
    'donut', 'cake', 'chair', 'couch', 'potted plant', 'bed', 'N/A', 'dining table',
    'N/A', 'N/A', 'toilet', 'N/A', 'tv', 'laptop', 'mouse', 'remote', 'keyboard', 'cell phone',
    'microwave', 'oven', 'toaster', 'sink', 'refrigerator', 'N/A', 'book',
    'clock', 'vase', 'scissors', 'teddy bear', 'hair drier', 'toothbrush'
    ])

    with open('coco_classes.pkl', 'wb') as f:
        print(len(coco_classes))
        pickle.dump(coco_classes, f)

if __name__ == '__main__':
    change_normalize_order()