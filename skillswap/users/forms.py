from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Qualification

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class ProfileEditForm(forms.ModelForm):
    profile_image = forms.ImageField(
        required=False,
        widget=forms.FileInput(attrs={'class': 'form-control'})
    )
    
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'phone', 'about', 'profile_image']
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'about': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }

class QualificationForm(forms.ModelForm):
    class Meta:
        model = Qualification
        fields = ['description']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }