from django.forms import ModelForm, DateTimeInput
from apps.gallery.models import Album
from django.contrib.admin import widgets
from django import forms


class AlbumForm(ModelForm):
    class Meta:
        model = Album
        fields = ('title','description','date')


class UploadPhotoForm(forms.Form):
    file = forms.FileField()

    def save(self, temp_file, uploaded_file):
        print 'File "%s" would presumably be saved to disk now.' % uploaded_file
        pass

