from django.http import HttpResponse, HttpResponseNotFound, HttpResponseBadRequest
from apps.gallery.models import *
from django.template import Context, RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from django.db.models import Count
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import redirect
from apps.gallery.forms import AlbumForm, UploadPhotoForm, AlbumEditForm
from django.contrib.auth.decorators import user_passes_test
from django.views.decorators.csrf import csrf_exempt
from django.http import Http404

import logging
logfile = settings.TEMP_DIRECTORY + 'applog.log'
logging.basicConfig(filename=logfile,level=logging.INFO)
log = logging

ALBUM_PAGE_SIZE = 10


from django.core.files.uploadedfile import UploadedFile
from django.views.decorators.csrf import csrf_exempt
from django.utils import simplejson
import random
from shutil import copyfile
#from PIL import Image, ExifTags
try:
    import Image
    import ExifTags
except ImportError:
    from PIL import Image, ExifTags
from datetime import datetime
from os import unlink
from django.core.files import File
#from easy_thumbnails.files import get_thumbnailer

def _process_uploaded_file(f, album_id):
    logid = random.randint(0,1000)
    randnumber = logid # use the random number here too
    log.info('[%s] received file to _process_uploaded_file view' % logid)

    # Dump out EXIF Tags for debugging purposes
    #im = Image.open(f)
    #if hasattr( im, '_getexif' ):
    #    exifinfo = im._getexif()
    #    if exifinfo:
    #        for tag, value in exifinfo.items():
    #            decoded = ExifTags.TAGS.get(tag, tag)
    #            log.info('Found tag: %s, value: %s' % (decoded,value))

    orientation = None
    date_taken = None
    # Make full size and thumbsize
    try:
        im = Image.open(f)
    except IOError:
        log.info('[%s] Error opening file %s: %s %s' % (logid, f, e.errno, e))
        return HttpResponseBadRequest('Could not read file')

    if hasattr( im, '_getexif' ):
        exifinfo = im._getexif()
        if exifinfo:
            for tag, value in exifinfo.items():
                decoded = ExifTags.TAGS.get(tag, tag)
#                    if decoded != 'MakerNote':
#                        if decoded != 'UserComment':
#                            log.info('Found tag: %s, value: %s' % (decoded,value))
                if decoded == 'Orientation':
                    orientation = value
                    log.info('[%s] Found tag: %s, value: %s' % (logid,decoded,value))
                elif decoded == 'DateTime':
                    date_taken =  datetime.strptime(value, "%Y:%m:%d %H:%M:%S")
                    log.info('[%s] Found tag: %s, value: %s, date_taken=%s' % (logid,decoded,value,date_taken))

    # We rotate regarding to the EXIF orientation information
    if orientation:
        if orientation == 1:
            # Nothing
            log.info('[%s] Orientation: No rotation necessary' % logid)
            pass
        elif orientation == 2:
            # Vertical Mirror
            log.info('[%s] Orientation: Vertical flip' % logid)
            im = im.transpose(Image.FLIP_LEFT_RIGHT)
        elif orientation == 3:
            # Rotation 180
            log.info('[%s] Orientation: Rotation 180' % logid)
            im = im.transpose(Image.ROTATE_180)
        elif orientation == 4:
            # Horizontal Mirror
            log.info('[%s] Orientation: Horizontal Mirror' % logid)
            im = im.transpose(Image.FLIP_TOP_BOTTOM)
        elif orientation == 5:
            # Horizontal Mirror + Rotation 270
            log.info('[%s] Orientation: Flip top bottom, rot 270' % logid)
            im = im.transpose(Image.FLIP_TOP_BOTTOM).transpose(Image.ROTATE_270)
        elif orientation == 6:
            # Rotation 270
            log.info('[%s] Orientation: Rotate 270' % logid)
            im = im.transpose(Image.ROTATE_270)
        elif orientation == 7:
            # Vertical Mirror + Rotation 270
            log.info('[%s] Orientation: Flip left right, rotate 270' % logid)
            im = im.transpose(Image.FLIP_LEFT_RIGHT).transpose(Image.ROTATE_270)
        elif orientation == 8:
            # Rotation 90
            log.info('[%s] Orientation: Rotate 90' % logid)
            im = im.transpose(Image.ROTATE_90)

    #------------------
    # Save the transposed image to disk
    orig_path = '%s_mod%s' % (f,randnumber)
    # keep 100% fidelity on the image
    try:
        log.info('[%s] Writing corrected photo to path %s' % (logid,orig_path))
        im.save(orig_path, "JPEG", quality=100)
    except IOError:
        log.info('[%s] Error saving file %s: %s %s' % (logid, orig_path, e.errno, e))
        return HttpResponseBadRequest('Could not save file')

    #------------------
    # Save the photo object into the database
    album = Album.objects.get(id=album_id)
    photo = Photo()
    photo.album = album
    photo.title = ''

    log.info('[%s] Determining photo order' % logid)
    #------------------
    # Determine where in the photo order this picture needs to be
    photo.order = 0
    if date_taken:
        photo.photodate = date_taken
        log.info('[%s] Date Taken is %s' % (logid,date_taken))
        # Now try to insert the photo by date taken in the order list
        prev_photo = photo.prev_photo_by_photodate()
        if prev_photo:
            log.info('got prev photo.  id=%s, photodate=%s, order=%s' % (prev_photo.id,prev_photo.photodate,prev_photo.order))
            photo.order = prev_photo.order
        else:
            # First in album
            photo.order = 0
    else:
        # Last in album
        photo.order = album.photo_set.count() + 1

    log.info('[%s] Writing photo entry to database' % logid)
    #------------------
    # Now finally write the entry to the db
    photo.save()
    log.info('[%s] Photo object saved.  id = %s, order = %s' % (logid, photo.id,photo.order))
    #album.reorder_photos()

    log.info('[%s] Attempting to save file %s to django model id %s' % (logid, orig_path, photo.id))
    f_ptr = open(orig_path,'rb')
    photo.filename.save('%s.jpg' % photo.id, File(f_ptr))
    f_ptr.close()

    log.info('[%s] Cleaning up files' % logid)
    #clean up temp files
    unlink(f)
    unlink(orig_path)


