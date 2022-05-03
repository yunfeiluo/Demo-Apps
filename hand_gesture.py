import mediapipe as mp

from utils import *

class HandGesture:
    def __init__(self):
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_hands = mp.solutions.hands

        with open('NORMAL_HAND_SPACE.pkl', 'rb') as f:
            self.dists = pickle.load(f)
    
    def detect(self, image, flip=True):
        with self.mp_hands.Hands(
            max_num_hands=1,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5) as hands:
                
            # HAND GESTURE RECOGNITION
            # To improve performance, optionally mark the image as not writeable to
            # pass by reference.
            image.flags.writeable = False
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            results = hands.process(image)
        return results
    
    def draw(self, image, results):
        orig = image.copy()
        normal_img = np.zeros(image.shape)
        if results.multi_hand_landmarks:
            # image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

            # check what inside the marks
            # for lm in results.multi_hand_landmarks[0].landmark:
            #     print(lm)
            # print(results.multi_hand_landmarks[0].landmark[0])
            # print('=================\n')

            # draw the gestures, will be [hand_landmarks] if 1 hand; array in hand_landmarks.landmark
            for hand_landmarks in results.multi_hand_landmarks:
                # draw on original image
                self.mp_drawing.draw_landmarks(
                    orig,
                    hand_landmarks,
                    self.mp_hands.HAND_CONNECTIONS) # connections is a list of tuples
                # cv2.imwrite('cam_buffer/result{}.png'.format(i), cv2.flip(image, 1))

                # draw on normal space
                centering(hand_landmarks, center=[0.5, 0.5, 0])
                normalize(hand_landmarks, self.dists)
                self.mp_drawing.draw_landmarks(
                    normal_img,
                    hand_landmarks,
                    self.mp_hands.HAND_CONNECTIONS)
        return orig, normal_img
