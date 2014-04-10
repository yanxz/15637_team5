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
				login(request.user)
				return redirect(reverse('home'))
			else:
				return render(request,'RemiScene/failed_to_confirm.html',{})
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
	new_user.email = token
	email_body = """
Welcome to the Simple Blog. Pleas click the link below to
verfiy your email address and complete the registration of
your account:

http://%s%s
	"""% (request.get_host(),
		  reverse('confirm',args = (new_user.username,token)))
	send_mail(subject='verify',
			  message=email_body,
			  from_email='chongyur@andrew.cmu.edu',
			  recipient_list=[new_user.username])
	new_user.save()
	new_user.get_profile().save()
	return render(request,'blog/need_confirm.html',{})