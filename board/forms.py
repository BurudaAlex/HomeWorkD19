from django import forms
from .models import Advertisement, Response, MediaFile



class AdvertisementForm(forms.ModelForm):
    class Meta:
        model = Advertisement
        fields = ['title', 'content', 'category']

class AdvertisementForm(forms.ModelForm):
    class Meta:
        model = Advertisement
        fields = ['category', 'title', 'content']

class MediaFileForm(forms.ModelForm):
    class Meta:
        model = MediaFile
        fields = ['file']

class ResponseForm(forms.ModelForm):
    class Meta:
        model = Response
        fields = ['content']