
from django import forms
from django.contrib.auth.models import User
from adstool import models

class AdsForm(forms.ModelForm):
	class Meta:
		model = models.Ads
		fields = ['user','name',"description",'template','info']
