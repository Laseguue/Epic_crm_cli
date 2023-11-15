from rest_framework import viewsets, permissions
from django_filters.rest_framework import DjangoFilterBackend
from .models import Contract
from .serializers import ContractSerializer
from .permissions import IsManagementTeam, IsSalesTeam

class ContractViewSet(viewsets.ModelViewSet):
    queryset = Contract.objects.all()
    serializer_class = ContractSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['client', 'sales_contact','total_amount','amount_due','creation_date','status']

    def get_permissions(self):
        if self.action in ['create']:
            permission_classes = [IsSalesTeam | IsManagementTeam]
        elif self.action in ['update', 'partial_update']:
            permission_classes = [IsSalesTeam | IsManagementTeam]
        elif self.action in ['destroy']:
            permission_classes = [IsManagementTeam]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]
