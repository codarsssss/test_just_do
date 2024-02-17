from django.urls import path, include
from djoser.views import UserViewSet
from rest_framework.routers import DefaultRouter
from .views import CustomTokenObtainPairView

router = DefaultRouter()
router.register(r'users', UserViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('auth/jwt/create/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),  # Заменяем стандартный маршрут на кастомный
]