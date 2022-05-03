from django.contrib.auth.models import User
from rest_framework import viewsets, permissions
from rest_framework.response import Response

from core import IsOwner, IsAdmin
from inventorization_service.models import Item
from inventorization_service.serializers import ItemSerializer, ItemUpdateSerializer


# CONNECTION = pika.BlockingConnection(
#     pika.ConnectionParameters(host='localhost')
# )
# CHANNEL = CONNECTION.channel()
#
# CHANNEL.exchange_declare(exchange='logs', exchange_type='fanout')


class ItemViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.filter(fix_status='ok')
    permission_classes = [permissions.IsAuthenticated]

    def get_permissions(self):
        permission_classes = [permissions.IsAuthenticated]
        if self.action in ["update", "partial_update"]:
            permission_classes = [IsOwner]
        if self.action in ["create", "destroy"]:
            permission_classes = [IsAdmin]
        return [permission() for permission in permission_classes]

    def get_serializer_class(self):
        serializer_class = ItemSerializer
        if self.action in ["update", "partial_update"]:
            serializer_class = ItemUpdateSerializer
        return serializer_class

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.fix_status = self.request.data["fix_status"]
        if instance.fix_status == "broken":
            instance.broke_count += 1

        instance.status = self.request.data["status"]
        if instance.status == "in_warehouse":
            instance.owner = None
        elif self.request.data["owner"] != "":
            instance.owner = User.objects.get(id=self.request.data["owner"])
        else:
            instance.owner = request.user
        instance.save()

        # message = {
        #     "status": self.request.data["status"],
        #     "item_id": instance.id,
        #     "username": request.user.username
        # }
        # CHANNEL.basic_publish(exchange='logs', routing_key='', body=json.dumps(message))

        return Response(instance.to_dict())
