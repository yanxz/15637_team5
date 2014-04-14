from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.db.models import Q

from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect

from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm

from django.core.mail import send_mail
from django.http import HttpResponse, Http404

from datetime import datetime, date, time
from mimetypes import guess_type

import string
import random

def home(request):
    return render(request, 'RemiScene/map.html')

# register page.
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