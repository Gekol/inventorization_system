from django.db import models


class ItemType(models.Model):
    name = models.CharField(max_length=100)
    min_amount = models.IntegerField(default=3)
    is_permanent = models.BooleanField(default=False)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "min_amount": self.min_amount,
            "is_permanent": self.is_permanent
        }

    def __str__(self):
        return self.name
