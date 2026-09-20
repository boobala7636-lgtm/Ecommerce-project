from .models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms


class CustomUserForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Enter your Username', 'class' :'form-control'
    }))
    email = forms.EmailField(widget=forms.TextInput(attrs={
        'placeholder': 'Enter Your Email Address' , 'class':'form-control'
    }))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder':'Enter Your Password', 'class':'form-control'
    }))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder':'Enter Your Confirm Password', 'class':'form-control'
    }))

    class Meta:
        model = User
        # password1 and password2 are safely handled automatically outside this list. (just mention for development mode.)
        fields = ['username','email']  