import json

from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework.reverse import reverse

from core import AsynchronousMessenger
from core.analytics import get_lacking_types_messages
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

    def list(self, request, *args, **kwargs):
        queryset = Item.objects.filter(fix_status='broken', type_id=int(self.kwargs["nested_1_pk"]))

        serializer = self.get_serializer(queryset, many=True)
        items = serializer.data
        view_name = "broken_items"
        items = [{
            "name": item["name"],
            "owner": item["owner"],
            "item_link": reverse(f"{view_name}-detail",
                                 args=[self.kwargs["nested_1_pk"], item["id"]],
                                 request=request)} for item in items]
        return Response(items)

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
        for message in get_lacking_types_messages():
            self.asynchronous_messenger.send_message("admin_message", message)

        return Response(instance.to_dict())
