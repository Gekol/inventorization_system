from django.contrib.auth.models import User
from rest_framework import permissions
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.reverse import reverse

from auth_service import serializers
from auth_service.serializers import ChangeUserSerializer
from core import IsAdmin


class UserViewSet(viewsets.ModelViewSet):
    """
        Viewset to work with User model
    """
    queryset = User.objects.all().order_by("username")

    def list(self, request, *args, **kwargs):
        users = [{
            "username": user.username,
            "user_link": reverse(f"users-detail", args=[user.id], request=request)
        }
            for user in self.queryset]
        return Response(users)

    def get_permissions(self):
        permission_classes = [permissions.IsAuthenticated]
        if self.action in ["create", "destroy", "update", "partial_update"]:
            permission_classes = [IsAdmin]
        return [permission() for permission in permission_classes]

    def get_serializer_class(self):
        serializer_class = serializers.UserSerializer
        if self.action in ["update", "partial_update"]:
            serializer_class = ChangeUserSerializer
        return serializer_class
