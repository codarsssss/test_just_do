from rest_framework import exceptions
from datetime import timedelta
from django.db.models import Q

from .utils import datetime_to_end_day, datatime_to_start_day


def get_filter_timestamp(model, timestamp, user_datetime, user):
    timestamp_dict = {
        "hour": Q(created_at__gte=user_datetime - timedelta(hours=1)),
        "today": Q(created_at__gte=datatime_to_start_day(user_datetime)),
        "yesterday": Q(created_at__range=[
            datatime_to_start_day(user_datetime),
            datetime_to_end_day(user_datetime)
        ]),
        "week": Q(created_at__gte=user_datetime - timedelta(weeks=1)),
        "month": Q(created_at__gte=user_datetime - timedelta(days=30))
    }

    model.objects.filter(timestamp_dict[timestamp]).filter(
        Q(recipient=user) | Q(recipient__isnull=True)
    )

