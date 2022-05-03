from rest_framework import viewsets, permissions
from rest_framework.response import Response

from core.permissions import IsAdmin, IsRepairman
from inventorization_service.models import Item
from rms_service.serializers import RepairSerializer


# CONNECTION = pika.BlockingConnection(
#     pika.ConnectionParameters(host='localhost')
# )
# CHANNEL = CONNECTION.channel()
#
# CHANNEL.exchange_declare(exchange='logs', exchange_type='fanout')


class RepairViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.filter(fix_status="broken")
    serializer_class = RepairSerializer
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ["get", "options", "put", "patch"]

    def get_permissions(self):
        permission_classes = (IsRepairman | IsAdmin,)
        return [permission() for permission in permission_classes]

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.fix_status = self.request.data["fix_status"]
        instance.save()

        # message = {
        #     "fix_status": instance.fix_status,
        #     "item_id": instance.id,
        #     "username": request.user.username
        # }

        # CHANNEL.basic_publish(exchange='logs', routing_key='', body=json.dumps(message))

        return Response(instance.to_dict())
