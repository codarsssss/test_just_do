from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth.models import User
import json


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
        if self.user.is_authenticated:
            # Принимаем WebSocket соединение
            await self.accept()
            # Если пользователь аутентифицирован, добавляем его в общею группу
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
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        recipient_id = text_data_json.get('recipient_id')
        if self.user.is_superuser:
            # Если суперпользователь, обрабатываем команду на отправку
            if recipient_id:
                # Отправка сообщения конкретному пользователю
                await self.channel_layer.group_send(
                    f"user_{recipient_id}",
                    {
                        "type": "send_notification",
                        "message": message,
                    }
                )
            else:
                # Отправка сообщения всем пользователям
                await self.channel_layer.group_send(
                    "superusers",
                    {
                        "type": "send_notification",
                        "message": message,
                    }
                )

    # Обработчик отправки уведомления
    async def send_notification(self, event):
        message = event['message']
        # Отправляем сообщение пользователю или группе
        await self.send(text_data=json.dumps({
            'message': message
        }))
