from django.urls import path
from . import views

app_name = 'skills'

urlpatterns = [
    path('browse/', views.browse_skills, name='browse_skills'),
    path('add/', views.add_skill, name='add_skill'),
    path('<int:skill_id>/edit/', views.edit_skill, name='edit_skill'),
    path('<int:skill_id>/delete/', views.delete_skill, name='delete_skill'),
] 