from django import forms
from .models import Skill, UserSkill
from users.models import Qualification

class QualificationForm(forms.ModelForm):
    class Meta:
        model = Qualification
        fields = ['qualification_image', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }

class AddSkillForm(forms.ModelForm):
    class Meta:
        model = UserSkill
        fields = ['skill', 'proficiency_level']
        widgets = {
            'proficiency_level': forms.NumberInput(attrs={'min': 1, 'max': 5}),
        }

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user
        # Exclude skills the user already has
        existing_skills = UserSkill.objects.filter(user=user).values_list('skill_id', flat=True)
        self.fields['skill'].queryset = Skill.objects.exclude(id__in=existing_skills)