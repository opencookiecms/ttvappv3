from django.shortcuts import render
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

def grab_cctv(id):

    camera = Cameraset.objects.get(id=id)
    cl = camera.camera_link1
    print("hello"+cl)
    
    return cl


def frame_renderer():
    pass


def image_result(request, id):
    if request.method == 'GET':
        try:
            return StreamingHttpResponse(frame_renderer(id), content_type='multipart/x-mixed-replace; boundary=frame')
        except HttpResponseServerError as e:
            print('respone got an error'+ e)


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
