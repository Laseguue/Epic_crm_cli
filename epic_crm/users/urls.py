from django.urls import path
from .views import UserViewSet, logout, current_user

urlpatterns = [
    path('users/', UserViewSet.as_view({'get': 'list', 'post': 'create'}), name='user-list'),
    path('users/<int:pk>/', UserViewSet.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'}), name='user-detail'),
    path('logout/', logout, name='logout'),
    path('me/', current_user, name='current-user'),
]
