from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from .models import Notification
from .serializers import NotificationSerializer
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

class NotificationViewSet(ModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        data = request.data
        data['author'] = request.user.pk
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        # Отправляем уведомление через Redis Channels
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)('notifications', {
            'type': 'notification.send',
            'content': 'New notification!',})

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(methods=['get'], detail=False, permission_classes=[IsAuthenticated])
    async def statistics(self, request, *args, **kwargs):
        user = request.user
        if user.is_staff:
            total_notifications = await Notification.objects.count()
        else:
            total_notifications = await Notification.objects.filter(author=user).count()

        return Response({'total_notifications': total_notifications})
