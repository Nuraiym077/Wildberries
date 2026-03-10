from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAuthenticatedUser(BasePermission):

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated


class IsSeller(BasePermission):

    def has_permission(self, request, view):
        return request.user.role == 'seller'


class IsCustomer(BasePermission):

    def has_permission(self, request, view):
        return request.user.role == 'customer'


class IsAdmin(BasePermission):

    def has_permission(self, request, view):
        return request.user.is_staff


class IsProductOwner(BasePermission):

    def has_object_permission(self, request, view, obj):
        return obj.seller == request.user


class IsOrderOwner(BasePermission):

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user


class ReadOnlyOrSeller(BasePermission):

    def has_permission(self, request, view):

        if request.method in SAFE_METHODS:
            return True

        return request.user.role == 'seller'