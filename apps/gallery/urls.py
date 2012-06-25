from django.conf.urls.defaults import *
from photos_er import settings

urlpatterns = patterns('apps.gallery.views',
    url(r'^$', 'main_page', name='home'),
    url(r'^albums/page/(?P<page_id>\d+)/$', 'album_list', name='album-list'),
    url(r'^album/(?P<album_id>\d+)/$', 'album_view', name='album-view'),
    url(r'^album/(?P<album_id>\d+)/upload/$', 'album_upload', name='album-upload'),
    url(r'^photo/(?P<photo_id>\d+)/$', 'photo_view', name='photo-view'),
    url(r'^album-list-by-year/$', 'album_list_by_year_years', name='album-list-by-year-years'),
    url(r'^album-list-by-year/(?P<year>\d+)/$', 'album_list_by_year', name='album-list-by-year'),    

    url(r'^album/new/$', 'album_new', name='album-new'),    


    url(r'^malbum/(?P<album_id>\d+)/$', 'mobile_album_view', name='mobile-album-view'),
    
    url(r'^uploadphotointerface/(?P<album_id>\d+)/$', 'upload_photo_interface', name='uploadphotointerface'),
    url(r'^uploadphotointerface/(?P<album_id>\d+)/upload/$', 'accept_uploaded_photo', name='acceptuploadedphoto'),

    url(r'^test$', 'test'),
    
    url(r'^login/$', 'login', name='login'),
    url(r'^logout/$', 'logout', name='logout'),
    url(r'^login-error/$', 'loginerror', name='loginerror'),    
    
)

if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^photos/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.MEDIA_ROOT,
        }),
   )