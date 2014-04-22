from django.http import HttpResponse, HttpResponseNotFound, HttpResponseBadRequest
from apps.gallery.models import *
from django.template import Context, RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import user_passes_test
from apps.gallery.forms import AlbumForm, UploadPhotoForm, AlbumEditForm
from django.shortcuts import redirect

import logging
logfile = settings.TEMP_DIRECTORY + 'applog.log'
logging.basicConfig(filename=logfile,level=logging.INFO)
log = logging


# num pages to show up and down
PAGINATOR_PAGES_TO_SHOW = 3

def album_list(request, page_id='1'):

    all_albums = Album.objects.all().order_by('-date').filter(published='1')
    paginator = Paginator(all_albums, settings.ALBUM_PAGE_SIZE)
    try:
        albums = paginator.page(page_id)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        albums = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        albums = paginator.page(paginator.num_pages)

    # calc number of pages to show
    prange_start = albums.number - PAGINATOR_PAGES_TO_SHOW
    prange_start = 1 if prange_start < 1 else prange_start
    prange_stop = albums.number + PAGINATOR_PAGES_TO_SHOW
    prange_stop = paginator.num_pages if prange_stop > paginator.num_pages else prange_stop
    prange = range(prange_start,prange_stop+1)
    print('start = %s, stop = %s' % (prange_start,prange_stop))
    print('prange = %s' % prange)
    print('num_pages = %s' % paginator.num_pages)

    context = Context()
    context['albums'] = albums
    context['prange'] = prange
    context['last_page'] = paginator.num_pages
    request_context = RequestContext(request)
    return render_to_response('album-list.html',
                              context,
                              request_context)

def album_list_by_year(request, year=None):

    albums = Album.objects.order_by('date').filter(published='1',date__year=year)

    context = Context()
    context['albums'] = albums
    context['next_page_id'] = None
    context['prev_page_id'] = None
    request_context = RequestContext(request)
    return render_to_response('album-list.html',
                              context,
                              request_context)

def album_list_by_year_years(request):

    album_dates = Album.objects.dates('date','year',order='DESC')

    context = Context()
    context['album_dates'] = album_dates
    request_context = RequestContext(request)
    return render_to_response('album-list-by-year.html',
                              context,
                              request_context)

def album_view(request, album_id=None):

    if not album_id:
        return HttpResponseNotFound('No such album')

    album = Album.objects.get(id=album_id)
    photos = Photo.objects.order_by('order','photodate').filter(album=album_id)

    context = Context()
    context['photos'] = photos
    context['album'] = album
    request_context = RequestContext(request)
    return render_to_response('album-view.html',
                              context,
                              request_context)


@user_passes_test(lambda u: u.is_staff)
def album_sort(request, album_id=None):

    if not album_id:
        return HttpResponseNotFound('No such album')

    album = Album.objects.get(id=album_id)
    photos = Photo.objects.order_by('order','photodate').filter(album=album_id)

    context = Context()
    context['photos'] = photos
    context['album'] = album
    request_context = RequestContext(request)
    return render_to_response('album-sort.html',
                              context,
                              request_context)

@csrf_exempt
@user_passes_test(lambda u: u.is_staff)
def album_sort_ajax(request, album_id=None):

    if not album_id:
        return HttpResponseNotFound('No such album')

    album = Album.objects.get(id=album_id)

    # walk through the photo array that was posted and save
    # each photo in order given
    for index, photo_id in enumerate(request.POST.getlist('photo[]')):
        photo = get_object_or_404(Photo, id=int(str(photo_id)))
        photo.order = index
        photo.save()

    return HttpResponse("Ok")

@user_passes_test(lambda u: u.is_staff)
def album_edit(request, album_id=None):

    if not album_id:
        return HttpResponseNotFound('No such album')

    album = Album.objects.get(id=album_id)
    photos = Photo.objects.order_by('order','photodate').filter(album=album_id)

    context = Context()
    context['photos'] = photos
    context['album'] = album
    request_context = RequestContext(request)
    return render_to_response('album-edit.html',
                              context,
                              request_context)

@csrf_exempt
@user_passes_test(lambda u: u.is_staff)
def album_edit_ajax(request, album_id=None):

    if not album_id:
        return HttpResponseNotFound('No such album')
    album = get_object_or_404(Album, id=album_id)

    form = AlbumEditForm(request.POST)
    if form.is_valid():
        new_val = form.cleaned_data['value']
        action,photo_id = form.cleaned_data['id'].split('|',1)

        photo = get_object_or_404(Photo, id=int(str(photo_id)))
        # verify photo exists in current album
        if photo.album != album:
            return HttpResponseBadRequest('Wrong album')

        if action == 'title':
            photo.title = new_val
            photo.save()
        elif action == 'description':
            photo.description = new_val
            photo.save()

        return HttpResponse(new_val)
    else:
        return HttpResponseBadRequest('Invalid Parameters')

@user_passes_test(lambda u: u.is_staff)
def album_new(request):

    if request.method == 'POST':
        form = AlbumForm(request.POST)
        if form.is_valid():

            album = form.save()
            return redirect(album.get_url())
    else:
        form = AlbumForm()

    context = Context()
    context['form'] = form
    request_context = RequestContext(request)
    return render_to_response('album-new.html',
                              context,
                              request_context)
