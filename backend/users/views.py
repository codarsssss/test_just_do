from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status

from .serializers import UserSerializer
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

User = get_user_model()
channel_layer = get_channel_layer()


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Фильтрация пользователей в зависимости от прав доступа
        if self.request.user.is_staff:
            return User.objects.all()
        else:
            return User.objects.filter(id=self.request.user.id)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        # Отправляем уведомление о новом пользователе через WebSocket-соединение
        async_to_sync(channel_layer.group_send)(
            'users',
            {
                'type': 'user.new',
                'message': f'New user: {serializer.data["username"]}'
            }
        )
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        # Отправляем уведомление об обновлении пользователя через WebSocket-соединение
        async_to_sync(channel_layer.group_send)(
            'users',
            {
                'type': 'user.updated',
                'message': f'User updated: {serializer.data["username"]}'
            }
        )
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        # Отправляем уведомление об удалении пользователя через WebSocket-соединение
        async_to_sync(channel_layer.group_send)(
            'users',
            {
                'type': 'user.deleted',
                'message': f'User deleted: {instance.username}'
            }
        )
        return Response(status=status.HTTP_204_NO_CONTENT)
