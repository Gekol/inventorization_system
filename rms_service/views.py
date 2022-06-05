import json

from rest_framework import viewsets, permissions
from rest_framework.response import Response

from core import AsynchronousMessenger
from core.permissions import IsAdmin, IsRepairman
from inventorization_service.models import Item
from rms_service.serializers import RepairSerializer


class RepairViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.filter(fix_status="broken")
    serializer_class = RepairSerializer
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ["get", "put", "patch"]
    asynchronous_messenger = AsynchronousMessenger()

    def get_permissions(self):
        permission_classes = (IsRepairman | IsAdmin,)
        return [permission() for permission in permission_classes]

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.fix_status = self.request.data["fix_status"]
        instance.save()

        message = {
            "item_id": instance.id,
            "item_name": instance.name,
            "type": instance.type.name,
            "username": request.user.username,
            "message": "Item fixed" if instance.fix_status == "ok" else "Item can't be fixed!"
        }
        if instance.fix_status == "unfixable":
            instance.delete()

        self.asynchronous_messenger.send_message("info", json.dumps(message))

        return Response(instance.to_dict())
