from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    '''
    Переопределенная модель пользователя.
    Email - уникальный идентификатор.
    Все поля обязательны для заполнения.
    '''

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    email = models.EmailField('E-mail', max_length=255, blank=False,
                              unique=True)
    first_name = models.CharField("first name", max_length=100, blank=False)
    last_name = models.CharField("last name", max_length=100, blank=False)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = 'username',

    def __str__(self):
        return self.username
