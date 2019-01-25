from rest_framework import permissions


class IsOwnerOf(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if obj.first_end == request.user or obj.second_end == request.user:
            return True
        return False
