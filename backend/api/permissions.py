from rest_framework import permissions


class Blocked(permissions.BasePermission):
    '''
    Разрешение, что никто не может просматривать, изменять и удалять контент
    '''

    def has_permission(self, request, view):
        return False