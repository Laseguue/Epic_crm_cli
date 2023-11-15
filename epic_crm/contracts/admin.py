from django.contrib import admin
from .models import Contract

@admin.register(Contract)
class ContractAdmin(admin.ModelAdmin):
    list_display = ('id', 'client', 'sales_contact', 'total_amount', 'amount_due', 'creation_date', 'status')
