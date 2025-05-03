from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'qualifications', views.QualificationViewSet, basename='qualification')

app_name = 'users'

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/login/', views.login_api, name='login_api'),
    # Keep old URLs for reference during Angular development
    path('dashboard/', views.dashboard, name='dashboard'),
    path('profile/', views.profile, name='profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('qualifications/add/', views.add_qualification, name='add_qualification'),
]