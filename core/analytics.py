from django.db.models import Count, Q

from analytics_service.models import ItemType


def get_lacking_item_types():
    in_warehouse = Count('item', filter=Q(item__status='in_warehouse'))
    item_types = [item_type for item_type in
                  ItemType.objects.filter(is_permanent=False).annotate(in_warehouse=in_warehouse)
                  if item_type.min_amount > item_type.in_warehouse]

    return item_types


def get_relation():
    in_use = Count('item', filter=Q(item__status='in_use'))
    total = Count('item')
    item_types = ItemType.objects.filter(is_permanent=False).annotate(in_use=in_use).annotate(total=total)
    res = []
    for item_type in item_types:
        item_type.relation = (item_type.in_use / item_type.total) * 100
        res.append(item_type)
    res.sort(key=lambda x: x.relation)
    return res
