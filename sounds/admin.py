#!/usr/bin/env python
#
# -*- coding: utf_8 -*-

from sounds.models import *
from django.contrib import admin
from django.forms import ModelForm
from django import forms
import bleach


class ClipForm(ModelForm):
    '''Form for adding new clips based on model.'''
    class Meta:
        '''Build on clip model to create the form.'''
        model = Clip

    def bleachData(self, data, whitelist=[]):
        '''Clean data to ensure we have safe HTML to display.'''
        allowed = whitelist
        clean_data = bleach.clean(data, allowed)
    
        return clean_data	

    def clean_description(self):
        '''Do some custom cleaning/validation on the description.'''
        description = self.cleaned_data['description']
        whitelist = ['b', 'i']
        description = self.bleachData(description, whitelist)

        return description

    def clean(self):
        '''Custom cleaning to override specific fields.'''
        cleaned_data = super(ClipForm, self).clean()        
        self.cleaned_data['description'] = self.clean_description()

        return self.cleaned_data

class ClipAdmin(admin.ModelAdmin):
    '''Setup our clip views and custom form with the admin interface.'''
    list_display = ('title', 'upload_date',)
    search_fields = ['title', 'description',]
    list_filter = ['user', 'location', 'tags', 'upload_date']
    
    form = ClipForm
    fieldsets = [
        ('Recording', {'fields':['title', 'record_date', 'location', 'tags', 'description', 'name']})
    ]
    filter_horizontal = ('location', 'tags',)
 
admin.site.register(Clip, ClipAdmin)
admin.site.register(Location)
admin.site.register(Tags)