from django.db.models import Count
from rest_framework import serializers
from .models import Notification


class NotificationSerializer(serializers.ModelSerializer):
    # notification_statistics = serializers.SerializerMethodField()

    class Meta:
        model = Notification
        fields = ['recipient', 'message', 'status', 'created_at']
