from django.contrib.auth.models import User, Group

from inventorization_service.models import Item, ItemType

MOCK_PASSWORD = "Some_password1111"


def get_or_create_group(group_name):
    return Group.objects.get_or_create(name=group_name)


def initialise_test_groups(groups):
    return [get_or_create_group(group_name) for group_name in groups]


def create_user(username, password, groups):
    user = User.objects.create_user(username=username, password=password)
    for group_name in groups:
        group = Group.objects.get(name=group_name)
        group.user_set.add(user)
    return user


def initialise_test_users(pairs):
    return [create_user(user_name, MOCK_PASSWORD, group_name) for user_name, group_name in pairs]


def create_type(name: str, is_permanent):
    return ItemType.objects.create(name=name, is_permanent=is_permanent)


def initialise_test_types(item_types):
    return [create_type(item_type, is_permanent) for item_type, is_permanent in item_types]


def create_item(name: str, type_id, owner: User, fix_status="ok"):
    return Item.objects.create(name=name,
                               type_id=type_id,
                               owner=owner,
                               status="in_use",
                               fix_status=fix_status,
                               broke_count=0 if fix_status == "ok" else 1)


def initialise_test_items(items):
    return [create_item(item_name, type_id, owner, fix_status) for item_name, type_id, owner, fix_status in items]
