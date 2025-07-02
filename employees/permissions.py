from rest_framework.permissions import BasePermission


class CanAccessEmployeeAPI(BasePermission):
    def has_permission(self, request, view):
        allowed_groups = ['CTO', 'Admin', 'Manager']
        return (
            request.user.is_authenticated and
            request.user.groups.filter(name__in=allowed_groups).exists()
        )