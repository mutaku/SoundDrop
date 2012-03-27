#!/usr/bin/env python
#
# -*- coding: utf_8 -*-

from sounds.models import *
from django.contrib import admin
from django.forms import ModelForm
from django import forms
from django.contrib.auth.models import User
import bleach
import mutagen

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
        _content_types = ['audio']
        if hasattr(self.cleaned_data['name'], 'content_type') and self.cleaned_data['name'].content_type.split('/')[0] not in _content_types:
            raise forms.ValidationError("File not of audio type")
    
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

    def save_model(self, request, obj, form, change):
        '''Interupt save and take care of adding addition object details.'''
        
        obj.user = User.objects.get(username=request.user)
        obj.size = obj.name.size
        obj.save()
        # This part is not ideal, but we do this post save so we can grab the file after upload.
        _song = mutagen.File(obj.name.path)
        obj.length = _song.info.length
        obj.audio_type = _song._mimes[0]
        obj.save()
 
admin.site.register(Clip, ClipAdmin)
admin.site.register(Location)
admin.site.register(Tags)