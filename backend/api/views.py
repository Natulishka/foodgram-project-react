from django.contrib.auth import get_user_model
from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status, viewsets
from rest_framework.permissions import AllowAny

from api.serializers import IngredientsSerializer, TagsSerializer
from recipes.models import Ingredient, Tag

User = get_user_model()


class IngridientsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientsSerializer
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    pagination_class = None
    search_fields = ('^name',)
    ordering = ('name',)


class TagsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagsSerializer
    pagination_class = None
