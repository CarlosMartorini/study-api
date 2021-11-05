from rest_framework.permissions import BasePermission


class Instructor(BasePermission):
    def allowed(self, request):
        if request.method == 'GET':
            return True
        return request.user.is_superuser


class Facilitator(BasePermission):
    def allowed(self, request):
        if request.method == 'GET':
            return True
        return request.user.is_staff