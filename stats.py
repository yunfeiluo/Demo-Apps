from demo import *

def capture_and_count(n_steps=64):
    count = dict() # map: location -> number
    steps = demo(n_steps=n_steps)
    for st in steps:
        lm = st['results'].multi_hand_landmarks.landmark

if __name__ == '__main__':
    steps = capture_and_count(n_steps=64)