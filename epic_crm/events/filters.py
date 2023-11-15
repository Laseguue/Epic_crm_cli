from django_filters import rest_framework as filters
from .models import Event

class EventFilter(filters.FilterSet):
    support_contact_is_null = filters.BooleanFilter(field_name='support_contact', lookup_expr='isnull')
    my_events = filters.BooleanFilter(method='filter_my_events')

    def filter_my_events(self, queryset, name, value):
        if value:
            request = self.request
            if request and hasattr(request, 'user'):
                return queryset.filter(support_contact=request.user)
        return queryset

    class Meta:
        model = Event
        fields = ['contract', 'support_contact','event_start_date','event_end_date','location','attendees','notes']