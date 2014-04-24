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

from form import RegistrationForm
import datetime
# Used to reverse url
from django.core.urlresolvers import reverse
# Used to send mail from within Django
from django.core.mail import send_mail

from django.http import HttpResponse, Http404, StreamingHttpResponse
from mimetypes import guess_type

from RemiScene.models import *
from RemiScene.forms import *

import sys

def my_login(request):
	context = {}
	if request.method == "GET":
		context['form'] = AuthenticationForm()
		return render(request, 'RemiScene/login.html',context)

	form = AuthenticationForm(request.POST)
	context['form'] = form
	if request.method == "POST":
		username = request.POST['username'];
		password = request.POST['password'];
		user = authenticate(username = username,
							password = password)
		if user is not None:
			if user.is_active:
				login(request,user)
				return redirect(reverse('home'))
			else:
				return render(request,'RemiScene/confirm_failed.html',{})
		else:
			context['error'] = 'Incorrect username and password'
			return render(request,'RemiScene/login.html',context);
	return render(request,'RemiScene/login.html',context)

def register(request):
	context = {}

	if request.method == "GET":
		context['form'] = RegistrationForm()
		return render(request,'RemiScene/register.html',context)

	form = RegistrationForm(request.POST)
	context['form'] = form
	if not form.is_valid():
		return render(request, 'RemiScene/register.html', context)
	new_user = User.objects.create_user(username=request.POST['email'],
									email=request.POST['email'],
									password=request.POST['password1'],
									first_name=request.POST['first'],
									last_name=request.POST['last'])

	new_user.is_active = False
	token = default_token_generator.make_token(new_user)
	new_user.save()
	profile = new_user.get_profile()
	profile.token = token
	profile.save()
	email_body = """
Welcome to the Simple RemiScene. Pleas click the link below to
verfiy your email address and complete the registration of
your account:

http://%s%s
	"""% (request.get_host(),
		  reverse('confirm',args = (new_user.username,token)))
	send_mail(subject='verify',
			  message=email_body,
			  from_email='chongyur@andrew.cmu.edu',
			  recipient_list=[new_user.username])
	
	return render(request,'RemiScene/need_confirm.html',{})

def confirm(request,email,token):
	
	try:
		user = User.objects.get(username=email)
	except:
		return render(request,'RemiScene/confirm_failded.html',{})
	if token == user.get_profile().token:
		user.is_active = True
		user.save()
		return render(request,'RemiScene/confirm_successed.html',{})
	else:
		return render(request,'RemiScene/confirm_failded.html',{})


def test(request):
	return render(request,'RemiScene/scene.html',{})

def edit_person_scene(request,id):
	person_scene = get_object_or_404(PersonScene,user=request.user,id=id)
	#person_scene = PersonScene()
	
	if request.method == "GET":
		form = PersonSceneForm(instance=person_scene)
		context = {"form":form,"id":id}
		return render(request,"RemiScene/edit_person_scene.html",context)

	form = PersonSceneForm(request.POST,request.FILES,instance=person_scene)

	if not form.is_valid():
		context = {"form":form,"id":id}
		return render(request,"RemiScene/edit_person_scene.html",context)
	form.save()
	person_scene.save()
	if 'photo' in request.FILES:
		photos = request.FILES.getlist('photo')
		person_scene.photo_num = person_scene.photo_num+len(photos)
		person_scene.save()
		for photo in photos:
			print(photo)
			newPhoto = PersonScene_photo(person_scene=person_scene,photo=photo)
			newPhoto.save()
	scene_id = int(person_scene.scene.id)

	return redirect(reverse('RemiScene.scene_view.home',args=(scene_id,)))

