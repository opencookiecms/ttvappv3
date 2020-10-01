from django.shortcuts import render
from .models import Ttvproject,Ttvcell,Cctvgroup,Cameraset,Cctvline,InventoryProduct,Groupcell

# Create your views here.

def index(request):
    return render(request, 'pages/maindashboard.html')

def cctv_dashboard(request):

    context = {
        'title':'Camera by Group',
        'groupcamera':Cctvgroup.objects.all(),
    }
    return render (request, 'pages/cctv_dashboard.html', context)

def cctv_cameragroup(request, group_id):

    context = {
        'camera':Cameraset.objects.filter(camera_group=group_id),
        'groupname': Cctvgroup.objects.get(id=group_id),
        'title':'Camera Group :' 
    }
    return render (request, 'pages/discam_bygroup.html', context)

def cctv(request, cam_id):

    context = {
        'camera': Cameraset.objects.get(id=cam_id),
    }
    return render(request, 'pages/cctv_view.html',context)
