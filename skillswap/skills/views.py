from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Skill
from .forms import AddSkillForm 
from reviews.models import Review

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

def home(request):
    # Get recent skills instead of featured skills
    recent_skills = Skill.objects.order_by('-created_at')[:3]
    
    # Get recent reviews without profile relationship
    recent_reviews = Review.objects.select_related('reviewer').order_by('-created_at')[:3]
    
    context = {
        'featured_skills': recent_skills,  # Using recent skills as featured for now
        'recent_reviews': recent_reviews,
    }
    return render(request, 'home.html', context)