from rest_framework.permissions import BasePermission


class IsUser(BasePermission):

    def has_permission(self, request, view):
        if request.user.groups.filter(name="user").exists():
            return True


class IsAdmin(BasePermission):

    def has_permission(self, request, view):
        if request.user.groups.filter(name="admin").exists():
            return True


class IsOwnerForModelUser(BasePermission):

    def has_object_permission(self, request, view, obj):
        return obj == request.user


class IsOwner(BasePermission):

    def has_object_permission(self, request, view, obj):
        return obj.author == request.user
