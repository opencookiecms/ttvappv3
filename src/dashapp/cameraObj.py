
import cv2
import imutils
import numpy as np
from vidgear.gears import CamGear
from imutils.video import VideoStream
from. models import Cameraset

class cameraobject(object):

    def __init__(self, id=object):
        self.id=id

    def ROI(self):
        cam = Cameraset.objects.get(id=id)

        point1 = [camera.camera_point1x,camera.camera_point1y] # p1(x,y)..............p2(x,y)
        point2 = [camera.camera_point2x,camera.camera_point2y]
        point3 = [camera.camera_point3x,camera.camera_point3y]
        point4 = [camera.camera_point4x,camera.camera_point4y] #p4(x,y)................p3(x,y)

        #point1 = [10,10] # p1(x,y)..............p2(x,y)
        #point2 = [300,10]
        #point3 = [300,300]
        #point4 = [10,300] #p4(x,y)................p3(x,y)

        pts = np.array([point1,point2,point3,point4],np.int32)
        pts = pts.reshape((-1,1,2))
        #overlay = frame.copy(
        cv2.polylines(frame,[pts],True,(0,255,255))

        #cv2.addWeighted(overlay,0.3,frame,1-0.65,0,frame)

    def objectDetection(self):
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)  # converts image to gray
        

    def annotation(self):
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(frame,'test camera',(20,50), font, 1,(255,255,255),2,cv2.LINE_AA)
