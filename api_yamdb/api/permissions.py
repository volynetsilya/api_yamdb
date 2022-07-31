from rest_framework import permissions


class AdminOnly(permissions.BasePermission):
    """Доступ только для пользователей с неограниченными правами."""

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return (
                request.user.is_admin
                or request.user.is_superuser
                or request.user.is_staff
            )
        return False

    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated:
            return (
                request.user.is_admin
                or request.user.is_superuser
                or request.user.is_staff
            )
        return False


class AccountOwnerOnly(permissions.BasePermission):
    """Доступ разрешен только владельцу аккаунта."""

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user