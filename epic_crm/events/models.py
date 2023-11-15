from django.db import models
from django.conf import settings
from contracts.models import Contract

class Event(models.Model):
    contract = models.ForeignKey(Contract, on_delete=models.CASCADE, related_name='events')
    support_contact = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='events')
    event_start_date = models.DateTimeField()
    event_end_date = models.DateTimeField()
    location = models.CharField(max_length=255)
    attendees = models.IntegerField()
    notes = models.TextField()

    def __str__(self):
        return f"Event {self.id} - {self.contract.client.full_name}"
