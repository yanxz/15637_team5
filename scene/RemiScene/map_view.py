from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import ObjectDoesNotExist

# Decorator to use built-in authentication system
from django.contrib.auth.decorators import login_required

# Used to create and manually log in a user
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.contrib.auth.tokens import *
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import *

from mimetypes import guess_type

from django.http import HttpResponse, Http404

from RemiScene.forms import *
from RemiScene.models import *

# Used to send mail from within Django
from django.core.mail import send_mail

# Used to reverse url
from django.core.urlresolvers import reverse

# User to combain queryset
from itertools import chain
from operator import attrgetter

from datetime import datetime, date, time
from mimetypes import guess_type
from itertools import chain

import re

@login_required
def home(request):
    users = [request.user]
    friends = Friends.get_friends(request.user)
    if len(friends) > 0:
        for friend in friends:
            if friend.is_active:
                users.append(User.objects.get(id=friend.friend_id))

    scene_set = []
    for user in users:
        person_scenes = PersonScene.get_personScenes_from_user(user)
        for s in person_scenes:
            scene_set.append(s.scene)
    time_dict = {}
    for scene in scene_set:
        time = str(scene.occur_time)
        time_dict[scene] = time[:10]
    return render(request, 'RemiScene/map.html', {'time' : time_dict})

@login_required
def select_tag(request):
    users = [request.user]
    friends = Friends.get_friends(request.user)
    if len(friends) > 0:
        for friend in friends:
            if friend.is_active:
                users.append(User.objects.get(id=friend.friend_id))

    scene_set = []
    for user in users:
        person_scenes = PersonScene.get_personScenes_from_user(user)
        for s in person_scenes:
            scene_set.append(s.scene)

    tag = request.POST["tag"]
    print tag

    time_dict = {}
    for scene in scene_set:
        if tag != "All":
            if scene.tag != str(tag):
                print scene.tag
                continue
        time = str(scene.occur_time)
        time_dict[scene] = time[:10]
    return render(request, 'RemiScene/map.html', {'time' : time_dict, 'selected_tag' : tag})

# register page.
@login_required
def plain_search(request):
    context = {}

    form = QueryForm(request.POST)
    context['form'] = form
    if not form.is_valid():
        return render(request, 'blog/register.html', context)

    scenes_results = []
    if request.POST['type'] == 'tag':
        scenes_results = Scene.objects.filter(request.POST['content'])
    elif request.POST['type'] == 'title':
        scenes_results = Scene.objects.filter(title__contains = request.POST['content'])
    else:
        user = User.objects.get(username = request.POST['content'])
        person_scenes = PersonScene.objects.filter(user = user)
        for person_scene in person_scenes:
            scenes_results.add(person_scene.scene)
    
    context['scenes'] = scenes
    return render(request, 'RemiScene/plain_search_result.html', context)