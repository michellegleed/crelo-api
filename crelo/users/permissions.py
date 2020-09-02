from rest_framework import permissions

class IsLoggedInUserOrReadOnly(permissions.BasePermission):
    message = "Oops! Hey Doofus! You need to log in first."

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.id == request.user.id

class IsLoggedInUser(permissions.BasePermission):
    message = "Oops! Hey Doofus! You need to log in first."

    def has_object_permission(self, request, view, obj):
        return obj.id == request.user.id

class IsAdminOrReadOnly(permissions.BasePermission):
    message = "That particular superpower is for Admins only. Soz!"

    def has_permission(self, request, view):
        # if request.method in permissions.SAFE_METHODS:
        #     return True
        # return request.user.is_admin
        return True