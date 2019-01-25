from rest_framework import permissions

from hose_usage.models import HoseAssociation, HoseContent


class IsOwnerOf(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if isinstance(obj, HoseAssociation):
            if obj.first_end == request.user or obj.second_end == request.user:
                return True
        elif isinstance(obj, HoseContent):
            hose = HoseContent.hose_from
            if hose.first_end == request.user or hose.second_end == request.user:
                return True
        return False
