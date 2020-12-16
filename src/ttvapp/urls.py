
from django.contrib import admin
from django.urls import path
from django.urls import include, path
from django.conf.urls.static import static
from django.conf import settings

from dashapp.views import (
    index,
    cctv_dashboard,
    cctv_cameragroup,
    cctv,
    testcctv,
    image_feed,
    projectlist,
    celldashboard,
    cameralist,
    cameraadd,
    cameraedit,
    cameraremove,
    getpcinfomation,
    
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name="index"),
    path('cctv/dashboard', cctv_dashboard, name="cctv/dashboard"),
    path('cctv/group/<int:group_id>', cctv_cameragroup, name="cctv/group"),
    path('cctv/view/<int:cam_id>', cctv, name="cctv/view"),
    path('cctv/for/<int:cam_id>', testcctv, name="cctv/for"),
    path('camera/list', cameralist, name="camera/list"),
    path('camera/add', cameraadd, name="camera/add"),
    path('camera/edit/<int:id>/',cameraedit, name="camera/edit"),
    path('camera/remove/<int:id>/',cameraremove, name="camera/remove"),
    path('image-feed/<int:id>', image_feed, name="image-feed"),
    path('project/listing', projectlist, name="project/listing"),
    path('cell/dashboard', celldashboard, name="cell/dashboard"),
    path('pcinfomation', getpcinfomation, name="pcinfomation"),

 
]


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)