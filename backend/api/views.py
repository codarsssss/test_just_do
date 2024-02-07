# views.py
from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from .models import Notification, User
from .serializers import NotificationSerializer


class NotificationViewSet(ModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return Notification.objects.all()
        else:
            return user.notifications.all()

    def create(self, request, *args, **kwargs):
        data = request.data
        data['author'] = request.user.pk
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


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
