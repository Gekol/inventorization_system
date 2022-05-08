from rest_framework import permissions, viewsets
from rest_framework.response import Response

from analytics_service.serializers import ItemTypeSerializer
from core import IsAdmin
from inventorization_service.models import ItemType


class ItemTypesViewSet(viewsets.ModelViewSet):
    queryset = ItemType.objects.all()
    serializer_class = ItemTypeSerializer

    def get_permissions(self):
        permission_classes = [permissions.IsAuthenticated]
        if self.action in ["update", "partial_update"]:
            permission_classes += [IsAdmin]
        return [permission() for permission in permission_classes]


class AnalyticsLinksViewSet(viewsets.ViewSet):
    """
        Viewset to work with User model
    """
    http_method_names = ["get"]

    def list(self, request):
        return Response([f"{request.get_host()}{request.get_full_path()}"])

    def get_permissions(self):
        permission_classes = [permissions.IsAuthenticated, IsAdmin]
        return [permission() for permission in permission_classes]
