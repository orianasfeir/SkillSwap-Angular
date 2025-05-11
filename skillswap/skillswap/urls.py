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
    path('api/', include('swaps.urls')),  # Include swaps app URLs
    path('api/', include('reviews.urls')),  # Include reviews app URLs
    path('api-auth/', include('rest_framework.urls')),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/login/', user_views.login_api, name='api_login'),
    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)