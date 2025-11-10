from rest_framework.permissions import BasePermission


def _user_in_groups(user, groups):
    if not user or not user.is_authenticated:
        return False
    if getattr(user, 'is_superuser', False):
        return True
    return user.groups.filter(name__in=groups).exists()


class GroupRequiredPermission(BasePermission):

    def has_permission(self, request, view):
        required = getattr(view, 'required_groups', None)
        if not required:
            return True
        return _user_in_groups(request.user, required)
