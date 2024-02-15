from django.db.models import Q, Count
from rest_framework import permissions, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated

from .models import Notification
from .serializers import NotificationSerializer


class NotificationViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        notifications = Notification.objects.filter(
            Q(recipient=self.request.user) | Q(recipient=None)
        )
        return notifications

    def get_serializer_context(self):
        notification_statistics = self.queryset.values('type').annotate(count=Count('type'))
        return {'notification_statistics': notification_statistics}

