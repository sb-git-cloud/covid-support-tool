from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField()
    institution = forms.CharField(required=False, max_length=180)
    # lastname = forms.CharField(max_length=180)
    # firstname = forms.CharField(max_length=180)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'institution', 'password1', 'password2']