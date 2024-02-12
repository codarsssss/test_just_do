from django.urls import path, include
from djoser.views import UserViewSet
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)

from .views import LogoutView
router = DefaultRouter()
router.register(r'users', UserViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
    # Эндпойнт для получения пары токенов (access и refresh)
    # path('auth/', TokenObtainPairView.as_view(),
    #      name='token_obtain_pair'),
    #
    # # Эндпойнт для обновления access токена с использованием refresh токена
    # path('auth/refresh/', TokenRefreshView.as_view(),
    #      name='token_refresh'),
    #
    # # Эндпойнт для верификации access токена
    # path('auth/verify/', TokenVerifyView.as_view(), name='token_verify'),
    #
    # # Эндпойнт для логаута, который может удалять токен из Redis
    # path('auth/logout/', LogoutView.as_view(), name='logout'),
]
