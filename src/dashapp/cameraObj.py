
import cv2
import imutils
import numpy as np
from vidgear.gears import CamGear
from imutils.video import VideoStream
from. models import Cameraset

class cameraobject:

    def __init__(self, cid, link,roi,detection):
        self.cid = cid
        self.link = link
        self.roi = roi
        self.detection = detection
    
    def grap_cctv(self):
        a = self.link
        print(a)
    

    
