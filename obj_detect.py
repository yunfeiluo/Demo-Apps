import torch
from torchvision.models import detection

from utils import *

# for fixing ssl certificate problem
import urllib.request
import ssl
ssl._create_default_https_context = ssl._create_unverified_context
response = urllib.request.urlopen('https://www.python.org')

class ObjDetectFRCNN:
    def __init__(self):
        self.DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.CLASSES = pickle.loads(open('coco_classes.pkl', "rb").read())
        self.COLORS = np.random.uniform(0, 255, size=(len(self.CLASSES), 3))
        self.CONFIDENCE = 0.5

        # configuration and checkpoint
        self.MODELS = {
            "frcnn-resnet": detection.fasterrcnn_resnet50_fpn,
            "frcnn-mobilenet": detection.fasterrcnn_mobilenet_v3_large_320_fpn,
            "retinanet": detection.retinanet_resnet50_fpn
        }
        # load the model and set it to evaluation mode
        # model = detection.fasterrcnn_resnet50_fpn(pretrained=True)
        self.model = detection.fasterrcnn_mobilenet_v3_large_320_fpn(pretrained=True)
        self.model.eval()
        param_size = 0
        for param in self.model.parameters():
            param_size += param.nelement() * param.element_size()
        print("num param for object detection", param_size)
    
    def detect(self, image, flip=True):
        if flip:
            image = cv2.flip(image, 1)
        image.flags.writeable = True
        # Preprocess
        im = image.transpose((2, 0, 1))
        # add the batch dimension, scale the raw pixel intensities to the
        # range [0, 1], and convert the image to a floating point tensor
        im = np.expand_dims(im, axis=0)
        im = im / 255.0
        im = torch.FloatTensor(im)
        # send the input to the device and pass the it through the network to
        # get the detections and predictions
        im = im.to(self.DEVICE)

        # Forward pass
        detections = self.model(im)[0]
        return detections

    def draw(self, image, detections, flip=True):
        orig = image.copy()
        if detections is None:
            return orig
        
        if flip:
            orig = cv2.flip(orig, 1)
        # post-process
        # loop over the detections
        for i in range(0, len(detections["boxes"])):
            # extract the confidence (i.e., probability) associated with the
            # prediction
            confidence = detections["scores"][i]
            # filter out weak detections by ensuring the confidence is
            # greater than the minimum confidence
            if confidence > self.CONFIDENCE:
                # extract the index of the class label from the detections,
                # then compute the (x, y)-coordinates of the bounding box
                # for the object
                idx = int(detections["labels"][i])
                box = detections["boxes"][i].detach().cpu().numpy()
                (startX, startY, endX, endY) = box.astype("int")
                # display the prediction to our terminal
                label = "{}: {:.2f}%".format(self.CLASSES[idx], confidence * 100)
                print("[INFO] {}".format(label))
                # draw the bounding box and label on the image
                cv2.rectangle(orig, (startX, startY), (endX, endY),
                    self.COLORS[idx], 2)
                y = startY - 15 if startY - 15 > 15 else startY + 15
                cv2.putText(orig, label, (startX, y),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, self.COLORS[idx], 2)
        if flip:
            orig = cv2.flip(orig, 1)
        return orig