from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter
from users import views as user_views
from skills import views as skill_views
from swaps import views as swap_views

# Create a router and register our viewsets with it
router = DefaultRouter()
router.register(r'users', user_views.UserViewSet)
router.register(r'qualifications', user_views.QualificationViewSet, basename='qualification')
router.register(r'skills', skill_views.SkillViewSet)
router.register(r'user-skills', skill_views.UserSkillViewSet, basename='user-skill')

urlpatterns = [
    # API endpoints
    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls')),
    
    # Admin
    path('admin/', admin.site.urls),
    
    # Authentication
    path('accounts/login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(template_name='registration/logged_out.html'), name='logout'),
    path('accounts/register/', user_views.register, name='register'),
    path('accounts/profile/', user_views.profile, name='profile'),
    path('accounts/profile/edit/', user_views.edit_profile, name='edit_profile'),
    path('accounts/profile/qualifications/add/', user_views.add_qualification, name='add_qualification'),
    
    # Password reset
    path('accounts/password_reset/', auth_views.PasswordResetView.as_view(template_name='registration/password_reset_form.html'), name='password_reset'),
    path('accounts/password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html'), name='password_reset_done'),
    path('accounts/reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='registration/password_reset_confirm.html'), name='password_reset_confirm'),
    path('accounts/reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'), name='password_reset_complete'),
    
    # App URLs (keeping for reference during Angular development)
    path('users/', include(('users.urls', 'users'), namespace='users')),
    path('skills/', include(('skills.urls', 'skills'), namespace='skills')),
    path('swaps/', include(('swaps.urls', 'swaps'), namespace='swaps')),
    path('reviews/', include(('reviews.urls', 'reviews'), namespace='reviews')),
    
    path('skills/add/', skill_views.add_skill, name='add_skill'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)