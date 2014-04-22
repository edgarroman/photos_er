from django.conf.urls.defaults import *
from photos_er import settings

urlpatterns = patterns('apps.gallery.views',
    url(r'^$', 'home.main_page', name='home'),
    url(r'^albums/page/(?P<page_id>\d+)/$', 'album.album_list', name='album-list'),
    url(r'^album/(?P<album_id>\d+)/$', 'album.album_view', name='album-view'),

    #--------------------------
    # Album endpoints
    #--------------------------

    # Sorting
    url(r'^album/(?P<album_id>\d+)/sort/$', 'album.album_sort', name='album-sort'),
    url(r'^album/(?P<album_id>\d+)/sort/ajax$', 'album.album_sort_ajax', name='album-sort-ajax'),
    # Edit album
    url(r'^album/(?P<album_id>\d+)/edit/$', 'album.album_edit', name='album-edit'),
    url(r'^album/(?P<album_id>\d+)/edit/ajax/$', 'album.album_edit_ajax', name='album-edit-ajax'),
    # Create new album
    url(r'^album/new/$', 'album.album_new', name='album-new'),

    # Upload endpoints
    url(r'^album/(?P<album_id>\d+)/upload/$', 'upload.album_upload', name='album-upload'),
    url(r'^album/(?P<album_id>\d+)/upload/photo/$', 'upload.photo_upload', name='photo-upload'),

    url(r'^photo/(?P<photo_id>\d+)/$', 'home.photo_view', name='photo-view'),
    url(r'^album-list-by-year/$', 'album.album_list_by_year_years', name='album-list-by-year-years'),
    url(r'^album-list-by-year/(?P<year>\d+)/$', 'album.album_list_by_year', name='album-list-by-year'),

    url(r'^test$', 'home.test'),

    url(r'^login/$', 'home.login', name='login'),
    url(r'^logout/$', 'home.logout', name='logout'),
    url(r'^login-error/$', 'home.loginerror', name='loginerror'),

)

if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^photos/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.MEDIA_ROOT,
        }),
   )