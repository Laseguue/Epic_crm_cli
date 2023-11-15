from rest_framework import viewsets, permissions
from django_filters.rest_framework import DjangoFilterBackend
from .models import Event
from .serializers import EventSerializer
from .permissions import IsSupportOrManagement, IsSalesTeamForEvents
from .filters import EventFilter

class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = EventFilter

    def get_queryset(self):
        queryset = super().get_queryset()
        filter = self.filterset_class(self.request.GET, queryset=queryset, request=self.request)
        return filter.qs

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            permission_classes = [permissions.IsAuthenticated]
        elif self.action in ['create']:
            permission_classes = [IsSalesTeamForEvents]
        elif self.action in ['update', 'partial_update']:
            permission_classes = [IsSupportOrManagement]
        elif self.action in ['destroy']:
            permission_classes = [IsSupportOrManagement]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]
