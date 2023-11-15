from django_filters import rest_framework as filters
from .models import Contract

class ContractFilter(filters.FilterSet):
    sales_contact_is_null = filters.BooleanFilter(field_name='sales_contact', lookup_expr='isnull')
    unpaid = filters.BooleanFilter(method='filter_unpaid')

    def filter_unpaid(self, queryset, name, value):
        if value:
            return queryset.exclude(amount_due=0)
        return queryset
    class Meta:
        model = Contract
        fields = ['client', 'sales_contact', 'total_amount', 'amount_due', 'creation_date', 'status', 'sales_contact_is_null']