#type: 0,profile  1,scene  2,personScene
def get_photo(request,username,id,type):
	try:
		#
		type = int(type)

		#profile id photo
		if type == 0:
			user = User.objects.get(username=username)
			profile = user.get_profile()
			'''
			if not profile.id_photo:
				content_type=guess_type('default.png')
				return HttpResponse(,mimetype=content_type)
				'''
			content_type = guess_type(profile.id_photo.name)
			return HttpResponse(profile.id_photo,mimetype=content_type)
		# scene pic (background)
		elif type == 1:
			scene = Scene.objects.get(id=id)
			print(scene.image_loc)
			if not scene.image_loc:
				return HttpResponse("error1")
				#content_type=guess_type('')
				#return HttpResponse('image/',mimetype=content_type)
			content_type = guess_type(scene.image_loc.name)
			return HttpResponse(scene.image_loc,mimetype=content_type)
		# person scene photo
		elif type == 2:
			personScene = PersonScene.objects.get(id=id)
			photos = PersonScene_photo.objects.filter(person_scene=personScene).order_by("id")
			
			content_type = guess_type(personScene.photo_loc.name)
			return HttpResponse(personScene.photo_loc,content_type=content_type)

		# profile backgournd photo 
		elif type == 3:
			user = User.objects.get(username=username)
			profile = user.get_profile()
			content_type = guess_type(profile.bg_pic.name)
			return HttpResponse(profile.bg_pic,content_type=content_type)


	except:
		return HttpResponse("error-1")

#type: 2 left, 1 right, 0 current
def get_person_scene_photo(request,id,index,type):
	try:
		index = int(index)
		id = int(id)
		type = int(type)
		personScene = PersonScene.objects.get(id=id)
		print(1)
		photos = PersonScene_photo.objects.filter(person_scene=personScene)
		print(2)
		print(len(photos))
		if len(photos) == 0 or index < 0 or index >= len(photos):
			return HttpResponse("")

		print(3)
		'''
		if index == 0:
			print(3)
			photo = photos[0]
			if photo == None:
				print('rcy')
			print(4)
		'''
		if type == 0:
			print("type = 0")
			photo = photos[index]
		elif type == 1:
			print("type = 1")
			if index == len(photos)-1:
				index = 0
			else:
				index = index + 1
			photo = photos[index]
		elif type == 2:
			print("type = 2")
			if index == 0:
				index = len(photos)-1
			else:
				index = index-1
			photo = photos[index]
		print(5)
		print(photo.photo)
		content_type = guess_type(photo.photo.name)
		print(6)
		return HttpResponse(photo.photo,content_type=content_type)
	except:
		return HttpResponse("error")

def get_music(request,username,id,type):
	try:
		type = int(type)
		if type == 0:
			user = User.objects.get(username=username)
			profile = user.get_profile()
			return StreamingHttpResponse(profile.music_id,content_type='audio/mp3')

		elif type == 1:
			scene = Scene.objects.get(id=id)
			content_type = guess_type()

		elif type == 2:
			personScene = PersonScene.objects.get(id=id)
			
			#content_type = guess_type(personScene.music_loc)
			print(personScene.music_loc)
			return HttpResponse(personScene.music_loc,content_type='audio/mp3')
	except:
		e = sys.exc_info()
		print(e)
		return HttpResponse("error-1")

@login_required
def edit_profile(request):
	profile = request.user.get_profile()
	#person_scene = PersonScene()
	
	if request.method == "GET":
		form = ProfileForm(instance=profile)
		context = {"form":form}
		return render(request,"RemiScene/edit_profile.html",context)

	form = ProfileForm(request.POST,request.FILES,instance=profile)

	if not form.is_valid():
		context = {"form":form}
		return render(request,"RemiScene/edit_profile.html",context)
	form.save()
	profile.save()
	return redirect(reverse('home'))

@login_required
def delete_message(request,id):
	message = Message.objects.get(id=id)
	if message.is_viewed:
		message.delete()
	else:
		from_user = message.from_user
		to_user = message.to_user
		if len(Friends.objects.filter(user=to_user,friend_id=from_user.id)) > 0:
			friendship = Friends.objects.get(user=to_user,friend_id=from_user.id)
			friendship.delete()
		if len(Friends.objects.filter(user=from_user,friend_id=to_user.id)) > 0:
			friendship = Friends.objects.get(user=from_user,friend_id=to_user.id)
			friendship.delete()
		content = to_user.first_name+" "+to_user.last_name+" declined your request."
		new_message = Message(from_user=to_user,to_user=from_user,is_viewed=True,content=content,create_time=datetime.now())
		new_message.save()
		message.delete()
	return redirect(reverse('message'))