from rest_framework import permissions
from rest_framework.exceptions import PermissionDenied


ERROR_MESSAGES = {
    'update_denied': 'Изменение чужого контента запрещено!',
    'delete_denied': 'Удаление чужого контента запрещено!'
}



class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or (request.user.is_authenticated
                    and (request.user.is_admin or request.user.is_superuser)))


class AuthorOrReadonly(permissions.BasePermission):

    def has_permission(self, request, view):
        return (request.user.is_authenticated
                or request.method in permissions.SAFE_METHODS)

    def has_object_permission(self, request, view, obj):
        if obj.author != request.user:
            if request.method in ['PUT', 'PATCH']:
                raise PermissionDenied(ERROR_MESSAGES['update_denied'])
            if request.method in ['DELETE']:
                raise PermissionDenied(ERROR_MESSAGES['delete_denied'])
        return True


class IsAdminModeratorOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_admin
            or request.user.is_moderator
            or obj.author == request.user
        )



class IsAdministrator(permissions.BasePermission):
    def has_permission(self, request, view):
        return (request.user.is_authenticated
                and (request.user.is_admin or request.user.is_superuser))
