from django.db import models
from django.conf import settings
from clients.models import Client

class Contract(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='contracts')
    sales_contact = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='contracts')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    amount_due = models.DecimalField(max_digits=10, decimal_places=2)
    creation_date = models.DateField(auto_now_add=True)
    status = models.BooleanField(default=False)

    def __str__(self):
        return f"Contract {self.id} with {self.client}"
