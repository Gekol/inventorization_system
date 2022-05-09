import json

from rest_framework import viewsets, permissions
from rest_framework.response import Response

from core import IsOwner, IsAdmin
from core import Logger
from inventorization_service.models import Item
from inventorization_service.serializers import ItemSerializer, ItemUpdateSerializer


class ItemViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    logger = Logger()

    def get_queryset(self):
        queryset = Item.objects.filter(fix_status='ok', type_id=int(self.kwargs["nested_1_pk"]))
        return queryset

    def get_permissions(self):
        permission_classes = [permissions.IsAuthenticated]
        if self.action in ["update", "partial_update"]:
            permission_classes += [IsOwner]
        if self.action in ["create", "destroy"]:
            permission_classes += [IsAdmin]
        return [permission() for permission in permission_classes]

    def get_serializer_class(self):
        serializer_class = ItemSerializer
        if self.action in ["update", "partial_update"]:
            serializer_class = ItemUpdateSerializer
        return serializer_class

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.fix_status = self.request.data["fix_status"]
        message = ""
        if instance.fix_status == "broken":
            message = "Item is broken"
            instance.broke_count += 1

        instance.status = self.request.data["status"]
        if instance.status == "in_warehouse":
            instance.owner = None
            message = "Item is returned to the warehouse" if message == "" else message
        elif instance.type.is_permanent:
            instance.delete()
        else:
            instance.owner = request.user
            message = "Item is taken from the warehouse" if message == "" else message
            instance.save()

        message = {
            "item_id": instance.id,
            "item_name": instance.name,
            "type": instance.type.name,
            "username": request.user.username,
            "message": message
        }

        self.logger.emit_log("info", json.dumps(message))

        return Response(instance.to_dict())
