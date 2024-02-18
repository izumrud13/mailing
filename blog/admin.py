from django.contrib import admin

from blog.models import Blog


# Register your models here.
@admin.register(Blog)
class ContactAdmin(admin.ModelAdmin):
    """Админка отображения модели Blog"""
    list_display = ('id', 'title', 'date_added')