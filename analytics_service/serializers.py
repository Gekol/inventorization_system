from rest_framework import serializers

from analytics_service.models import ItemType


class ItemTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemType
        fields = ['name', 'min_amount', 'is_permanent']

    def to_representation(self, instance):
        representation = {
            "id": instance.id,
            'name': instance.name,
            'min_amount': instance.min_amount,
            'is_permanent': instance.is_permanent
        }
        return representation