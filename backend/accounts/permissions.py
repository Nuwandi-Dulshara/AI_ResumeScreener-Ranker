from rest_framework.permissions import BasePermission


class HasAllowedRole(BasePermission):

    def has_permission(self, request, view):

        if not request.user.is_authenticated:
            return False

        allowed_roles = getattr(
            view,
            "allowed_roles",
            []
        )

        if request.user.is_superuser:
            return True

        return request.user.groups.filter(
            name__in=allowed_roles
        ).exists()