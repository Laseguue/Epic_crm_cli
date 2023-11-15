from rest_framework import permissions
from .models import Event
from contracts.models import Contract

class IsSupportOrManagement(permissions.BasePermission):
    """
    Permission pour permettre à l'équipe de gestion ou au support contact assigné de mettre à jour un événement.
    """

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True

        if request.user.groups.filter(name='Management').exists():
            return True

        if view.action in ['update', 'partial_update']:
            event_id = view.kwargs.get('pk')
            try:
                event = Event.objects.get(pk=event_id)
                return event.support_contact == request.user
            except Event.DoesNotExist:
                return False

        return False

class IsSalesTeamForEvents(permissions.BasePermission):
    """Permission pour les membres de l'équipe commerciale pour créer des événements."""
    def has_permission(self, request, view):
        if view.action != 'create':
            return False

        user_is_sales = request.user.groups.filter(name='Sales').exists()
        if not user_is_sales:
            return False

        contract_id = request.data.get('contract')
        if not contract_id:
            return False

        try:
            contract = Contract.objects.get(id=contract_id)
        except Contract.DoesNotExist:
            return False

        return contract.status and contract.sales_contact == request.user
