from django.conf.urls.defaults import *
from photos_er import settings

urlpatterns = patterns('apps.gallery.views',
    url(r'^$', 'main_page', name='home'),
    url(r'^albums/page/(?P<page_id>\d+)/$', 'album_list', name='album-list'),
    url(r'^album/(?P<album_id>\d+)/$', 'album_view', name='album-view'),

    # Album endpoints
    url(r'^album/(?P<album_id>\d+)/sort/$', 'album_sort', name='album-sort'),
    url(r'^album/(?P<album_id>\d+)/sort/ajax$', 'album_sort_ajax', name='album-sort-ajax'),
    url(r'^album/(?P<album_id>\d+)/edit/$', 'album_edit', name='album-edit'),
    url(r'^album/new/$', 'album_new', name='album-new'),    
    
    # Upload endpoints
    url(r'^album/(?P<album_id>\d+)/upload/$', 'album_upload', name='album-upload'),
    url(r'^album/(?P<album_id>\d+)/upload/photo/$', 'photo_upload', name='photo-upload'),

    url(r'^photo/(?P<photo_id>\d+)/$', 'photo_view', name='photo-view'),
    url(r'^album-list-by-year/$', 'album_list_by_year_years', name='album-list-by-year-years'),
    url(r'^album-list-by-year/(?P<year>\d+)/$', 'album_list_by_year', name='album-list-by-year'),    

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