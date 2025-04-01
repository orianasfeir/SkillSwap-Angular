from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Skill
from .forms import AddSkillForm 

@login_required
def add_skill(request):
    user = request.user
    available_skills = Skill.objects.exclude(users=user)
    
    if request.method == 'POST':
        form = AddSkillForm(user, request.POST)
        if form.is_valid():
            skill = form.cleaned_data['skill']
            user.skills.add(skill)
            messages.success(request, f'Added skill: {skill.name}')
            return redirect('profile')
    else:
        form = AddSkillForm(user)
    
    return render(request, 'skills/add_skill.html', {
        'form': form,
        'available_skills': available_skills
    })