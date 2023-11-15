from django.contrib import admin
from .models import Event

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('id', 'contract', 'support_contact', 'event_start_date', 'event_end_date', 'location', 'attendees')
