#!/usr/bin/env python
#
# -*- coding: utf_8 -*-

from django.db import models


class Clip(models.Model):
    '''Recorded clip elements.'''
    title = models.CharField('Name', help_text='Choose a name for clip', max_length=75)
    record_date = models.DateTimeField('Date recorded', help_text='Indicate date of recording')
    location = models.ManyToManyField('Location', help_text='Indicate location(s) represented in clip.')
    user = models.ForeignKey('User', editable=False,)
    tags = models.ManyToManyField('Tags')
    description = models.TextField('Description', help_text='Describe recording for searchable reference', null=True)
    
    name = models.FileField('Recording', help_text='Select recording file to upload', upload_to='recordings/%Y/%m/%d',)
    size = models.IntegerField('File size', editable=False,)
    length = models.IntegerField('File length', editable=False,)
    upload_date = models.DateTimeField('Date uploaded', auto_now=True, editable=False,)
    
    def __unicode__(self):
        '''Return name when unicode is requested.'''
        return u"%s" % self.filebits

class Location(models.Model):
    '''Recording locations.'''
    city = models.CharField('City', max_length=30)    
    
    def __unicode__(self):
        '''Return location when unicode is requested.'''
        return u"%s" % self.city

class User(models.Model):
    '''User information.'''
    name = models.CharField('Name', max_length=20,)
    
    def __unicode__(self):
        '''Return name when unicode is requested.'''
        return u"%s" % self.name

class Tags(models.Model):
    '''Tags to associate with clips.'''
    tagtext = models.CharField('Tag', max_length=50, unique=True,)
    
    def __unicode__(self):
        '''Return tag when unicode is requested.'''
        return u"%s" % self.tagtext