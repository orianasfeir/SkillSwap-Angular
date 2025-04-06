from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from users import views as user_views
from skills import views as skill_views
from swaps import views as swap_views

urlpatterns = [
    path('', skill_views.home, name='home'),
    path('admin/', admin.site.urls),
    
    path('accounts/login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('accounts/register/', user_views.register, name='register'),
    path('accounts/profile/', user_views.profile, name='profile'),
    path('accounts/profile/edit/', user_views.edit_profile, name='edit_profile'),
    path('accounts/profile/qualifications/add/', user_views.add_qualification, name='add_qualification'),
    
    path('accounts/password_reset/', auth_views.PasswordResetView.as_view(template_name='registration/password_reset_form.html'), name='password_reset'),
    path('accounts/password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html'), name='password_reset_done'),
    path('accounts/reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='registration/password_reset_confirm.html'), name='password_reset_confirm'),
    path('accounts/reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'), name='password_reset_complete'),
    
    path('users/', include(('users.urls', 'users'), namespace='users')),
    path('skills/', include(('skills.urls', 'skills'), namespace='skills')),
    
    path('skills/add/', skill_views.add_skill, name='add_skill'),

    path('swaps/', swap_views.swap_requests, name='swap_list'),
    path('swaps/create/<int:user_id>/<int:skill_id>/', swap_views.create_swap_request, name='create_swap_request'),
    path('swaps/accept/<int:swap_id>/', swap_views.accept_swap, name='accept_swap'),
    path('swaps/reject/<int:swap_id>/', swap_views.reject_swap, name='reject_swap'),
]