from django.db.models import Count, Q
from rest_framework import permissions, viewsets
from rest_framework.generics import ListCreateAPIView
from rest_framework.response import Response

from analytics_service.serializers import ItemTypeSerializer
from core import IsAdmin
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
        in_use = Count('type_id', filter=Q(status='in_use'))
        overall = Count('type_id')
        print(Item.objects.annotate())
        return Response(Item.objects.all())

    def get_permissions(self):
        permission_classes = [permissions.IsAuthenticated, IsAdmin]
        return [permission() for permission in permission_classes]
