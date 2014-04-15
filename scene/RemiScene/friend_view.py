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
def home(request, userid):
	user = User.objects.get(id=userid)

	friends = Friends.objects.filter(user=user)
	if len(friends) == 0 or request.user not in friends[0].friends.all():
		return render(request, 'RemiScene/not_a_friend.html', {'user' : user})

	friends = Friends.get_friends(user)
	profile = user.get_profile()
	scene_set = []
	person_scenes = PersonScene.get_personScenes_from_user(user)
	for s in person_scenes:
		scene_set.append(s.scene)
	print scene_set
	context = {'user':user,
		'logged_user':request.user,
		'profile':profile,
		'scenes':scene_set,
		'friends':friends}

	return render(request, 'RemiScene/home.html',context)

@login_required
def search_friend(request):
	context = {}
	user = request.user

	if request.method == 'GET':
		friendships = Friends.get_friends(user)
		friends = []
		if len(friendships) > 0:
			friends = friendships[0].friends.all()
		return render(request, "RemiScene/search_friends.html", {'result_users': friends, 'user': request.user})

	name = request.POST["name"]

	users_group1 = User.objects.filter(first_name__contains=name)
	users_group2 = User.objects.filter(last_name__contains=name)
	temp_list = list(chain(users_group1, users_group2))

	result_list = []
	friends = Friends.get_friends(user)
	for user in temp_list:
		if user in friends:
			result_list.add(user)

	context = {'result_users': result_list, 'user': request.user}
	return render(request, "RemiScene/search_friends.html", context)