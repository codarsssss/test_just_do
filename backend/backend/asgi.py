import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import api.routing  # Импортируем маршруты WebSocket из вашего приложения

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')

# Получаем обычное приложение Django
django_application = get_asgi_application()

# Определяем маршрутизатор протоколов для обработки HTTP и WebSocket запросов
application = ProtocolTypeRouter({
    "http": django_application,
    "websocket": AuthMiddlewareStack(
        URLRouter(
            api.routing.websocket_urlpatterns  # Подключаем маршруты WebSocket
        )
    ),
})
