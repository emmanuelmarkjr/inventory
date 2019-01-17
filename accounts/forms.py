from django.contrib.auth.forms import AuthenticationForm
from django import forms
from accounts.models import UserProfile
import fileinput


class LoginForm(AuthenticationForm):
    username = forms.CharField(max_length=30,
                               widget=forms.TextInput(attrs={'class': 'form-control', 'name': 'username',
                                                             'placeholder': ' Username'}))
    password = forms.CharField(max_length=30,
                               widget=forms.PasswordInput(attrs={'class': 'form-control', 'name': 'password',
                                                                 'placeholder': 'Password'}))


class ProfileForm(forms.ModelForm):

    picture = forms.ImageField(required=False, widget=forms.FileInput)

    class Meta:
        model = UserProfile
        fields = ('full_name', 'email', 'phone', 'address')
