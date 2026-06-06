from django.contrib import admin
from .models import Notification

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ['destinataire', 'type', 'message', 'is_lue', 'date_creation']
    list_filter = ['type', 'is_lue']
    search_fields = ['destinataire__email', 'message']