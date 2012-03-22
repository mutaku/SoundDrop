#!/usr/bin/env python
#
# -*- coding: utf_8 -*-

from django.db import models
from django.forms import ModelForm
from django import forms
import bleach

###################
# Database Models
###################

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
    
#####################
# Form from Models
#####################

class ClipForm(ModelForm):
    '''Form for adding new clips based on model.'''
    class Meta:
        '''Build on clip model to create the form.'''
        model = Clip
        fields = ('filebits', 'date', 'location', 'tags', 'description')

    taglist = forms.CharField(required=False, help_text='Insert a comma delimited list of descriptive terms for your item.')

    def bleachData(self, data, whitelist=[]):
        '''Clean data to ensure we have safe HTML to display.'''
        allowed = whitelist
        clean_data = bleach.clean(data, allowed)
    
        return clean_data	

    def fix_tags(self):
        '''Transform the taglist input into the tags array.'''
        pretags = self.cleaned_data['taglist']
        tagstring = bleach.clean(pretags)
        tags = []

        for tag in tagstring.split(","):
            tags.append(Tags.objects.get_or_create(tagtext=tag)[0].pk)

        return tags

    def clean_description(self):
        '''Do some custom cleaning/validation on the description.'''
        description = self.cleaned_data['description']
        whitelist = ['b', 'i']
        description = self.bleachData(description, whitelist)

        return description

    def clean_location(self):
        '''Clean the location.'''
        location = self.cleaned_data['location']
        locaiton = self.bleachData(location)		

        return location


    def clean(self):
        '''Custom cleaning to override specific fields.'''
        super(PostForm, self).clean()
        self.cleaned_data['tags'] = self.fix_tags()
        
        # --> Hmm, may need to explicity run the description and location clean

        return self.cleaned_data