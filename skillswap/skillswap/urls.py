from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter
from users import views as user_views
from skills import views as skill_views
from swaps import views as swap_views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

# Create a router and register our viewsets with it
router = DefaultRouter()
router.register(r'users', user_views.UserViewSet)
router.register(r'qualifications', user_views.QualificationViewSet, basename='qualification')

urlpatterns = [
    # API endpoints
    path('api/', include(router.urls)),
    path('api/', include('skills.urls')),  # Include skills app URLs
    path('api-auth/', include('rest_framework.urls')),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/login/', user_views.login_api, name='api_login'),
    
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
    path('swaps/', include(('swaps.urls', 'swaps'), namespace='swaps')),
    path('reviews/', include(('reviews.urls', 'reviews'), namespace='reviews')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)