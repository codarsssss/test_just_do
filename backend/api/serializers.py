# from django.db.models import Count
# from rest_framework import serializers
# from .models import Notification
#
#
# class NotificationSerializer(serializers.ModelSerializer):
#     # notification_statistics = serializers.SerializerMethodField()
#
#     class Meta:
#         model = Notification
#         fields = ['recipient', 'message', 'type', 'created_at']
#
#     # def get_notification_statistics(self):
#     #
#     #     return self.queryset.values('type').annotate(count=Count('type'))
