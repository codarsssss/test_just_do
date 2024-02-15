import json

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from rest_framework.generics import get_object_or_404

from .models import Notification, User


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

        # Принимаем WebSocket соединение
        await self.accept()
        # Если пользователь аутентифицирован, добавляем его в общую группу
        await self.channel_layer.group_add(
            f"user_{self.user.id}",
            self.channel_name
        )
        # Добавляем суперпользователей в отдельную группу для рассылки всем
        if self.user.is_superuser:
            await self.channel_layer.group_add("superusers",
                                               self.channel_name)

    async def disconnect(self, close_code):
        # При отключении удаляем пользователя из его группы уведомлений
        await self.channel_layer.group_discard(
            f"user_{self.user.id}",
            self.channel_name
        )
        # Удаляем суперпользователя из группы рассылки
        if self.user.is_superuser:
            await self.channel_layer.group_discard("superusers",
                                                   self.channel_name)

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
        recipient = text_data_json.get("recipient_id")
        message = text_data_json['message']
        status = text_data_json['status']
        notif_obj = await (database_sync_to_async
                           (Notification.objects.create)
                           (recipient=recipient, status=status,
                            message=message))

        if recipient:
            await self.send_message_to_user(recipient.id, notif_obj)
        else:
            await self.channel_layer.group_send(notif_obj)

    async def send_message_to_user(self, user_id, notif_obj):
        channel_name = f"user_{user_id}"
        await self.channel_layer.send(channel_name, notif_obj)

    # Обработчик отправки уведомления
    # async def send_notification(self, event):
    #     message = event['message']
    #     # Отправляем сообщение пользователю или группе
    #     await self.send(text_data=json.dumps({
    #         'message': message
    #     }))
