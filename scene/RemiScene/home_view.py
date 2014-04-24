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
    friendships = Friends.get_friends(user)
    profile = user.get_profile()
    messages = Message.get_messages(user)
    scene_set = []
    person_scenes = PersonScene.get_personScenes_from_user(user)
    for s in person_scenes:
        scene_set.append(s.scene)
    print scene_set
    friends = []
    for friend in friendships:
        if friend.is_active == False:
            continue
        friends.append(User.objects.get(id=friend.friend_id))
    context = {'user':user,
            'profile':profile,
            'scenes':scene_set,
            'friends':friends,
            'messages':messages}
            
    return render(request, 'RemiScene/home.html',context)

@login_required
def manage_scene_create(request):
    context = {'form':SceneForm()}
    friend_list = []
    friendships = Friends.objects.filter(user=request.user)
    for friendship in friendships:
        if friendship.is_active:
            friend_list.append(User.objects.get(id=friendship.friend_id))
    context['friends']=friend_list
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

    if len(friends) > 0:
        friends_list = re.compile(r',').split(friends)

        for friend_name in friends_list:
            friend_name = friend_name.strip();
            names= re.compile(r' ').split(friend_name, 2)
            user = User.objects.filter(first_name=names[0], last_name=names[1])
            if len(user) <= 0:
                continue

            if len(Friends.objects.filter(user=request.user,friend_id=user[0].id)) > 0:
                new_person_scene = PersonScene(user=user[0], scene=new_Scene)
                new_person_scene.save()

    new_person_scene = PersonScene(user=request.user, scene=new_Scene)
    new_person_scene.save()
    return redirect(reverse('home'))

@login_required
def search_people(request):
    context = {}
    if request.method == 'GET':
        return render(request, "RemiScene/search_people.html", {'user': request.user})

    name = request.POST["name"]
    if len(name) == 0:
        return render(request, "RemiScene/search_people.html", {'user': request.user})

    names = re.split('\W+', name)
    leng = len(names)
    if names[leng-1] == '':
        leng -= 1

    if leng >= 3:
        return render(request, "RemiScene/search_people.html", {'user': request.user})

    friends = Friends.get_friends(request.user)
    friends_acked = friends.filter(is_active=True)
    friends_id_list = friends.values_list('friend_id', flat=True)
    friends_acked_id_list = friends_acked.values_list('friend_id', flat=True)
    
    friend_group = []
    friend_acked_group = []

    if leng == 2:
        users_group = User.objects.filter(first_name__contains=names[0], last_name__contains=names[1]).exclude(id=request.user.id)
        
        for user in users_group:
            if user.id in friends_acked_id_list:
                friend_acked_group.append(user)
            elif user.id in friends_id_list:
                friend_group.append(user)
        context = {'result_users': users_group, 'friend_group':friend_group, 'friend_acked_group':friend_acked_group, 'user': request.user}
        return render(request, "RemiScene/search_people.html", context)

    result_list = set()
    users_group1 = User.objects.filter(first_name__contains=name).exclude(id=request.user.id)
    users_group2 = User.objects.filter(last_name__contains=name).exclude(id=request.user.id)
    
    for user in users_group1:
        result_list.add(user)
    for user in users_group2:
        result_list.add(user)

    for user in result_list:
        if user.id in friends_acked_id_list:
            friend_acked_group.append(user)
        elif user.id in friends_id_list:
            friend_group.append(user)
    context = {'result_users': result_list, 'friend_group':friend_group, 'friend_acked_group':friend_acked_group, 'user': request.user}
    return render(request, "RemiScene/search_people.html", context)

@login_required
def add_friend(request,userid):
    user = request.user
    friendships = Friends.objects.filter(user=user,friend_id=userid)
    if len(friendships) == 0: 
        friendship = Friends(user=request.user,friend_id=userid)
        friendship.save()

        friend = User.objects.get(id=userid)
        
        content = user.first_name+" "+user.last_name+" wants to add you as a friend."
        new_Message = Message(create_time=datetime.now(),content=content,from_user=user,to_user=friend)
        new_Message.save()
        add_friend_result = 'You have send a message to '+ friend.first_name + " " + friend.last_name
    else:
        friend = User.objects.get(id=userid)
        if friendships[0].is_active:
            add_friend_result = friend.first_name + " " + friend.last_name + ' is already your friend.'
        else:
            add_friend_result = friend.first_name + " " + friend.last_name + ' has not comfirm the request.'

    context = {'add_friend_result': add_friend_result}
    return render(request, "RemiScene/search_people.html", context)


'''
@login_required
def add_friend(request, userid):
    friend = User.objects.get(id=userid)
    print("friend's userid: " + str(userid))
    user = Friends.objects.filter(user = request.user)
    print("user's userid: " + str(request.user.id))
    if len(user) == 0:
        friendship = Friends(user = request.user)
        friendship.save()
        friendship.friends.add(friend)
        friendship.save()
    elif friend not in user[0].friends.all():
        user[0].friends.add(friend)
        user[0].save()

    # save a message into the system.
    content = "I have added you as a SceneFriend."
    add_friend_message = Message(create_time=datetime.now(), content=content, from_user=request.user, to_user=friend)
    add_friend_message.save()

    add_friend_result = 'You have successfully added '+ friend.first_name + " " + friend.last_name
    context = {'add_friend_result': add_friend_result}
    return render(request, "RemiScene/search_people.html", context)
'''
@login_required
def message(request):
    messages = Message.get_messages(request.user)
    context = {'messages' : messages}
    return render(request, "RemiScene/message.html", context)

@login_required
def confirm_message(request,id):
    message = Message.objects.get(id=id)
    if message.is_viewed:
        return redirect(reverse('message'))
    message.is_viewed = True
    message.save()
    to_user = message.to_user
    from_user = message.from_user
    content = to_user.first_name + " "+to_user.last_name + " has added you as a friend."
    new_message = Message(to_user=from_user,from_user=to_user,content=content,create_time=datetime.now(),is_viewed=True)
    new_message.save()
    new_friendship = Friends(user=to_user,friend_id=from_user.id,is_active=True)
    new_friendship.save()
    friendship = Friends.objects.get(user=from_user,friend_id=to_user.id)
    friendship.is_active = True
    friendship.save()
    return redirect(reverse('message'))

@login_required
def all_scenes(request):
    users = [request.user]
    friends = Friends.get_friends(request.user)
    if len(friends) > 0:
        '''
        for user in friends[0].friends.all():
            users.append(user)
        '''
        for friend in friends:
            if friend.is_active:
                users.append(User.objects.get(id=friend.friend_id))
            
    scene_set = []
    for user in users:
        person_scenes = PersonScene.get_personScenes_from_user(user)
        for ps in person_scenes:
            scene_set.append(ps.scene)

    scene_set = sorted(scene_set, key = lambda x : x.occur_time, reverse=True)
    return render(request, 'RemiScene/all_scenes.html', {'scenes' : scene_set})