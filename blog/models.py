from django.conf import settings
from django.db import models

NULLABLE = {'blank': True, 'null': True}


class Blog(models.Model):
    """Модель таблицы - статьи"""
    title = models.CharField(max_length=150, verbose_name='Заголовок')
    slug = models.CharField(max_length=150, **NULLABLE, verbose_name='slug')
    image = models.ImageField(upload_to='products/', **NULLABLE, verbose_name='Превью')
    content = models.TextField(max_length=1000, verbose_name='Содержимое')
    is_published = models.BooleanField(default=False, verbose_name='Опубликовано')
    date_added = models.DateField(auto_now_add=True, verbose_name='Дата создания')
    views_count = models.IntegerField(verbose_name='Количество просмотров', default=0)

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, default=1,
                             verbose_name='Пользователь', **NULLABLE)

    def __str__(self):
        return f'{self.title}'

    class Meta:
        """Класс отображения метаданных"""
        verbose_name = 'Публикация'
        verbose_name_plural = 'Публикации'