from django.http import HttpResponse, HttpResponseNotFound, HttpResponseBadRequest
from gallery.models import *
from django.template import Context, RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from django.db.models import Count
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist

import logging
logfile = settings.TEMP_DIRECTORY + 'applog.log'
logging.basicConfig(filename=logfile,level=logging.INFO)
log = logging

def main_page(request):

#    albums_qs = Album.objects.order_by('-date').filter(published='1')[:10]
#    albums = []
#    for album in albums_qs:
#        a = album
#        if album.photo_set.count():
#            first_photo = Photo.objects.order_by('order').filter(album=album.id)[0]
#            a['thumbnail_url'] = first_photo.get_thumbnail_url
#        albums.append(a)
    albums = Album.objects.order_by('-date').filter(published='1')[:10]

    context = Context()
    context['albums'] = albums
    request_context = RequestContext(request)
    return render_to_response('homepage.html',
                              context,
                              request_context)
    
def album_list(request, page_id='0'):

    page_size = 10
    page_id = int(page_id)
    start = page_id * page_size
    end = start + page_size

    albums = Album.objects.order_by('-date').filter(published='1')[start:end]
    
    if len(albums) <= 0:
        next_page_id = None
    else:
        next_page_id = page_id + 1
    
    if page_id == 0:
        prev_page_id = None
    else:
        prev_page_id = page_id - 1

    context = Context()
    context['albums'] = albums
    context['next_page_id'] = next_page_id
    context['prev_page_id'] = prev_page_id
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

    album_dates = Album.objects.dates('date','year')

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

def mobile_album_view(request, album_id=None):

    if not album_id:
        return HttpResponseNotFound('No such album')
        
    album = Album.objects.get(id=album_id)

    context = Context()
    context['album'] = album
    request_context = RequestContext(request)
    return render_to_response('mobile-album-view.html',
                              context,
                              request_context)

def photo_view(request, photo_id=None):
    
    if not photo_id:
        return HttpResponseNotFound('No such photo')

    photo = Photo.objects.get(id=photo_id)
    
    context = Context()
    context['photo'] = photo
#    context['album'] = album
    request_context = RequestContext(request)
    return render_to_response('photo-view.html',
                              context,
                              request_context)
    
def upload_photo_interface(request, album_id=None):
    
    if not album_id:
        return HttpResponseNotFound('No such album')
    album = Album.objects.get(id=album_id)

    context = Context()
    context['album'] = album
    request_context = RequestContext(request)
    return render_to_response('upload-photo-interface.html',
                              context,
                              request_context)

def login(request):
    context = Context()
    request_context = RequestContext(request)
    return render_to_response('login.html',
                              context,
                              request_context)

from django.contrib.auth import logout as auth_logout
from django.shortcuts import redirect

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


from django.core.files.uploadedfile import UploadedFile
from django.views.decorators.csrf import csrf_exempt
from django.utils import simplejson
import random
from shutil import copyfile
from PIL import Image, ExifTags
from datetime import datetime
from os import unlink
from django.core.files import File  
from easy_thumbnails.files import get_thumbnailer

@csrf_exempt
def accept_uploaded_photo(request, album_id):
    """
    Main Multiuploader module.
    Parses data from jQuery plugin and makes database changes.
    """
    if request.method == 'POST':
        logid = random.randint(0,1000)
        log.info('[%s] received POST to main multiuploader view' % logid)
        if request.FILES == None:
            return HttpResponseBadRequest('Must have files attached!')

        #getting file data for farther manipulations
        file = request.FILES[u'files[]']
        wrapped_file = UploadedFile(file)
        filename = wrapped_file.name
        file_size = wrapped_file.file.size
        log.info ('[%s] Got file: "%s"' % (logid, str(filename)))

        # Write out file to disk as a temp file
        randnumber = logid # use the random number here too
        temp_filename = '%stmp%s_%s' % (settings.TEMP_DIRECTORY,randnumber, filename)
        log.info('[%s] Writing out to: %s' % (logid, temp_filename))
        destination = open(temp_filename, 'wb+')
        if wrapped_file.multiple_chunks():
            for chunk in wrapped_file.chunks():
                destination.write(chunk)
        else:
            destination.write(wrapped_file.read())
        destination.close()

        # Dump out EXIF Tags
#        im = Image.open(temp_filename)
#        if hasattr( im, '_getexif' ):
#            exifinfo = im._getexif()
#            if exifinfo:
#                for tag, value in exifinfo.items():
#                    decoded = ExifTags.TAGS.get(tag, tag)
#                    log.info('Found tag: %s, value: %s' % (decoded,value))

        orientation = None
        date_taken = None
        # Make full size and thumbsize
        try:
            im = Image.open(temp_filename)
        except IOError:
            log.info('[%s] Error opening file %s: %s %s' % (logid, temp_filename, e.errno, e))
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
        orig_path = '%stmp%s_mod%s' % (settings.TEMP_DIRECTORY,randnumber, filename)
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
        f = open(orig_path, 'r')        
        photo.filename.save('%s.jpg' % photo.id, File(f))
        f.close()

        log.info('[%s] Cleaning up files' % logid)
        #clean up temp file
        unlink(temp_filename)
        unlink(orig_path)
        
        #settings imports
        file_delete_url = 'multi_delete/'

        thumbnail_options = dict(size=(200, 200), crop=True)
        thumb_url = get_thumbnailer(photo.filename).get_thumbnail(thumbnail_options).url

        #generating json response array
        result = []
        result.append({"name":filename, 
                       "size":file_size, 
                       "url": thumb_url, 
                       "thumbnail_url":thumb_url,
                       "delete_url":'/', 
                       "delete_type":"POST",})
        response_data = simplejson.dumps(result)
        
        #checking for json data type
        #big thanks to Guy Shapiro
        if "application/json" in request.META['HTTP_ACCEPT_ENCODING']:
            mimetype = 'application/json'
        else:
            mimetype = 'text/plain'
        return HttpResponse(response_data, mimetype=mimetype)
    else: #GET
        return HttpResponse('Only POST accepted')


def test(request):

    log.info('Test received')
    
    album = Album.objects.get(id='448')
    if album:
        log.info('Found Album: %s' % album.title)
        #album.reorder_photos()
    else:
        log.info('No Album found')
        
    
    return HttpResponse ('Test working!')
    
 
