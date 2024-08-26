from rest_framework.permissions import BasePermission


class IsAdmin(BasePermission):
    message = "Вы не являетесь администратором"

    def has_permission(self, request, view):
        return request.user.is_staff


class IsOwner(BasePermission):
    message = "Вы не являетесь создателем данного курса"

    def has_object_permission(self, request, view, obj):
        return request.user == obj.user


class IsTeacher(BasePermission):
    message = "Вы не являетесь преподавателем"

    def has_permission(self, request, view):
        return request.user.groups.filter(name="teacher").exists()
