from django.contrib.auth.models import User
from django import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm

class CustomerUserForm(forms.ModelForm):
    class Meta:
        model=User
        # fields=['first_name','last_name','username','password']
        fields=['username','password']
        widgets = {
        'password': forms.PasswordInput()
        }

class contactusform(forms.ModelForm):
    class Meta:
        model=tblcontactus
        fields='__all__'