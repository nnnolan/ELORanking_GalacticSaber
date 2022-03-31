from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class RegistrationForm(UserCreationForm):
    emails = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ["username", "email", "phone", "password1", "password2"]