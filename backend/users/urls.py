from django.urls import path, include
from rest_framework.routers import DefaultRouter

# from .views import UserViewSet


app_name = 'users'

router = DefaultRouter()
# router.register('users', UserViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('', include('djoser.urls')),
]
