from django import forms
from django.contrib.auth.forms import UserCreationForm
from userauths.models import User, Profile

class UserRegisterForm(UserCreationForm):

    full_name = forms.CharField(label='Full Name', widget=forms.TextInput(attrs={'placeholder':"Enter full name",'class':"fullname"}))
    username = forms.CharField(label='Username',widget=forms.TextInput(attrs={'placeholder':"Enter username",'class':"username"}))
    email = forms.CharField(label='Email',widget=forms.TextInput(attrs={'placeholder':"Enter email",'class':"email"}))
    phone = forms.CharField(label='Phone Number',widget=forms.TextInput(attrs={'placeholder':"Enter phone number",'class':"phone"}))
    password1 = forms.CharField(label='Password',widget=forms.TextInput(attrs={'placeholder':"Enter password",'class':"password"}))
    password2 = forms.CharField(label='Confirm Password',widget=forms.TextInput(attrs={'placeholder':"Enter confirm password",'class':"password"}))
    class Meta:
        model = User 
        fields = ['full_name', 'username', 'email','phone', 'password1', 'password2']  

