from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Skill, UserSkill
from .forms import AddSkillForm, QualificationForm
from reviews.models import Review

@login_required
def add_skill(request):
    if request.method == 'POST':
        skill_form = AddSkillForm(request.user, request.POST)
        qualification_form = QualificationForm(request.POST, request.FILES)
        
        if skill_form.is_valid() and qualification_form.is_valid():
            # Create the user skill
            user_skill = skill_form.save(commit=False)
            user_skill.user = request.user
            user_skill.save()
            
            # Create and associate the qualification if provided
            if qualification_form.cleaned_data.get('qualification_image') or qualification_form.cleaned_data.get('description'):
                qualification = qualification_form.save(commit=False)
                qualification.user = request.user
                qualification.save()
                user_skill.qualifications.add(qualification)
            
            messages.success(request, 'Skill added successfully!')
            return redirect('skills:browse_skills')
    else:
        skill_form = AddSkillForm(request.user)
        qualification_form = QualificationForm()
    
    return render(request, 'skills/add_skill.html', {
        'skill_form': skill_form,
        'qualification_form': qualification_form,
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
    user_skill = get_object_or_404(UserSkill, id=skill_id, user=request.user)
    
    if request.method == 'POST':
        form = AddSkillForm(request.user, request.POST, instance=user_skill)
        if form.is_valid():
            form.save()
            messages.success(request, f'Skill "{user_skill.skill.name}" updated successfully.')
            return redirect('skills:browse_skills')
    else:
        form = AddSkillForm(request.user, instance=user_skill)
    
    return render(request, 'skills/edit_skill.html', {
        'form': form,
        'user_skill': user_skill
    })

@login_required
def delete_skill(request, skill_id):
    """Delete a user's skill after confirmation."""
    user_skill = get_object_or_404(UserSkill, id=skill_id, user=request.user)
    
    if request.method == 'POST':
        skill_name = user_skill.skill.name
        user_skill.delete()
        messages.success(request, f'Skill "{skill_name}" deleted successfully.')
        return redirect('users:dashboard')
    
    return redirect('users:dashboard')

@login_required
def skill_detail(request, skill_id):
    skill = get_object_or_404(Skill, id=skill_id)
    user_has_skill = UserSkill.objects.filter(user=request.user, skill=skill).exists()
    
    # Get all users offering this skill with their qualifications
    users_offering = UserSkill.objects.filter(
        skill=skill
    ).exclude(
        user=request.user  # Exclude current user
    ).select_related(
        'user'
    ).prefetch_related(
        'qualifications'
    )
    
    # Get reviews through swap requests where this skill was involved
    reviews = Review.objects.filter(
        swap_request__skill_requested=skill
    ).select_related('reviewer')
    
    context = {
        'skill': skill,
        'user_has_skill': user_has_skill,
        'users_offering': users_offering,
        'reviews': reviews,
    }
    return render(request, 'skills/skill_detail.html', context)