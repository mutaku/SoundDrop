#!/usr/bin/env python
#
# -*- coding: utf_8 -*-

from sounddrop.models import *
from django.contrib import admin
from django.forms import ModelForm
from django import forms
import bleach


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
        location = self.bleachData(location)		

        return location


    def clean(self):
        '''Custom cleaning to override specific fields.'''
        super(PostForm, self).clean()
        self.cleaned_data['tags'] = self.fix_tags()
        
        # --> Hmm, may need to explicity run the description and location clean

        return self.cleaned_data

class ClipAdmin(admin.ModelAdmin):
    '''Setup our custom form with the admin interface.''' 
    form = ClipForm
 
admin.site.register(Clip, ClipAdmin)