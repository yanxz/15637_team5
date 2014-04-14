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
    user = request.user
    friends = Friends.get_friends(user)
    profile = user.get_profile()
    messages = Message.get_messages(user)
    scene_set = []
    person_scenes = PersonScene.get_personScenes_from_user(user)
    for s in person_scenes:
        scene_set.append(s.scene)
    print scene_set
    context = {'user':user,
            'profile':profile,
            'scenes':scene_set,
            'friends':friends,
            'messages':messages}
            
    return render(request, 'RemiScene/home.html',context)

@login_required
def manage_scene_create(request):
    context = {'form':SceneForm()}
    return render(request, 'RemiScene/create_scene.html', context)

@login_required
def add_scene(request):
    new_Scene = Scene(create_time = datetime.now())
    form = SceneForm(request.POST, request.FILES, instance=new_Scene)

    if not form.is_valid():
        return redirect('create_scene')

    form.save()
    print("passed form validation!")
    friends = request.POST['friends']
    friends_list = re.compile(r',').split(friends)

    for friend_name in friends_list:
        friend_name = friend_name.strip();
        names= re.compile(r' ').split(friend_name, 2)
        user = User.objects.filter(first_name=names[0], last_name=names[1])
        if len(user) <= 0:
            continue

        new_person_scene = PersonScene(user=user[0], scene=new_Scene)
        new_person_scene.save()

    new_person_scene = PersonScene(user=request.user, scene=new_Scene)
    new_person_scene.save()
    return redirect(reverse('home'))

@login_required
def search_people(request):
    context = {}
    if request.method == 'GET':
        return render(request, "RemiScene/search_people.html", context)

    name = request.POST["name"]

    users_group1 = User.objects.filter(first_name__contains=name)
    users_group2 = User.objects.filter(last_name__contains=name)
    result_list = list(chain(users_group1, users_group2))
    print(result_list)
    context = {'result_users': result_list}
    return render(request, "RemiScene/search_people.html", context)

@login_required
def add_friend(request, userid):
    friend = User.objects.get(id=userid)

    user = Friends.objects.filter(user = request.user)
    if len(user) == 0:
        friendship = Friends(user = request.user)
        friendship.save()
    elif friend not in user[0].friends.all():
        user[0].friends.add(friend)
        user[0].save()

    message = 'You have successfully added '+ friend.first_name + " " + friend.last_name
    context = {'message': message}
    return render(request, "RemiScene/search_people.html", context)