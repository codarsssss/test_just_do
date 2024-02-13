from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import AccessToken
from channels.db import database_sync_to_async
import logging


User = get_user_model()


@database_sync_to_async
def get_user(user_id):
    try:
        return User.objects.get(id=user_id)
    except User.DoesNotExist:
        return AnonymousUser()


class JWTAuthMiddleware:
    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        cookies = scope.get('cookies', {})
        token = cookies.get('jwt')

        try:
            access_token = AccessToken(token)
            access_token.verify()
            user_id = access_token.payload.get('user_id')
            scope['user'] = await get_user(user_id=user_id)
        except TokenError as error:
            logging.error(error)
        finally:
            return await self.app(scope, receive, send)
