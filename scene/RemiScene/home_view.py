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

@login_required
def home(request):
    return render(request,'RemiScene/home.html')
    '''
    user = request.user
    friends = Friends.get_friends(user)
    profile = user.get_profile()
    messages = Message.get_messages(user)
    scene_set = []
    person_scenes = PersonScene.get_personScenes_from_user(user)
    for s in person_scenes:
        scene_set.append(s.scene)
    context = {'user':user,
            'profile':profile,
            'scenes':scene_set,
            'friends':friends,
            'messages':messages}
            
    return render(request, 'blog/home.html',context)
    '''
'''
@transaction.atomic
def register(request)
'''

def manage_scene_create(request):
    context = {'form':SceneForm()}
    return render(request, 'RemiScene/create_scene.html', context)

