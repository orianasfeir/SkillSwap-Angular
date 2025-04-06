from django.shortcuts import render, redirect, get_object_or_404
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

@login_required
def browse_skills(request):
    skills = Skill.objects.all().order_by('-created_at')
    context = {
        'skills': skills,
    }
    return render(request, 'skills/browse_skills.html', context)

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

@login_required
def edit_skill(request, skill_id):
    skill = get_object_or_404(Skill, id=skill_id)
    
    if request.method == 'POST':
        form = AddSkillForm(request.user, request.POST, instance=skill)
        if form.is_valid():
            form.save()
            messages.success(request, f'Skill "{skill.name}" updated successfully.')
            return redirect('skills:browse_skills')
    else:
        form = AddSkillForm(request.user, instance=skill)
    
    return render(request, 'skills/edit_skill.html', {
        'form': form,
        'skill': skill
    })

@login_required
def delete_skill(request, skill_id):
    """Delete a skill after confirmation."""
    skill = get_object_or_404(Skill, id=skill_id)
    
    if request.method == 'POST':
        skill_name = skill.name
        skill.delete()
        messages.success(request, f'Skill "{skill_name}" deleted successfully.')
        return redirect('skills:browse_skills')
    
    return render(request, 'skills/delete_skill.html', {
        'skill': skill
    })