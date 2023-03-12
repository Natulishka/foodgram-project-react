from django.contrib.auth import get_user_model
from django.shortcuts import render
from rest_framework import filters, status, viewsets
from rest_framework.permissions import AllowAny

from api.serializers import UserSerializer

User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    # lookup_field = 'username'
    # search_fields = ('name',)
    # permission_classes = (AllowAny,)
    ordering = ('username',)
