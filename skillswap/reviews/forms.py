from django import forms
from .models import Review

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'text']
        widgets = {
            'rating': forms.NumberInput(attrs={
                'type': 'range',
                'min': '1',
                'max': '5',
                'step': '1',
                'class': 'form-range'
            }),
            'text': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': '3',
                'placeholder': 'Share your experience with this skill swap...'
            })
        } 