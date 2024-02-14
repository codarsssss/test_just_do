import os
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')

application = get_asgi_application()


from api.middleware import JWTAuthMiddleware
import api.routing

application = ProtocolTypeRouter({
    'http': application,
    'websocket': AllowedHostsOriginValidator(
        AuthMiddlewareStack(JWTAuthMiddleware(URLRouter(api.routing.websocket_urlpatterns)))
    ),
})
