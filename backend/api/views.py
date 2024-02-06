# views.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from .models import Notification
from .serializers import NotificationSerializer


class NotificationListView(APIView):
    permission_classes = [IsAdminUser | IsAuthenticated]

    def get(self, request):
        user = request.user
        if user.is_staff:  # Для администраторов
            notifications = Notification.objects.all()
        else:  # Для обычных пользователей
            notifications = Notification.objects.filter(author=user)

        serializer = NotificationSerializer(notifications, many=True)
        return Response(serializer.data)


class NotificationStatisticsView(APIView):
    permission_classes = [IsAdminUser | IsAuthenticated]

    def get(self, request):
        user = request.user
        if user.is_staff:  # Для администраторов
            # Реализация статистики по всем уведомлениям
            statistics = {
                'total_notifications': Notification.objects.count(),
                # Другие статистические данные
            }
        else:  # Для обычных пользователей
            # Реализация статистики по уведомлениям пользователя
            user_notifications = Notification.objects.filter(author=user)
            statistics = {
                'total_notifications': user_notifications.count(),
                # Другие статистические данные
            }

        return Response(statistics)
