
from rest_framework.permissions import BasePermission

#permissions check for owner or admin role so other user won't be able to delete the task
class IsOwnerRole(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and (request.user.role == 'ADMIN' or request.user.role == 'OWNER')