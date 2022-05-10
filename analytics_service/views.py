from django.db.models import Count, Q
from rest_framework import permissions, viewsets
from rest_framework.generics import ListCreateAPIView
from rest_framework.response import Response

from analytics_service.serializers import ItemTypeSerializer
from core import IsAdmin
from core.analytics import get_relation
from inventorization_service.models import ItemType, Item


class ItemTypesViewSet(viewsets.ModelViewSet):
    queryset = ItemType.objects.all()
    serializer_class = ItemTypeSerializer

    def get_permissions(self):
        permission_classes = [permissions.IsAuthenticated]
        if self.action in ["update", "partial_update"]:
            permission_classes += [IsAdmin]
        return [permission() for permission in permission_classes]


class AnalyticsViewSet(viewsets.ViewSet):
    """
        Viewset to work with User model
    """

    def list(self, request, *args, **kwargs):


        data = [dict(item_type.to_dict(), ** {"in_use": item_type.in_use, "overall": item_type.overall})
                for item_type in get_relation()]
        return Response(data)

    def get_permissions(self):
        permission_classes = [permissions.IsAuthenticated, IsAdmin]
        return [permission() for permission in permission_classes]
