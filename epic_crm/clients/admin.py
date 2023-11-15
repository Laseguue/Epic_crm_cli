from django.contrib import admin
from .models import Client

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('id','full_name', 'email', 'company_name', 'date_created', 'last_update', 'sales_contact')
