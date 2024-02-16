import json
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer

from .models import Notification, User
from .serializers import NotificationSerializer
from .middleware import get_user


class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        '''
        При установке соединения пользователь добавляется в группу с именем,
         основанным на его id, чтобы отправлять уведомления этому пользователю.
         Если пользователь является суперпользователем, добавляется в
         группу "superusers", которая может быть использована для рассылки
         сообщений всем пользователям
         '''
        self.user = self.scope["user"]
        if not self.user.is_authenticated:
            return await self.close()

        await self.accept()

        await self.channel_layer.group_add(f"user_{self.user.id}",
                                           self.channel_name)
        await self.channel_layer.group_add(f"users", self.channel_name)

    async def disconnect(self, close_code):
        # При отключении удаляем пользователя из его группы уведомлений
        await self.channel_layer.group_discard(
            f"user_{self.user.id}",
            self.channel_name
        )
        await self.channel_layer.group_discard('users', self.channel_name)

    async def receive(self, text_data):
        '''
        Вызывается при получении сообщения от пользователя. Если пользователь
        является суперпользователем, он может отправлять сообщения всем
        пользователям или конкретному пользователю, указав recipient_id.
        Сообщение рассылается через группу Channels, используя метод group_send
        '''
        # Обработка входящих сообщений от пользователя
        if not self.user.is_superuser:
            return

        text_data_json = json.loads(text_data)
        recipient_id = text_data_json.get("recipient_id")

        recipient = None
        if recipient_id is not None:
            recipient: User = await get_user(recipient_id)
            if recipient.is_anonymous:
                return await self.send(json.dumps(
                    {'status': 'error', 'message': 'Unknown recipient_id'})
                )

        message = text_data_json['message']
        status = text_data_json['status']
        notif_obj = await (
            database_sync_to_async(Notification.objects.create)(
                recipient=recipient,
                status=status,
                message=message
            )
        )

        serializer = NotificationSerializer(notif_obj)
        json_data = serializer.data
        json_data['type'] = 'send.notification'

        if recipient_id is not None:
            await self.channel_layer.group_send(f"user_{recipient_id}", json_data)
        else:
            await self.channel_layer.group_send("users", json_data)

    async def send_notification(self, event):
        await self.send(json.dumps(event))
