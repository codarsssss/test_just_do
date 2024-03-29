from django.contrib import admin
from django.urls import path, include, re_path
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


schema_view = get_schema_view(
   openapi.Info(
      title="Notification API",
      default_version='v1',
      description="Документация проекта Notification",
      contact=openapi.Contact(email="codarsssss@yandex.ru"),
      license=openapi.License(name="BSD License"),
   ), public=True)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('users.urls')),
    path('api/', include('api.urls')),
]

urlpatterns += [
   re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0),
           name='schema-swagger-ui'),
]
