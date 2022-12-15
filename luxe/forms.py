from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from phone_field import PhoneField

class RegisterForm(UserCreationForm):
    first_name = forms.CharField(max_length='50')
    last_name = forms.CharField(max_length='50')
    tel = PhoneField(blank=True, help_text='Contact phone number')
    email = forms.EmailField()

    class Meta:
        fields = ['username', 'first_name', 'last_name', 'tel', 'email', 'password1', 'password2']