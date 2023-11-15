from rest_framework import permissions

class IsAdminOrManagementUser(permissions.BasePermission):
    """
    La création et la modification d'utilisateurs sont réservées aux administrateurs et aux membres du groupe Management.
    Lecture est disponible pour tous les utilisateurs.
    """

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True

        return request.user and (request.user.is_superuser or request.user.groups.filter(name='Management').exists())
