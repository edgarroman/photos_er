# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Album',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=765, db_column=b'AlbumName')),
                ('description', models.TextField(db_column=b'AlbumDescription', blank=True)),
                ('keywords', models.CharField(max_length=765, db_column=b'Keywords', blank=True)),
                ('date', models.DateTimeField(default=datetime.datetime.now, db_column=b'AlbumDate')),
                ('datecreated', models.DateTimeField(auto_now=True, auto_now_add=True, db_column=b'DateCreated')),
                ('datelastmodified', models.DateTimeField(auto_now=True, auto_now_add=True, db_column=b'DateLastModified')),
                ('published', models.IntegerField(default=1, db_column=b'Published')),
                ('passwordprotected', models.IntegerField(default=0, db_column=b'PasswordProtected')),
                ('parent', models.ForeignKey(db_column=b'ParentAlbumId', blank=True, to='gallery.Album', null=True)),
            ],
            options={
                'db_table': 'tblAlbums',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('idx', models.IntegerField(serialize=False, primary_key=True)),
                ('name', models.TextField(db_column=b'Name')),
                ('email', models.TextField(db_column=b'Email')),
                ('lastupdate', models.DateTimeField(db_column=b'LastUpdate')),
                ('active', models.IntegerField(db_column=b'Active')),
            ],
            options={
                'db_table': 'tblNotification',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Photo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('filename', models.ImageField(null=True, upload_to=b'images/')),
                ('photodate', models.CharField(max_length=765, db_column=b'PhotoDate', blank=True)),
                ('title', models.CharField(max_length=765, db_column=b'Title', blank=True)),
                ('description', models.CharField(max_length=765, db_column=b'Description', blank=True)),
                ('location', models.CharField(max_length=765, db_column=b'Location', blank=True)),
                ('keywords', models.CharField(max_length=765, db_column=b'Keywords', blank=True)),
                ('datecreated', models.DateTimeField(default=datetime.datetime(2014, 11, 17, 20, 24, 41, 746067), db_column=b'DateCreated')),
                ('datelastmodified', models.DateTimeField(default=datetime.datetime(2014, 11, 17, 20, 24, 41, 746100), db_column=b'DateLastModified')),
                ('order', models.IntegerField(db_column=b'PhotoOrder')),
                ('album', models.ForeignKey(to='gallery.Album', db_column=b'Album')),
            ],
            options={
                'ordering': ['order', 'photodate'],
                'db_table': 'tblPhotos',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.IntegerField(unique=True, serialize=False, primary_key=True)),
                ('username', models.CharField(max_length=192, db_column=b'UserName')),
                ('password', models.CharField(max_length=192, db_column=b'Password')),
                ('email', models.CharField(max_length=384, db_column=b'Email', blank=True)),
                ('name', models.CharField(max_length=384, db_column=b'Name', blank=True)),
                ('lastlogindate', models.DateTimeField(db_column=b'LastLoginDate')),
                ('hash', models.CharField(max_length=384, db_column=b'Hash', blank=True)),
                ('authlevel', models.IntegerField(db_column=b'AuthLevel')),
            ],
            options={
                'db_table': 'tblUsers',
            },
            bases=(models.Model,),
        ),
    ]
