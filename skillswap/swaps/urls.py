from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'swaps', views.SkillSwapRequestViewSet, basename='swap')

urlpatterns = [
    path('', include(router.urls))
] 