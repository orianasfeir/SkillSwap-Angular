from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'reviews', views.ReviewViewSet, basename='review')

app_name = 'reviews'

urlpatterns = [
    path('api/', include(router.urls)),
    # Keep old URLs for reference during Angular development
    path('create/<int:swap_id>/', views.create_review, name='create_review'),
    path('user/<int:user_id>/', views.user_reviews, name='user_reviews'),
] 