from rest_framework import viewsets, status
from django_filters.rest_framework import DjangoFilterBackend
from .models import CustomUser
from .serializers import UserSerializer
from .permissions import IsAdminOrManagementUser
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.authtoken.models import Token

class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminOrManagementUser]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['id', 'username', 'email', 'first_name', 'last_name', 'groups']

@api_view(['POST'])
def logout(request):
    try:
        request.user.auth_token.delete()
    except (AttributeError, Token.DoesNotExist):
        return Response(status=status.HTTP_400_BAD_REQUEST)
    return Response(status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def current_user(request):
    """
    Renvoie les données de l'utilisateur actuellement connecté.
    """
    user = request.user
    return Response({
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "groups": [group.name for group in user.groups.all()],
    })