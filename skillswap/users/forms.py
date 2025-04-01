from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Qualification

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email', 'phone', 'profile_image', 'about']

class QualificationForm(forms.ModelForm):
    class Meta:
        model = Qualification
        fields = ['qualification_image', 'description']