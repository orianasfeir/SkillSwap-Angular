from django import forms
from .models import Skill

class AddSkillForm(forms.Form):
    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['skill'] = forms.ModelChoiceField(
            queryset=Skill.objects.exclude(users=user),
            label="Select a skill to add"
        )