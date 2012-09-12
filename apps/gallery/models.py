# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#     * Rearrange models' order
#     * Make sure each model has one field with primary_key=True
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin.py sqlcustom [appname]'
# into your database.

from django.db import models
from django.conf import settings
from datetime import datetime
from os import unlink, error,path
#from easy_thumbnails.files import get_thumbnailer
from django.core.urlresolvers import reverse

import logging
logging.basicConfig(filename=settings.TEMP_DIRECTORY + 'applog.log',level=logging.INFO)
log = logging

class User(models.Model):
    id = models.IntegerField(primary_key=True,unique=True)
    username = models.CharField(max_length=192, db_column='UserName') # Field name made lowercase.
    password = models.CharField(max_length=192, db_column='Password') # Field name made lowercase.
    email = models.CharField(max_length=384, db_column='Email', blank=True) # Field name made lowercase.
    name = models.CharField(max_length=384, db_column='Name', blank=True) # Field name made lowercase.
    lastlogindate = models.DateTimeField(db_column='LastLoginDate') # Field name made lowercase.
    hash = models.CharField(max_length=384, db_column='Hash', blank=True) # Field name made lowercase.
    authlevel = models.IntegerField(db_column='AuthLevel') # Field name made lowercase.
    class Meta:
        db_table = u'tblUsers'

class Album(models.Model):
#    id = models.IntegerField(primary_key=True)
    parent = models.ForeignKey('Album',null=True, db_column='ParentAlbumId', blank=True) # Field name made lowercase.
    title = models.CharField(max_length=765, db_column='AlbumName') # Field name made lowercase.
    description = models.TextField(db_column='AlbumDescription', blank=True) # Field name made lowercase.
    keywords = models.CharField(max_length=765, db_column='Keywords', blank=True) # Field name made lowercase.
    date = models.DateTimeField(db_column='AlbumDate', blank=False, default=datetime.now) # Field name made lowercase.
    datecreated = models.DateTimeField(auto_now=True, auto_now_add=True,db_column='DateCreated') # Field name made lowercase.
    datelastmodified = models.DateTimeField(auto_now=True, auto_now_add=True,db_column='DateLastModified') # Field name made lowercase.
    published = models.IntegerField(db_column='Published', default=1) # Field name made lowercase.
    passwordprotected = models.IntegerField(db_column='PasswordProtected', default=0) # Field name made lowercase.
    class Meta:
        db_table = u'tblAlbums'

    def __unicode__(self):
        return self.title

    def get_url(self):
        return reverse('album-view', args=(self.id,))
    get_url.short_description = 'Link to album'

    def get_link(self):
        link = reverse('album-view', args=(self.id,))
        return '<a href="%s">%s</a>' % (link, link)
    get_link.short_description = 'Link to album'
    get_link.allow_tags = True

class Photo(models.Model):
#    id = models.BigIntegerField(primary_key=True)
#    filename = models.CharField(max_length=765, db_column='FileName', editable=False) # Field name made lowercase.
    filename = models.ImageField(upload_to='images/', null=True)
    photodate = models.CharField(max_length=765, db_column='PhotoDate', blank=True) # Field name made lowercase.
    title = models.CharField(max_length=765, db_column='Title', blank=True) # Field name made lowercase.
    description = models.CharField(max_length=765, db_column='Description', blank=True) # Field name made lowercase.
    location = models.CharField(max_length=765, db_column='Location', blank=True) # Field name made lowercase.
    keywords = models.CharField(max_length=765, db_column='Keywords', blank=True) # Field name made lowercase.
    datecreated = models.DateTimeField(db_column='DateCreated', default=datetime.now()) # Field name made lowercase.
    datelastmodified = models.DateTimeField(db_column='DateLastModified', default=datetime.now()) # Field name made lowercase.
    album = models.ForeignKey('Album',db_column='Album') # Field name made lowercase.
    order = models.IntegerField(db_column='PhotoOrder') # Field name made lowercase.
    class Meta:
        db_table = u'tblPhotos'
        ordering = ['order','photodate']

    def thumb(self):

        thumbnail_options = dict(size=(100, 100), crop=True)
        #thumb_url = get_thumbnailer(self.filename).get_thumbnail(thumbnail_options).url
        thumb_url =''
        return "<img src='%s' width=100px />" % (thumb_url)
    thumb.allow_tags = True

    def path(self):
        return "%s/origsize/%s.jpg" % (settings.MEDIA_PHOTO_PATH, self.id)

    def next_photo(self):
            photo_qs = Photo.objects.filter(order__gt=self.order,album=self.album).order_by('order')
            if len(photo_qs) == 0:
                return None
            else:
                return photo_qs[0]

    def prev_photo(self):
            photo_qs = Photo.objects.filter(album=self.album,order__lt=self.order).order_by('-order')
            if len(photo_qs) == 0:
                return None
            else:
                return photo_qs[0]

    def prev_photo_by_photodate(self):
            photo_qs = Photo.objects.filter(photodate__lt=self.photodate,album=self.album).order_by('-photodate')
            if len(photo_qs) == 0:
                return None
            else:
                return photo_qs[0]

    def __unicode__(self):
        return self.title

    def delete(self):

        try:
            unlink (self.filename.path)
        except error as e:
            pass

        # TODO: unlink thumbnail files too!
        super(Photo, self).delete()


class Notification(models.Model):
    idx = models.IntegerField(primary_key=True)
    name = models.TextField(db_column='Name') # Field name made lowercase.
    email = models.TextField(db_column='Email') # Field name made lowercase.
    lastupdate = models.DateTimeField(db_column='LastUpdate') # Field name made lowercase.
    active = models.IntegerField(db_column='Active') # Field name made lowercase.
    class Meta:
        db_table = u'tblNotification'


