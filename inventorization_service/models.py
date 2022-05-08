from django.contrib.auth.models import User
from django.db import models
from analytics_service.models import ItemType


class Item(models.Model):
    name = models.CharField(max_length=100)
    type = models.ForeignKey(ItemType, on_delete=models.CASCADE, default=1)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, default=None, null=True)
    status = models.CharField(max_length=30, choices=[
        ("in_warehouse", "In warehouse"),
        ("in_use", "In use")
    ])
    fix_status = models.CharField(max_length=30, choices=[
        ("broken", "Broken"),
        ("ok", "OK")
    ], default="ok")
    broke_count = models.IntegerField()

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "type": self.type.name,
            "owner": None if self.owner is None else self.owner.username,
            "status": self.status,
            "fix_status": self.fix_status,
            "broke_count": self.broke_count,
        }

    def __str__(self):
        return f"Id={self.id} Name='{self.name}' Owner={self.owner}"
