from rest_framework.permissions import BasePermission


class ModeratorPermission(BasePermission):
    """
    Проверяет, является ли пользователь модератором.
    """
    def has_permission(self, request, view):
        return request.user.groups.filter(name='Модераторы').exists()


class IsOwner(BasePermission):
    """
        Проверяет, является ли пользователь владельцем.
    """
    def has_object_permission(self, request, view, obj):
        if obj.user == request.user:
            return True
        return False
