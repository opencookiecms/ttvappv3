from django.shortcuts import render
import cv2
import sys
import numpy as np
import face_recognition
from vidgear.gears import CamGear
from django.http import StreamingHttpResponse, HttpResponse, HttpResponseServerError
from .cameraObj import cameraobject
from .models import Ttvproject,Ttvcell,Cctvgroup,Cameraset,Cctvline,InventoryProduct,Groupcell

# Create your views here.

def index(request):
    return render(request, 'pages/maindashboard.html')

#dashbord view
def cctv_dashboard(request):

    context = {
        'title':'Camera by Group',
        'groupcamera':Cctvgroup.objects.all(),
    }
    return render (request, 'pages/cctv_dashboard.html', context)

#camera group
def cctv_cameragroup(request, group_id):

    context = {
        'camera':Cameraset.objects.filter(camera_group=group_id),
        'groupname': Cctvgroup.objects.get(id=group_id),
        'title':'Camera Group :' 
    }
    return render (request, 'pages/discam_bygroup.html', context)


#####################cctv processing in here ##########################################
#stage 5
def grab_cctv(id):

    camera = Cameraset.objects.get(id=id)
    clink = camera.camera_link1
    print("hello"+clink)
  
    
    return clink
#stage 3
def frame_renderer(id):

    #stage 4
    camgrap = grab_cctv(id)

    cap = cv2.VideoCapture(camgrap)
    cap.set(cv2.CAP_PROP_FPS, 10)
    fps = int(cap.get(5))
    print("fps:", fps)

    while True:
        success, frame = cap.read()
        if not success:
            break
        else:
            #stage 6
            ret, buffer = cv2.imencode('.png', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # concat frame one by one and show result
            

#stage 2
def image_feed(request, id):
    if request.method == 'GET':
        try:
            return StreamingHttpResponse(frame_renderer(id), content_type='multipart/x-mixed-replace; boundary=frame')
        except HttpResponseServerError as e:
            print('respone got an error'+ e)

#stage 1
def cctv(request, cam_id):

    context = {
        'camera': Cameraset.objects.get(id=cam_id)
    }
    return render(request, 'pages/cctv_view.html',context)

#####################cctv processing in here ##########################################


def testcctv(request, cam_id):
    
    context = {
        'camera': Cameraset.objects.get(id=cam_id),
    }
    return render(request, 'pages/v_test.html',context)
