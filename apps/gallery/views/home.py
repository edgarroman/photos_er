from django.http import HttpResponse, HttpResponseNotFound, HttpResponseBadRequest
from apps.gallery.models import *
from django.template import Context, RequestContext
from django.shortcuts import render_to_response, get_object_or_404

from django.db.models import Count
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist

import logging
log = logging.getLogger(__name__)

def main_page(request):

    albums = Album.objects.order_by('-date').filter(published='1')[:settings.ALBUM_PAGE_SIZE]

    context = Context()
    context['albums'] = albums
    request_context = RequestContext(request)
    return render_to_response('homepage.html',
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
    return HttpResponse ('Test working!')

