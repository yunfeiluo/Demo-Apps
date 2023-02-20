from utils import *
# from obj_detect import *
from hand_gesture import *

# main functions
def demo(n_steps=64, hand_detector=None, obj_detector=None, flip=True):
    steps = list()

    # For webcam input:
    cap = cv2.VideoCapture(0)
    i = -1
    img = None
    while cap.isOpened():
        if i >= n_steps:
            break
        i += 1
        success, image = cap.read()
        # h, w, c = image.shape
        if not success:
            print("Ignoring empty camera frame.")
            # If loading a video, use 'break' instead of 'continue'.
            continue

        # HAND GEDSTURE RECOGNITION
        results = hand_detector.detect(image)

        # OBJECT DETECTION
        detections = None
        if obj_detector is not None:
            detections = obj_detector.detect(image, flip=flip)

        # draw the hand skeleton on
        img_w_hand, normal_img = hand_detector.draw(image, results)
        
        # draw the object box on
        if obj_detector is not None:
            image_w_objs = obj_detector.draw(img_w_hand, detections, flip=flip)
            # Flip the image horizontally for a selfie-view display.
            final_img = cv2.flip(image_w_objs, 1) if flip else image_w_objs
        else:
            final_img = cv2.flip(img_w_hand, 1) if flip else img_w_hand

        # display the hand skeleton in normal space
        if img is None:
            img = plt.imshow(normal_img)
        else:
            img.set_data(normal_img)
        plt.pause(.1)
        plt.draw()

        # image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        cv2.imshow('MediaPipe Hands', final_img)

        # add to log
        steps.append({'image': image, 'results': results, 'detections': detections})

        # exit if there are no motion for about 5 seconds
        if cv2.waitKey(5) & 0xFF == 27:
            break
    
    # close camera and release the memory resource
    cap.release()

    # # For Normalization
    # last_lm = steps[-1]['results'].multi_hand_landmarks[0].landmark
    # dists = dict()
    # # for t in [(0, 1), (1, 2), (2, 3), (3, 4), (0, 5), (5, 6), (6, 7), (7, 8), (0, 17), (17, 18), (18, 19), (19, 20), (17, 13), (13, 14), (14, 15), (15, 16), (13, 9), (9, 10), (10, 11), (11, 12)]:
    # for t in [(0, 1), (1, 2), (2, 3), (3, 4), (0, 5), (5, 6), (6, 7), (7, 8), (5, 9), (9, 10), (10, 11), (11, 12), (9, 13), (13, 14), (14, 15), (15, 16), (13, 17), (17, 18), (18, 19), (19, 20)]:
    #     dists[t] = np.linalg.norm(get_vec(last_lm[t[0]]) - get_vec(last_lm[t[1]]))
    # with open('NORMAL_HAND_SPACE.pkl', 'wb') as f:
    #     pickle.dump(dists, f)

    return steps

# def draw_stream_3d(steps):
#     for st in steps:
#         # Creating dataset
#         x = list()
#         y = list()
#         z = list()
#         for i in st['results'].multi_hand_landmarks[0].landmark:
#             x.append(1 - i.x)
#             y.append(1 - i.y)
#             z.append(1 - i.z)
        
#         # Creating figure
#         fig = plt.figure(figsize = (10, 7))
#         ax = plt.axes(projection ="3d")
        
#         # Creating plot
#         ax.scatter3D(x, z, y, color = "blue")
#         for connect in mp_hands.HAND_CONNECTIONS:
#             ax.plot3D([x[connect[0]], x[connect[1]]], [z[connect[0]], z[connect[1]]], [y[connect[0]], y[connect[1]]], 'gray')
#         ax.set_xlabel('x')
#         ax.set_ylabel('z')

#         plt.title("3D scatter gesture plot")
        
#         # show plot
#         plt.show()

if __name__ == '__main__':
    num = sys.argv[1]
    num = np.inf if num == 'inf' else int(num)
    # obj_detector = ObjDetectFRCNN()
    hand_detector = HandGesture()
    steps = demo(n_steps=num, hand_detector=hand_detector, obj_detector=None) # steps containing image, results for hand gesture, and detection for objects
    print('Capture success')
    # draw_stream_3d(steps)