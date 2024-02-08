from channels.generic.websocket import AsyncWebsocketConsumer
import json

class UserConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add(
            'users',  # Название канала, к которому подключаемся
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            'users',  # Название канала, из которого отключаемся
            self.channel_name
        )

    async def receive(self, text_data):
        # Обработка полученных данных
        pass

    async def user_message(self, event):
        message = event['message']

        # Отправляем сообщение обратно клиенту
        await self.send(text_data=json.dumps({
            'type': 'user_message',
            'message': message
        }))
