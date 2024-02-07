from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import NotificationViewSet, NotificationStatisticsView


router = DefaultRouter()
router.register(r'notifications' , NotificationViewSet, basename='notifications')


urlpatterns = [
    # path('notifications/', NotificationViewSet.as_view({'get': 'list'}),
    #      name='notification-list'),
    path('', include(router.urls)),
    path('notifications/statistics/', NotificationStatisticsView.as_view(),
         name='notification-statistics'),
]