def main_page(request):

    albums = Album.objects.order_by('-date').filter(published='1')[:ALBUM_PAGE_SIZE]

    context = Context()
    context['albums'] = albums
    request_context = RequestContext(request)
    return render_to_response('homepage.html',
                              context,
                              request_context)

def album_list(request, page_id='1'):

    all_albums = Album.objects.all().order_by('-date').filter(published='1')
    paginator = Paginator(all_albums, ALBUM_PAGE_SIZE)
    try:
        albums = paginator.page(page_id)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        albums = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        albums = paginator.page(paginator.num_pages)

    context = Context()
    context['albums'] = albums
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

def photo_view(request, photo_id=None):

    if not photo_id:
        return HttpResponseNotFound('No such photo')

    photo = Photo.objects.get(id=photo_id)
    album = photo.album

    context = Context()
    context['photo'] = photo
    context['album'] = album
    request_context = RequestContext(request)
    return render_to_response('photo-view.html',
                              context,
                              request_context)

UPLOAD_FILE_FAIL = 0
UPLOAD_FILE_IN_PROGRESS = 1
UPLOAD_FILE_DONE = 2
def _receive_uploaded_file(request, f, album_id):

    # extract some information from the request
    current_chunk = request.REQUEST.get('chunk', '0')
    total_chunks = request.REQUEST.get('chunks', None)
    name = request.REQUEST.get('name', '')
    if not name:
        name = f.name

    print 'name: %s' % (name)

    temp_file = '%s%s' % (settings.TEMP_DIRECTORY,name)
    with open(temp_file, ('wb' if current_chunk == '0' else 'ab')) as destination:
        for chunk in f.chunks():
            print 'writing chunk!!'
            destination.write(chunk)

    if total_chunks == None:
        print '---> all done uploading: all chunks in a single request'
        _process_uploaded_file(temp_file, album_id)
        return UPLOAD_FILE_DONE

    if int(current_chunk) + 1 >= int(total_chunks):
        print '---> all done uploading'
        _process_uploaded_file(temp_file, album_id)
        return UPLOAD_FILE_DONE

    print '---> more upload to be be done'
    return UPLOAD_FILE_IN_PROGRESS

def photo_upload(request, album_id=None):

    if not album_id:
        return HttpResponseNotFound('No such album')
    album = Album.objects.get(id=album_id)

    if request.method == 'POST':
        form = UploadPhotoForm(request.POST, request.FILES)
        if form.is_valid():
            print 'got a file chunk!'
            if request.FILES == None:
                return HttpResponseBadRequest('Must have files attached!')

            #getting file data for farther manipulations
            f = request.FILES[u'file']
            rc = _receive_uploaded_file(request, f, album_id)

            if rc == UPLOAD_FILE_IN_PROGRESS:
                return HttpResponse("Keep transmitting breaker breaker")
            elif rc == UPLOAD_FILE_DONE:
                return HttpResponse("Finished Upload")
            elif rc == UPLOAD_FILE_FAIL:
                return HttpResponseBadRequest('Some Error occured')
        else:
            # invalid form
            return HttpResponseBadRequest('Bad data in form')
    else:
        form = UploadPhotoForm()

    context = Context()
    context['form'] = form
    context['album_id'] = album_id
    request_context = RequestContext(request)
    return render_to_response('photo-upload.html',
                              context,
                              request_context)


def login(request):
    context = Context()
    request_context = RequestContext(request)
    return render_to_response('login.html',
                              context,
                              request_context)

from django.contrib.auth import logout as auth_logout

def logout(request):
    auth_logout(request)
    # Redirect to homepage.
    return redirect('/')

from social_auth import __version__ as version
from django.contrib.messages.api import get_messages

def loginerror(request):

    messages = get_messages(request)
    return render_to_response('loginerror.html', {'version': version,
                                             'messages': messages},
                              RequestContext(request))


def test(request):

    log.info('Test received')

    album = Album.objects.get(id='448')
    if album:
        log.info('Found Album: %s' % album.title)
        #album.reorder_photos()
    else:
        log.info('No Album found')


    return HttpResponse ('Test working!')

@user_passes_test(lambda u: u.is_staff)
def album_upload(request,album_id):

    album = Album.objects.get(id=album_id)
    if not album:
        return HttpResponseNotFound('No such album')

    context = Context()
    context['album'] = album
    request_context = RequestContext(request)
    return render_to_response('album-upload.html',
                              context,
                              request_context)
