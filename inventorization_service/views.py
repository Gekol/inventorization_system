import json

from django.shortcuts import redirect
from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework.reverse import reverse

from core import AsynchronousMessenger
from core import IsOwner, IsAdmin
from inventorization_service.models import Item
from inventorization_service.serializers import ItemSerializer, ItemUpdateSerializer


class ItemViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    asynchronous_messenger = AsynchronousMessenger()

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

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        item = serializer.save()
        item.type_id = int(self.kwargs["nested_1_pk"])
        item.save()
        return redirect("fixed_items-list", nested_1_pk=self.kwargs["nested_1_pk"])

    def list(self, request, *args, **kwargs):
        queryset = Item.objects.filter(fix_status='ok', type_id=int(self.kwargs["nested_1_pk"]))

        serializer = self.get_serializer(queryset, many=True)
        items = serializer.data
        items = [item for item in items if str(item["owner"]) == str(self.request.user) or item["owner"] is None]
        view_name = "fixed_items" if "/inventory_service/" in request.path else "broken_items"
        items = [{
            "name": item["name"],
            "item_link": reverse(f"{view_name}-detail",
                                 args=[self.kwargs["nested_1_pk"], item["id"]],
                                 request=request)} for item in items]
        page = self.paginate_queryset(self.get_queryset())
        if page is not None:
            return self.get_paginated_response(items)
        return Response(items)

    # def retrieve(self, request, *args, **kwargs):
    #     instance = self.get_object()
    #     serializer = self.get_serializer(instance)
    #     return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.fix_status = self.request.data["fix_status"]
        message = ""
        if instance.fix_status == "broken":
            message = "Item is broken"
            instance.broke_count += 1
            instance.save()

        instance.status = self.request.data["status"]
        if instance.status == "in_warehouse":
            instance.owner = None
            message = "Item is returned to the warehouse" if message == "" else message
            instance.save()
        elif instance.type.is_permanent:
            instance.owner = request.user
            message = "Item is permanently taken from the warehouse" if message == "" else message
            instance.save()
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

        self.asynchronous_messenger.send_message("info", json.dumps(message))

        return Response(instance.to_dict())
