from django.contrib.auth.models import Group, User
from rest_framework import permissions

from inventorization_service.models import Item


class NoAccessPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return False


def _is_in_group(user: User, group_name: str):
    """
    Takes a user and a group name, and returns `True` if the user is in that group.
    :User user:
    :str group_name:
    :return: bool
    """
    try:
        return Group.objects.get(name=group_name).user_set.filter(id=user.id).exists()
    except Group.DoesNotExist:
        return None


def _has_group_permission(user: User, required_groups: list):
    """
    Takes a user and the list of groups and returns 'True' if the user is in all of these groups
    :User user:
    :list required_groups:
    :return: bool
    """
    return any([_is_in_group(user, group_name) for group_name in required_groups])


class IsAdmin(permissions.BasePermission):
    required_groups = ['admin']

    def has_permission(self, request, view):
        has_group_permission = _has_group_permission(request.user, self.required_groups)
        return request.user and has_group_permission


class IsRepairman(permissions.BasePermission):
    required_groups = ['repairman']

    def has_permission(self, request, view):
        has_group_permission = _has_group_permission(request.user, self.required_groups)
        return request.user and has_group_permission


class IsOwner(permissions.BasePermission):
    def has_permission(self, request, view):
        has_owner = bool(len(Item.objects.filter(id=request.parser_context["kwargs"]["pk"], owner_id=request.user.id)))
        in_warehouse = bool(
            len(Item.objects.filter(id=request.parser_context["kwargs"]["pk"], owner_id=None))
        )
        return has_owner or in_warehouse
