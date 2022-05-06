from rest_framework import serializers

from inventorization_service.models import Item
from inventorization_service.models import Item


class RepairSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        owner = None
        if instance.owner is not None:
            owner = instance.owner.username
        representation = {
            "id": instance.id,
            'name': instance.name,
            'owner': owner,
            'status': instance.status,
            'fix_status': instance.fix_status,
            'broke_count': instance.broke_count,
        }
        return representation

    class Meta:
        model = Item
        fields = ['fix_status']