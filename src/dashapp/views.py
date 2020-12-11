import cv2
import sys
import os
import time
import imutils
import numpy as np
import face_recognition
from django.shortcuts import render, get_list_or_404, redirect, reverse
from vidgear.gears import CamGear
from .cameraObj import cameraobject
from django.conf.urls.static import static
from django.conf import settings
from django.http import StreamingHttpResponse, HttpResponse, HttpResponseServerError
from .models import Ttvproject,Ttvcell,Cctvgroup,Cameraset,Cctvline,InventoryProduct,Groupcell
from .forms import CameraForm


base_dir = settings.BASE_DIR


def get_chatroom(name):
    for conversation in twilio_client.conversations.conversations.list():
        if conversation.friendly_name == name:
            return conversation

    return twilio_client.conversations.conversations.create(
        friendly_name=name)

# Create your views here.
def index(request):
    return render(request, 'pages/maindashboard.html')

#dashbord view
def cctv_dashboard(request):

    context = {
        'title':'Camera by Group',
        'groupcamera':Cctvgroup.objects.all(),
    }

    #STATICFILES_DIRS = os.path.join(base_dir, "static_in_env/facedetect/haarcascade_frontalface_alt.xml")
    

    #print(STATICFILES_DIRS)


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

    camr = grab_cctv(id)
    cap = cv2.VideoCapture("")
    time.sleep(2.0)
    sub = cv2.createBackgroundSubtractorMOG2()

    while cap:
        camera = Cameraset.objects.get(id=id)
        cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
        ret, frame = cap.read()# import image
        frame = imutils.resize(frame, width=700)

        if(camera.camera_overlay == 1):

            point1 = [camera.camera_point1x,camera.camera_point1y] # p1(x,y)..............p2(x,y)
            point2 = [camera.camera_point2x,camera.camera_point2y]
            point3 = [camera.camera_point3x,camera.camera_point3y]
            point4 = [camera.camera_point4x,camera.camera_point4y] #p4(x,y)................p3(x,y)
            
            pts = np.array([point1,point2,point3,point4],np.int32)
            pts = pts.reshape((-1,1,2))
        
            cv2.polylines(frame,[pts],True,(0,255,255))
        
        if(camera.camera_annotation == 1):
            
            font = cv2.FONT_HERSHEY_SIMPLEX
            cv2.putText(frame,'test camera',(20,50), font, 1,(255,255,255),2,cv2.LINE_AA)

        if not ret: #if vid finish repeat
            frame = cv2.VideoCapture(cam)
            continue
        if ret:
            image = cv2.resize(frame, (0, 0), None, 1, 1)  # resize image

            if(camera.camera_detection == 1):

                gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)  # converts image to gray
                fgmask = sub.apply(gray)  # uses the background subtraction
                kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))  # kernel to apply to the morphology
                closing = cv2.morphologyEx(fgmask, cv2.MORPH_CLOSE, kernel)
                opening = cv2.morphologyEx(closing, cv2.MORPH_OPEN, kernel)
                dilation = cv2.dilate(opening, kernel)
                retvalbin, bins = cv2.threshold(dilation, 220, 255, cv2.THRESH_BINARY)  # removes the shadows
                contours, hierarchy = cv2.findContours(dilation, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                minarea = 400
                maxarea = 50000
                for i in range(len(contours)): 
                    # cycles through all contours in current frame
                    if hierarchy[0, i, 3] == -1: 
                        # using hierarchy to only count parent contours (contours not within others)
                        area = cv2.contourArea(contours[i])  # area of contour
                        if minarea < area < maxarea: 
                            # area threshold for contour
                            # calculating centroids of contours
                            cnt = contours[i]
                            M = cv2.moments(cnt)
                            cx = int(M['m10'] / M['m00'])
                            cy = int(M['m01'] / M['m00'])
                            # gets bounding points of contour to create rectangle
                            # x,y is top left corner and w,h is width and height
                            x, y, w, h = cv2.boundingRect(cnt)
                            # creates a rectangle around contour
                            cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
                            # Prints centroid text in order to double check later on
                            cv2.putText(image, str(cx) + "," + str(cy), (cx + 10, cy + 10), cv2.FONT_HERSHEY_SIMPLEX,.3, (0, 0, 255), 1)
                            cv2.drawMarker(image, 
                            (cx, cy), (0, 255, 255), cv2.MARKER_CROSS, markerSize=8, thickness=3,line_type=cv2.LINE_8)
                            #cv2.imshow("countours", image)

            frame = cv2.imencode('.png', image)[1].tobytes()
            yield (b'--frame\r\n'b'Content-Type: image/png\r\n\r\n' + frame + b'\r\n')
            #fps.update()
    del(camera)

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


#this is project section

def projectlist(request):
    context = {
        'projectlist':Ttvproject.objects.all()
    }
    return render(request, 'pages/project-list.html',context)

#end of project section

#this is camera section

def cameralist(request):
    context = {
        'cameralist':Cameraset.objects.all()
    }
    return render(request, 'pages/camera-list.html',context)

def cameraadd(request):

    form = CameraForm(request.POST or None)
    if form.is_valid():
        form.save()
        form = CameraForm()
    else:
        print(form)
        print('the data was not save')

    data = {
      'msg':"the data not save" ,
      'form':form
    }

    return render(request, 'pages/camera-add.html',data)

def cameraedit(request, id):
    dataobject = Cameraset.objects.get(id=id)
    form = CameraForm(request.POST or None, instance=dataobject)
    if form.is_valid():
        form.save()
    else:
        print('data was no save')
        print(form)
    
    data = {
        'form':form
    }

    return render(request, 'pages/camera-edit.html',data)

def cameraremove(request, id):
    dataobject = Cameraset.objects.get(id=id)
    dataobject.delete()

    if dataobject:
        return redirect('camera/list')
    else:
        return render(request, 'pages/camera-list.html')

#end of camera list section

#cell section in here
def celldashboard(request):
    context = {
        'cell':Ttvcell.objects.all()
    }
    return render(request, 'pages/cell-dashboard.html')
#end of cell section

def conferenceRoom(request):

    if request.method == 'POST':
        username = request.get_json(force=True).get('username')
        if not username:
            abort(401)
        conversation = get_chatroom('My Room')
        try:
            conversation.participants.create(identity=username)
        except TwilioRestException as exc:
            if exc.status != 409:
                raise
        token = AccessToken(twilio_account_sid, twilio_api_key_sid,twilio_api_key_secret, identity=username)
        token.add_grant(VideoGrant(room='My Room'))
        token.add_grant(ChatGrant(service_sid=conversation.chat_service_sid))
        return {'token': token.to_jwt().decode(),'conversation_sid': conversation.sid}

    return render(request, 'pages/conference.html')

