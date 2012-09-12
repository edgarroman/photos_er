from django.contrib import admin
from apps.gallery.models import User
from apps.gallery.models import Album
from apps.gallery.models import Photo
from apps.gallery.models import Notification


admin.site.register(User)
admin.site.register(Notification)

class PhotoAdmin(admin.ModelAdmin):
    date_hierarchy = 'datecreated'
    list_display = ('id','title','filename','order','photodate','datecreated', 'album')
    list_filter = ('album__title',)
    search_fields = ['title']
admin.site.register(Photo,PhotoAdmin)


# http://stackoverflow.com/questions/2227891/customising-django-admin-tabularinline-default-field

class PhotoInline(admin.TabularInline):
    model = Photo
    fields = ('thumb', 'title', 'photodate','datecreated', 'order')
    readonly_fields = ('thumb', 'photodate', 'datecreated',)
#    date_hierarchy = 'datecreated'
#    list_display = ('id','title','filename','order','datecreated')
#    list_filter = ('album__title',)
    sortable_field_name = 'order'
class AlbumAdmin(admin.ModelAdmin):
    date_hierarchy = 'date'
    list_display = ('id','title','get_link','date')
    search_fields = ['title']
    inlines = [
        PhotoInline
    ]
admin.site.register(Album,AlbumAdmin)

