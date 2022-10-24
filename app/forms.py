from dataclasses import fields
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from app import models
# from django.core import validators
# import urllib.request
# Create your forms here.

class NewUserForm(UserCreationForm):
	email = forms.EmailField(required=True)

	class Meta:
		model = User
		fields = ("username", "email", "password1", "password2")

	def save(self, commit=True):
		user = super(NewUserForm, self).save(commit=False)
		user.email = self.cleaned_data['email']
		if commit:
			user.save()
		return user

class CompaignUploadForm(forms.ModelForm):
	class Meta:
		model = models.CompaignUpload
		fields = '__all__' 
	
# 	def clean_Url(self):
# 		try:
# 			urllib.request.urlopen(self.cleaned_data['Url']).getcode()
# 		except:
# 			raise forms.ValidationError('Invalid URL')
# 		return self.cleaned_data['Url']

# class CampaignForm(forms.ModelForm):
# 	class Meta:
# 		model = models.Campaign
# 		fields = ['user','Name','AdFile']

class ContactForm(forms.ModelForm):
	class Meta:
		model = models.Contact
		fields = "__all__"