from django.forms import ModelForm, DateTimeInput
from apps.gallery.models import Album
from django.contrib.admin import widgets


class AlbumForm(ModelForm):
    class Meta:
        model = Album
        fields = ('title','description','date')
'''
        widgets = {
            'date': widgets.AdminSplitDateTime(),
        }
        widgets = {
            'title' : forms.TextInput(attrs={'placeholder':'Title','class':'required'}),
            'web_domain' : forms.TextInput(attrs={'placeholder':'Web Domain','class':'required'}),
            'address_line1' : forms.TextInput(attrs={'placeholder':'Address Line 1'}),
            'address_line2' : forms.TextInput(attrs={'placeholder':'Address Line 2'}),
            'city' : forms.TextInput(attrs={'placeholder':'City'}),            
        }

'''
