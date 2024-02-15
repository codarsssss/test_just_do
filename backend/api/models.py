from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class Notification(models.Model):
    TYPE_CHOICES = [
        ('info', 'Информационное'),
        ('warning', 'Предупреждающее'),
        ('error', 'Сообщение об ошибке'),
    ]

    recipient = models.ForeignKey(User, on_delete=models.CASCADE, blank=True,
                                  null=True, related_name='notifications')
    message = models.TextField()
    type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Уведомление'
        verbose_name_plural = "Уведомления"

    def __str__(self):
        return f"{self.status}-{self.created_at}"
