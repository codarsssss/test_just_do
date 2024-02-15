from django.utils import timezone
from datetime import timedelta
from django.db.models import Q, Count
from rest_framework import permissions, viewsets
from .utils import datetime_to_end_day, datatime_to_start_day

from .models import Notification
from .serializers import NotificationSerializer


class NotificationViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_filter_timestamp(self):
        timestamp = self.request.query_params['timestamp']
        user_datetime = timezone.localdate(
            timezone=self.request.query_params.get('timezone'))
        time_filter = {
            "hour": Q(creqted_at__gte=user_datetime - timedelta(hours=1)),
            "today": Q(creqted_at__gte=datatime_to_start_day(user_datetime)),
            "yesterday": Q(created_at__range=[
                datatime_to_start_day(user_datetime),
                datetime_to_end_day(user_datetime)
            ]),
            "week": Q(creqted_at__gte=user_datetime - timedelta(weeks=1)),
            "month": Q(creqted_at__gte=user_datetime - timedelta(days=30))
        }
        return time_filter[timestamp]

    def get_queryset(self):
        timestamp_filter = self.get_filter_timestamp()
        notifications = Notification.objects.filter(timestamp_filter).filter(
            Q(recipient=self.request.user) | Q(recipient__isnull=True)
        )
        return notifications.order_by('-created_at')

    def get_serializer_context(self):
        notification_statistics = self.queryset.values('type').annotate(
            count=Count('type'))
        return {'notification_statistics': notification_statistics}
