from django.db.models import Count, Q
from django.http import HttpResponseRedirect
from rest_framework import permissions, viewsets
from rest_framework.generics import ListCreateAPIView
from rest_framework.response import Response
from rest_framework.reverse import reverse

from analytics_service.serializers import ItemTypeSerializer
from core import IsAdmin
from core.analytics import get_relation
from inventorization_service.models import ItemType, Item


class ItemTypesViewSet(viewsets.ModelViewSet):
    queryset = ItemType.objects.all()
    serializer_class = ItemTypeSerializer

    def list(self, request, *args, **kwargs):
        page = self.paginate_queryset(self.queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(self.queryset, many=True)
        item_types = serializer.data
        for item_type in item_types:
            item_type["link"] = f"{self}"
        print(str(self.request.path))
        for key in self.request.META:
            print(key, self.request.META[key])
        return super().list(request, *args, **kwargs)
        # return HttpResponseRedirect(redirect_to=f"{self.request.build_absolute_url()}")

    def get_permissions(self):
        permission_classes = [permissions.IsAuthenticated]
        if self.action in ["create", "update", "partial_update"]:
            permission_classes += [IsAdmin]
        return [permission() for permission in permission_classes]


class AnalyticsViewSet(viewsets.ViewSet):
    """
        Viewset to work with User model
    """

    def list(self, request, *args, **kwargs):
        data = [dict(item_type.to_dict(), **{"in_use": item_type.in_use, "total": item_type.total})
                for item_type in get_relation()]
        return Response(data)

    def get_permissions(self):
        permission_classes = [permissions.IsAuthenticated]
        if self.action in ["create", "destroy", "update", "partial_update"]:
            permission_classes += [IsAdmin]
        return [permission() for permission in permission_classes]
