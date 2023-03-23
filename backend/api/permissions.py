from rest_framework import permissions


class Blocked(permissions.BasePermission):
    '''
    Разрешение, что никто не может просматривать, изменять и удалять контент.
    '''

    def has_permission(self, request, view):
        return False


class IsAuthorOrAdminOrReadOnly(permissions.BasePermission):
    '''
    Разрешение, что только администратор и автор может изменять и удалять
    контент, для остальных пользователей только чтение.
    Post запрос может делать только пользователь, прошедший аутентификацию.
    '''
    message = ('Только администратор и автор может изменять и удалять'
               ' контент! Post запрос может делать только'
               ' пользователь, прошедший аутентификацию!')

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_authenticated and (
            request.user.is_staff or request.user == obj.author)
