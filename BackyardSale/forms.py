from django import forms
from DashBoard.models import NewUser
from django.contrib.auth.models import User


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    username = forms.CharField(max_length=50)
    email = forms.EmailField(max_length=100)
    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'first_name', 'last_name']

class updateUser(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    email = forms.EmailField(max_length=100)
    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)

    class Meta:
        model = User
        fields = ['password','email', 'first_name', 'last_name']

class PasswordForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['password']

class UserInfoForm(forms.ModelForm):
    PhoneNum = forms.CharField(max_length=15, widget=forms.NumberInput)
    Address = forms.CharField(max_length=500)

    class Meta:
        model = NewUser
        fields = ['Address', 'PhoneNum']
