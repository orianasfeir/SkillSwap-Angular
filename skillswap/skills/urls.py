from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'skills', views.SkillViewSet)
router.register(r'user-skills', views.UserSkillViewSet, basename='user-skill')

app_name = 'skills'

urlpatterns = [
    path('api/', include(router.urls)),
    # Keep old URLs for reference during Angular development
    path('browse/', views.browse_skills, name='browse_skills'),
    path('add/', views.add_skill, name='add_skill'),
    path('<int:skill_id>/', views.skill_detail, name='skill_detail'),
    path('<int:skill_id>/edit/', views.edit_skill, name='edit_skill'),
    path('<int:skill_id>/delete/', views.delete_skill, name='delete_skill'),
] 