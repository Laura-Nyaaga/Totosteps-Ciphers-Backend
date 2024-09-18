from rest_framework.permissions import BasePermission

class IsAuthenticatedAndHasPermission(BasePermission):
    def has_permission(self, request, view):
        # Ensure the user is authenticated
        if not request.user or not request.user.is_authenticated:
            return False
        
        # Add any additional custom permission logic here
        # For example, check if the user has a specific permission:
        # return request.user.has_perm('app_label.permission_name')
        
        return True
