from django import forms
from .models import Cameraset, Cctvgroup, Ttvproject, Ttvcell

class CameraForm(forms.ModelForm):

    camera_name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control rounded','placeholder':'Camera Name'}))
    camera_no = forms.IntegerField(required=False, widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Camera No','value':'0'}))
    camera_link1 = forms.CharField(required=False, widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Link for master camera'}))
    camera_link2 = forms.CharField(required=False, widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Link for slave camera'}))
    camera_main = forms.CharField(required=False, widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Main camera id'}))
    camera_slave = forms.CharField(required=False, widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Slave camera id'}))
    camera_point1x =forms.IntegerField(required=False, widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Overlay Point x1','value':'0'}))
    camera_point1y =forms.IntegerField(required=False, widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Overlay Point y1','value':'0'}))
    camera_point2x =  forms.IntegerField(required=False, widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Overlay Point x2','value':'0'}))
    camera_point2y =  forms.IntegerField(required=False, widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Overlay Point y2','value':'0'}))
    camera_point3x =  forms.IntegerField(required=False, widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Overlay Point x3','value':'0'}))
    camera_point3y =  forms.IntegerField(required=False, widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Overlay Point y3','value':'0'}))
    camera_point4x =  forms.IntegerField(required=False, widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Overlay Point x4','value':'0'}))
    camera_point4y =  forms.IntegerField(required=False, widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Overlay Point y4','value':'0'}))
    camera_overlay = forms.IntegerField(required=False, widget=forms.TextInput(attrs={'class':'form-control','placeholder':'1 or 0','value':'0'}))
    camera_detection = forms.IntegerField(required=False, widget=forms.TextInput(attrs={'class':'form-control','placeholder':'1 or 0','value':'0'}))
    camera_annotation = forms.IntegerField(required=False, widget=forms.TextInput(attrs={'class':'form-control','placeholder':'1 or 0','value':'0'}))
    camera_group = forms.ModelChoiceField(required=False, queryset=Cctvgroup.objects.all(), widget=forms.Select(attrs={'class':'form-control'}))
    camera_cell_tag = forms.MultipleChoiceField(required=False)

    class Meta:
        model = Cameraset
        fields = [
            'camera_name',
            'camera_no',
            'camera_link1',
            'camera_link2',
            'camera_main',
            'camera_slave',
            'camera_point1x',
            'camera_point1y',
            'camera_point2x',
            'camera_point2y',
            'camera_point3x', 
            'camera_point3y',
            'camera_point4x', 
            'camera_point4y', 
            'camera_overlay',
            'camera_detection',
            'camera_annotation',
            'camera_group',
            'camera_cell_tag',
        ]