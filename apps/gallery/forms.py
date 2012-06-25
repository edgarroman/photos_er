from django.forms import ModelForm, DateTimeInput
from apps.gallery.models import Album
from django.contrib.admin import widgets


class AlbumForm(ModelForm):
    class Meta:
        model = Album
        fields = ('title','description','date')
