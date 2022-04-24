from rest_framework import serializers

from inventorization_service.models import Item


class ItemSerializer(serializers.ModelSerializer):
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
        fields = ['name', 'status', 'fix_status']

    def create(self, validated_data):
        item = Item(
            name=validated_data["name"],
            owner=None,
            status="in_warehouse",
            fix_status="OK",
            broke_count=0
        )
        item.save()
        return item


class ItemUpdateSerializer(serializers.ModelSerializer):

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
        fields = ['owner', 'status', 'fix_status']
