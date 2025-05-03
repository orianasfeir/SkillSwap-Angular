from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'swap-requests', views.SkillSwapRequestViewSet, basename='swap-request')

app_name = 'swaps'

urlpatterns = [
    path('api/', include(router.urls)),
    # Keep old URLs for reference during Angular development
    path('', views.swap_requests, name='swap_list'),
    path('create/<int:user_id>/<int:skill_id>/', views.create_swap_request, name='create_swap'),
    path('accept/<int:swap_id>/', views.accept_swap, name='accept_swap'),
    path('reject/<int:swap_id>/', views.reject_swap, name='reject_swap'),
    path('complete/<int:swap_id>/', views.complete_swap, name='complete_swap'),
    path('cancel/<int:swap_id>/', views.cancel_swap, name='cancel_swap'),
] 