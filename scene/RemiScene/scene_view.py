from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.db.models import Q

from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect

from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm

from RemiScene.models import *
#from RemiScene.forms import *

from django.core.mail import send_mail
from django.http import HttpResponse, Http404

from datetime import datetime, date, time
from mimetypes import guess_type

import string
import random

#@login_required
def home(request, scene_id):
    scene = Scene.objects.get(id = scene_id)
"""
    # check if this user could view this scene
    user_scenes = PersonScene.objects.filter(user = request.user)

    scene_ids = []
    for personscene in user_scenes:
        scene_ids.add(personscene.scene_id)
    scenes = Scene.objects.filter(id__in=scene_ids)

    if scene not in scenes:
        return redirect(reverse('not_authenticated'))
"""
# get all PersonScene objects
    person_scenes = PersonScene.objects.filter(scene = scene)
    comments = Comment.objects.filter(person_scene__in = person_scenes)
    comments_count = {}
    for comment in comments:
        if comment.person_scene in comments_count.keys():
            comments_count[comment.person_scene] = comments_count[comment.person_scene]+1
    	else:
            comments_count[comment.person_scene] = 1

    person_scenes = sorted(person_scenes, key = lambda x : comments_count.get(x, 0), reverse=True)

    context = {}
    context['person_scenes'] = person_scenes
    context['scene'] = scene
    return render(request, "RemiScene/testSceneHome.html", context)

#@login_required
def click_on_person(request, person_scene_id):
	person_scene = PersonScene.objects.get(id = person_scene_id)
	context = {'person_scene' : person_scene}
	return render(request, 
                "RemiScene/personscene.xml", 
                context, 
                content_type='application/xml')