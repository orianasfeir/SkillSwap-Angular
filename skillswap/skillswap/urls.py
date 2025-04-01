from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from users import views as user_views
from skills import views as skill_views
from swaps import views as swap_views

urlpatterns = [
    path('admin/', admin.site.urls),
    
    path('accounts/login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('accounts/register/', user_views.register, name='register'),
    
    path('profile/', user_views.profile, name='profile'),
    path('profile/edit/', user_views.edit_profile, name='edit_profile'),
    path('profile/qualifications/add/', user_views.add_qualification, name='add_qualification'),
    
    path('skills/add/', skill_views.add_skill, name='add_skill'),

    path('swaps/', swap_views.swap_requests, name='swap_list'),
    path('swaps/create/<int:user_id>/<int:skill_id>/', swap_views.create_swap_request, name='create_swap_request'),
    path('swaps/accept/<int:swap_id>/', swap_views.accept_swap, name='accept_swap'),
    path('swaps/reject/<int:swap_id>/', swap_views.reject_swap, name='reject_swap'),
]