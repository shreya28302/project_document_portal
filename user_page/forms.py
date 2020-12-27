from django import forms
from django.contrib.auth.models import User
from . import models

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = models.UserProfile
        fields = ['phone_no', 'first_name', 'last_name', 'image']

class SearchForm(forms.Form):
    searchuser = forms.CharField(label='search for a user', max_length=200)
