#!/usr/bin/env python
#
# -*- coding: utf_8 -*-

from django.shortcuts import get_object_or_404,get_list_or_404,render_to_response,redirect
from sounds.models import *

def main(request):
    sound_clips = Clip.objects.all().order_by('-id')
    return render_to_response('index.html',{'clips': sound_clips,})
