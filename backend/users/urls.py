from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)

from .views import LogoutView

urlpatterns = [
    # Эндпойнт для получения пары токенов (access и refresh)
    path('api/token/', TokenObtainPairView.as_view(),
         name='token_obtain_pair'),

    # Эндпойнт для обновления access токена с использованием refresh токена
    path('api/token/refresh/', TokenRefreshView.as_view(),
         name='token_refresh'),

    # Эндпойнт для верификации access токена
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),

    # Эндпойнт для логаута, который может удалять токен из Redis
    path('api/logout/', LogoutView.as_view(), name='logout'),
]
