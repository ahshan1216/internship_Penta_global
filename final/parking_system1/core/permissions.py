from rest_framework.permissions import BasePermission
from .models import Assign

class IsAdminRole(BasePermission):
    """
    Allow access only to users assigned to the 'admin' role.
    """

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        return Assign.objects.filter(user=request.user, role__name='admin').exists()
