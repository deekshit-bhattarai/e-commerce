from django.contrib.auth import get_user_model
from .serializers import AdminUserSerializer
from rest_framework import viewsets
from .permissions import IsAdminUser

User = get_user_model()

class AdminUserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = AdminUserSerializer
    permission_classes = [IsAdminUser]
