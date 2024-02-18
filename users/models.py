from django.contrib.auth.models import AbstractUser
from django.db import models
import random

random_code = ''.join(random.sample('0123456789', 5))
NULLABLE = {'blank': True, 'null': True}


class User(AbstractUser):
    """Модель таблицы User"""
    username = None

    email = models.EmailField(unique=True, verbose_name='Почта')
    phone = models.CharField(max_length=35, verbose_name='Телефон', **NULLABLE)
    country = models.CharField(max_length=25, verbose_name='Страна', **NULLABLE)
    avatar = models.ImageField(upload_to='users/', verbose_name='Аватар', **NULLABLE)
    verify_code = models.CharField(max_length=5, default=random_code, verbose_name='Код верификации')

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        """Класс отображения метаданных"""
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'



