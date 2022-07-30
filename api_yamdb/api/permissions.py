from rest_framework import permissions


class AdminOnly(permissions.BasePermission):
    """Доступ только для пользователей с неограниченными правами."""

    def has_permission(self, request, view):
        return (request.user.is_admin or request.user.is_superuser)

    def has_object_permission(self, request, view, obj):
        return (request.user.is_admin or request.user.is_superuser)


# class IsAuthorOrReadOnly(permissions.BasePermission):
#     """Ограние прав для редактировая чужих публикаций."""

#     def has_object_permission(self, request, view, obj):
#         if request.method in permissions.SAFE_METHODS:
#             return True
#         return obj.author == request.user


# class IsAdminOrReadOnly(permissions.BasePermission):
#     """Ограничение прав для всех кроме администратора."""
#     def has_permission(self, request, view):
#         if request.method in permissions.SAFE_METHODS:
#             return True
#         return request.user.is_admin

#     def has_object_permission(self, request, view, obj):
#         if request.method in permissions.SAFE_METHODS:
#             return True
#         return request.user.is_admin


