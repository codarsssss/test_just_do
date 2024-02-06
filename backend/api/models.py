from django.contrib.auth import get_user_model
from django.db import models


User = get_user_model()


class Notification(models.Model):
    class Status(models.TextChoices):
        INFO = 'INFO', 'Информационное'
        WARNING = 'WARNING', 'Предупреждающее'
        ERROR = 'ERROR', 'Сообщение об ошибке'

    status = models.CharField(max_length=7, choices=Status.choices)
    author = models.ForeignKey(to=User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100) # надо подумать, нужен ли вообще title
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Уведомление'
        verbose_name_plural = "Уведомления"

    def __str__(self):
        return f"{self.status}-{self.created_at}"
