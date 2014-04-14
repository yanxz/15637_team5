from django import forms
from django.contrib.auth.models import User
from models import *

class RegistrationForm(forms.Form):
	email = forms.EmailField(max_length = 200,
								label='E-mail')
	first = forms.CharField(max_length = 200,
								label = 'First Name',
								required = False)
	last = forms.CharField(max_length = 200,
								label = 'Last Name',
								required = False)
	password1 = forms.CharField(max_length = 200, 
								label='Password', 
								widget = forms.PasswordInput())
	password2 = forms.CharField(max_length = 200, 
								label='Confirm password',  
								widget = forms.PasswordInput())

	# Customizes form validation for properties that apply to more
	# than one field.  Overrides the forms.Form.clean function.
	def clean(self):
		# Calls our parent (forms.Form) .clean function, gets a dictionary
		# of cleaned data as a result
		cleaned_data = super(RegistrationForm, self).clean()

		# Confirms that the two password fields match
		password1 = cleaned_data.get('password1')
		password2 = cleaned_data.get('password2')
		if password1 and password2 and password1 != password2:
			raise forms.ValidationError("Passwords did not match.")

		# We must return the cleaned data we got from our parent.
		return cleaned_data


	# Customizes form validation for the email field.
	def clean_email(self):
		# Confirms that the email is not already present in the
		# User model database.
		email = self.cleaned_data.get('email')
		if User.objects.filter(username=email):
			raise forms.ValidationError("email is already taken.")

		# We must return the cleaned data we got from the cleaned_data
		# dictionary
		return email

class SceneForm(forms.ModelForm):
	class Meta:
		model = Scene
		exclude = ('create_time',)
		widgets = {
			'title': forms.TextInput(attrs={'class': 'input-block-level'}),
			'description': forms.Textarea(attrs={'class': 'span6 text', 'cols': 60}),
			'occur_time': forms.DateInput(attrs={'class': ''}),
			'tag': forms.Select(attrs={'class': ''}),
			'location': forms.TextInput(attrs={'class': ''}),
			'image_loc': forms.FileInput(attrs={'class': 'btn'})
		}

class PersonSceneForm(forms.ModelForm):
	class Meta:
		model = PersonScene
		exclude = {'scene','user',}
		widgets = {
			'essay' : forms.Textarea(),
			'video_loc' : forms.FileInput(),
			'music_loc' : forms.FileInput(),
			'photo_loc' : forms.FileInput()
		}
