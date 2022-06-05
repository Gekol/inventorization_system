from rest_framework import permissions, viewsets
from rest_framework.response import Response
from rest_framework.reverse import reverse

from analytics_service.serializers import ItemTypeSerializer
from core import IsAdmin, AsynchronousMessenger, IsRepairman
from core.analytics import get_relation, get_lacking_item_types
from inventorization_service.models import ItemType


class ItemTypesViewSet(viewsets.ModelViewSet):
    queryset = ItemType.objects.all()
    serializer_class = ItemTypeSerializer

    def list(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.queryset, many=True)
        item_types = serializer.data
        item_type_view_name = "inventory_service" if "/inventory_service/" in request.path else "repair_service"
        items_view_name = "fixed_items" if "/inventory_service/" in request.path else "broken_items"
        item_types = [{
            "item_type": item_type["name"],
            "item_type_info": reverse(f"{item_type_view_name}-detail", args=[item_type["id"]], request=request),
            "items": reverse(f"{items_view_name}-list", args=[item_type["id"]], request=request)
        }
            for item_type in item_types]

        page = self.paginate_queryset(self.queryset)
        if page is not None:
            return self.get_paginated_response(item_types)
        return Response(item_types)

    def get_permissions(self):
        permission_classes = [permissions.IsAuthenticated]
        if self.request.path == "/repair_service/":
            permission_classes = [permissions.IsAuthenticated, IsRepairman]
        if self.action in ["create", "update", "partial_update"]:
            permission_classes = [permissions.IsAuthenticated, IsAdmin]
        return [permission() for permission in permission_classes]


class AnalyticsViewSet(viewsets.ViewSet):
    """
        Viewset to work with User model
    """

    def list(self, request, *args, **kwargs):
        item_types = [dict(item_type.to_dict(),
                           **{"in_use": item_type.in_use,
                              "total": item_type.total,
                              "relation": item_type.relation})
                      for item_type in get_relation()]
        lacking_item_types = get_lacking_item_types()
        asynchronous_messenger = AsynchronousMessenger()
        for item_type in item_types:
            if item_type["relation"] >= 80:
                asynchronous_messenger.send_message("admin_message",
                                                    f"We are missing items of type {item_type['name']}. "
                                                    f"The relation of its current usage is equal "
                                                    f"to {item_type['relation']}%. "
                                                    f"We should buy {round(item_type['total'] * 0.2)} items of "
                                                    f"that type.")
            if item_type["name"] in lacking_item_types:
                asynchronous_messenger.send_message("admin_message",
                                                    f"The number of the items of type {item_type['name']} "
                                                    f"is less than the minimum equal to {item_type['min_amount']}.")
        return Response(item_types)

    def get_permissions(self):
        permission_classes = [permissions.IsAuthenticated]
        if self.action in ["create", "destroy", "update", "partial_update"]:
            permission_classes += [IsAdmin]
        return [permission() for permission in permission_classes]
