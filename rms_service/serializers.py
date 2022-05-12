from rest_framework import serializers

from inventorization_service.models import Item


class RepairSerializer(serializers.ModelSerializer):
    fix_status = serializers.ChoiceField(choices=[
        ("unfixable", "Unfixable"),
        ("ok", "OK")
    ], default="ok")

    def to_representation(self, instance):
        owner = None
        if instance.owner is not None:
            owner = instance.owner.username
        representation = {
            "id": instance.id,
            "type": instance.type.name,
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
