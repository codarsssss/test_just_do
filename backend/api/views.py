from rest_framework import status
from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Notification
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

    @action(methods=['get'], detail=False, permission_classes=[IsAuthenticated])
    def statistics(self, request, *args, **kwargs):
        user = request.user
        if user.is_staff:
            statistics = {
                'total_notifications': Notification.objects.count(),
            }
        else:
            user_notifications = Notification.objects.filter(author=user)
            statistics = {
                'total_notifications': user_notifications.count(),
            }

        return Response(statistics)
