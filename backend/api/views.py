from django.utils import timezone
from django.db.models import Q, Count
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from .filters import get_filter_timestamp
from .models import Notification
# from .serializers import NotificationSerializer


class NotificationView(APIView):
    def get(self, request):
        user = request.user
        user_datetime = timezone.localtime(
            timezone=self.request.query_params.get('timezone')
        )
        timestamp = request.query_params.get('timestamp')
        notifications = get_filter_timestamp(Notification, timestamp,
                                             user_datetime, user)
        if notifications:
            stat = notifications.values('type').annotate(count=Count('type'))
        else:
            stat = None

        return Response({
            "notifications": notifications,
            "statistic": stat},
            status=status.HTTP_200_OK
        )
