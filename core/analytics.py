from django.db.models import Count, Q

from analytics_service.models import ItemType


def get_lacking_item_types():
    in_warehouse = Count('item', filter=Q(item__status='in_warehouse'))
    item_types = [item_type.to_dict() for item_type in
                  ItemType.objects.all().annotate(in_warehouse=in_warehouse)
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


def get_lacking_types_messages():
    item_types = [dict(item_type.to_dict(),
                       **{"in_use": item_type.in_use,
                          "total": item_type.total,
                          "relation": item_type.relation})
                  for item_type in get_relation()]
    lacking_item_types = get_lacking_item_types()
    messages = []
    for item_type in item_types:
        if item_type["relation"] >= 80:
            messages.append(f"We are missing items of type {item_type['name']}. "
                            f"The relation of its current usage is equal to {item_type['relation']}%. "
                            f"We should buy {round(item_type['total'] * 0.2)} items of that type.")
    for item_type in lacking_item_types:
        messages.append(f"The number of the items of type {item_type['name']} "
                        f"is less than the minimum equal to {item_type['min_amount']}.")
    return messages
