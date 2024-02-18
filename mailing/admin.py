from django.contrib import admin

# Register your models here.
from mailing.models import Mailing, Message, Client, Log


# Register your models here.
@admin.register(Mailing)
class ContactAdmin(admin.ModelAdmin):
    """Админка отображения модели Blog"""
    list_display = ('id', 'time', 'status')


@admin.register(Message)
class ContactAdmin(admin.ModelAdmin):
    """Админка отображения модели Blog"""
    list_display = ('id', 'subject', 'body')


@admin.register(Client)
class ContactAdmin(admin.ModelAdmin):
    """Админка отображения модели Blog"""
    list_display = ('id', 'email', 'full_name')


@admin.register(Log)
class ContactAdmin(admin.ModelAdmin):
    """Админка отображения модели Blog"""
    list_display = ('id', 'time', 'status', 'server_response', 'mailing')