from rest_framework import permissions
from clients.models import Client
from contracts.models import Contract

class IsSalesTeam(permissions.BasePermission):
    """Permission pour les membres de l'équipe commerciale."""
    def has_permission(self, request, view):
        if view.action in ['list', 'retrieve']:
            return True
        return request.user.groups.filter(name='Sales').exists()

    def has_object_permission(self, request, view, obj):
        if view.action == 'create':
            return True
        return obj.sales_contact == request.user

class IsManagementTeam(permissions.BasePermission):
    """Permission pour les membres de l'équipe de gestion."""
    def has_permission(self, request, view):
        return request.user.groups.filter(name='Management').exists()

    def has_object_permission(self, request, view, obj):
        return True
    