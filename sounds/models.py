#!/usr/bin/env python
#
# -*- coding: utf_8 -*-

from django.db import models


class Clip(models.Model):
    '''Recorded clip elements.'''
    filebits = models.ForeignKey('FileElement')
    date = models.DateTimeField('Date uploaded', auto_now=True,)
    location = models.ForeignKey('Location')
    user = models.ForeignKey('User')
    tags = models.ManyToManyField('Tags')
    description = models.TextField('Description')
    
    def __unicode__(self):
        '''Return name when unicode is requested.'''
        return u"%s" % self.filebits

class FileElement(models.Model):
    '''Physical file container.'''
    name = models.FileField('File name', upload_to='recordings/%Y/%m/%d',)
    size = models.IntegerField('File size')
    length = models.IntegerField('File length')
    
    def __unicode__(self):
        '''Return file name when unicode is requested.'''
        return u"%s" % self.name

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